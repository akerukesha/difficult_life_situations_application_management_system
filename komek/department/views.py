# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from utils import codes, http, string_utils, messages,  token, time_utils

from models import Department

def index(request):
    return HttpResponse("Authe index.")


@csrf_exempt
@http.json_response()
@require_http_methods("GET")
def get_departments(request):
    """
    """
    try:
        departments = Department.objects.all()
        return {
            'departments': [d.full() for d in departments]
        }
    except Exception as e:
        return http.code_response(codes.SERVER_ERROR, message=str(e))