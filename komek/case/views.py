# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from utils import codes, messages, token, http, time_utils
from utils.user_types import USER_TYPES, USER, SOCIAL_WORKER, COMMISSION_HEAD, DEPARTMENTAL_WORKER, DEPARTMENTAL_COMMISSION

from models import Priority, Comment, Case, CaseDepartmentPriority, SolutionCase, ResultCase
from department.models import Department, UserDepartment

def index(request):
    return HttpResponse("Authe index.")

@csrf_exempt
@http.json_response()
@http.require_http_methods("GET")
def get_priorities(request):
    """
    """
    try:
        return {
            'priorities': [x.full() for x in Priority.objects.all()]
        }
    except Exception as e:
        return http.code_response(codes.SERVER_ERROR, message=str(e))


@csrf_exempt
@http.json_response()
@require_http_methods("GET")
@http.requires_token()
def get_all_cases(request, user):
    """
    """
    try:
        print(request)
        print(user)
        return {
            'cases': [x.full() for x in Case.objects.all()]
        }
    except Exception as e:
        return http.code_response(codes.SERVER_ERROR, message=str(e))


@csrf_exempt
@http.json_response()
@require_http_methods("POST")
@http.required_parameters(["cases[]"])
def create_cases(request):
    try:
        cases = request.POST.getlist("cases[]", [])
        print(cases)
        if len(cases) == 0:
            return http.code_response(code=codes.NO_CASES, message=messages.NO_CASES)

        new_cases = []
        for case in cases:
            case = json.loads(case)
            full_name = case["full_name"]
            iin = case["iin"]
            address = case["address"]
            address_residential = case["address_residential"]
            contacts = case["contacts"]
            status = case["status"]
            place_of_work = case["place_of_work"]
            occupation = case["occupation"]
            income = case["income"]
            health_condition = case["health_condition"]
            description = case["description"]
            new_case = None
            if full_name and iin and address and address_residential and \
                contacts and status and place_of_work and occupation and \
                income and health_condition and description:
                new_case, _ = Case.objects.get_or_create(full_name=full_name,
                    iin=iin, address=address, address_residential=address_residential,
                    contacts=contacts, status=status, place_of_work=place_of_work,
                    occupation=occupation, income = income,
                    health_condition=health_condition, description=description)
            else:
                return http.code_response(code=codes.MISSING_REQUIRED_PARAMS,
                                      message=messages.MISSING_REQUIRED_PARAMS)
            print(new_case)
            
            parent_case = new_cases[0].id if len(new_cases) > 0 else new_case.id
            new_case.parent_case = parent_case
            new_case.save()
            new_cases.append(new_case)

        return http.ok_response()

    except Exception as e:
        return http.code_response(codes.SERVER_ERROR, message=str(e))


@csrf_exempt
@http.json_response()
@require_http_methods("POST")
@http.required_parameters(["cases[]"])
@http.requires_token()
def update_cases(request, user):
    try:
        cases = request.POST.getlist("cases[]", [])
        if len(cases) == 0:
            return http.code_response(code=codes.NO_CASES, message=messages.NO_CASES)

        new_cases = []
        print(cases)
        
        for case in cases:
            case = json.loads(case)
            case_id = case["case_id"]
            if case_id is None:
                return http.code_response(code=codes.NO_CASE_ID, message=messages.NO_CASE_ID)
            current_case = Case.objects.get(id=case_id)
            print(current_case)
            full_name = case["full_name"]
            iin = case["iin"]
            address = case["address"]
            address_residential = case["address_residential"]
            contacts = case["contacts"]
            status = case["status"]
            place_of_work = case["place_of_work"]
            occupation = case["occupation"]
            income = case["income"]
            health_condition = case["health_condition"]
            description = case["description"]
        
            if full_name and iin and address and address_residential and \
                contacts and status and place_of_work and occupation and \
                income and health_condition and description:
                current_case.full_name = case["full_name"]
                current_case.iin = case["iin"]
                current_case.address = case["address"]
                current_case.address_residential = case["address_residential"]
                current_case.contacts = case["contacts"]
                current_case.status = case["status"]
                current_case.place_of_work = case["place_of_work"]
                current_case.occupation = case["occupation"]
                current_case.income = case["income"]
                current_case.health_condition = case["health_condition"]
                current_case.description = case["description"]
                current_case.save()
            else:
                return http.code_response(code=codes.MISSING_REQUIRED_PARAMS,
                                      message=messages.MISSING_REQUIRED_PARAMS)
            print("HERE")
            if case.get("parent_case") is not None:
                current_case.parent_case = case["parent_case"]
            if case.get("needs") is not None:
                current_case.needs = case["needs"]
            if case["problems"] is not None:
                current_case.problems = case["problems"]
            if case.get("is_approved_by_social_worker") is not None:
                current_case.is_approved_by_social_worker = case["is_approved_by_social_worker"]
            if case.get("place") is not None and case.get("datetime") is not None:
                current_case.place = case["place"]
                current_case.datetime = case["datetime"]
                child_cases = Case.objects.filter(parent_case=current_case.parent_case)
                for c in child_cases:
                    c.place = case["place"]
                    c.datetime = case["datetime"]
                    c.save()
            current_case.save()
            print(current_case)

            if case.get("departments") is not None:
                departments = case["departments"]
                for d in departments:
                    d_id = d["department_id"]
                    p_id = d["priority_id"]
                    cdp, _ = CaseDepartmentPriority.objects.get_or_create(case=current_case,
                                        department=Department.objects.get(id=d_id),
                                        priority=Priority.objects.get(id=p_id))
                    print(cdp)

            if user.user_type == DEPARTMENTAL_WORKER:
                if case.get("solution") is not None:
                    solution = case["solution"]
                if solution.get("comment_text") is not None:
                    comment_text = solution["comment_text"]
                if solution.get("timestamp") is not None:
                    timestamp = solution["timestamp"]
                if solution.get("is_done") is not None:
                    is_done = solution["is_done"]
                user_department = UserDepartment.objects.get(user=user)
                comment, _ = Comment.objects.get_or_create(user=user,
                                        text=comment_text, timestamp=timestamp)
                solution_case, _ = SolutionCase.objects.get_or_create(case=current_case,
                            user_department=user_department, comment=comment,
                            is_done=is_done, timestamp=timestamp)
                print(solution_case)

            if user.user_type == DEPARTMENTAL_COMMISSION:
                if case.get("deadline") is not None:
                    deadline = case["deadline"]
                    current_case.deadline = deadline
                if case.get("result") is not None:
                    result = case["result"]
                if result.get("comment_text") is not None:
                    comment_text = result["comment_text"]
                if result.get("timestamp") is not None:
                    timestamp = result["timestamp"]
                if result.get("is_done") is not None:
                    is_done = result["is_done"]
                user_department = UserDepartment.objects.get(user=user)
                comment, _ = Comment.objects.get_or_create(user=user,
                                        text=comment_text, timestamp=timestamp)
                result_case, _ = ResultCase.objects.get_or_create(case=current_case,
                            user_department=user_department, comment=comment,
                            is_done=is_done, timestamp=timestamp)
                print(result_case)

            if user.user_type == COMMISSION_HEAD and case.get("is_approved") is not None:
                current_case.is_approved = case["is_approved"]

            print(current_case)
            current_case.save()
            new_cases.append(current_case)


        return http.ok_response()

    except Exception as e:
        return http.code_response(codes.SERVER_ERROR, message=str(e))