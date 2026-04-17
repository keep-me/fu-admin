# -*- coding: utf-8 -*-
# @Time    : 2024/4/17
# @Author  : 数据报表模块
# @FileName: report.py
# @Software: PyCharm
from typing import List
from datetime import datetime, timedelta
from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from ninja import Field, ModelSchema, Query, Router, Schema
from ninja.pagination import paginate
from system.models import Users, Role, Dept, OperationLog, LoginLog
from utils.fu_ninja import FuFilters, MyPagination
from utils.fu_response import FuResponse

router = Router()


class ReportSchema(Schema):
    total_count: int = Field(0, description="总数")
    active_count: int = Field(0, description="活跃数")
    inactive_count: int = Field(0, description="非活跃数")


class UserTrendItem(Schema):
    date: str
    count: int


class UserDistributionItem(Schema):
    name: str
    value: int


class LogTrendItem(Schema):
    date: str
    success_count: int
    fail_count: int


class DeptDistributionItem(Schema):
    name: str
    user_count: int
    role_count: int


class RoleDistributionItem(Schema):
    name: str
    user_count: int


@router.get("/report/user/overview", response=ReportSchema)
def user_overview(request):
    total_count = Users.objects.count()
    active_count = Users.objects.filter(status=True).count()
    inactive_count = Users.objects.filter(status=False).count()
    return {
        "total_count": total_count,
        "active_count": active_count,
        "inactive_count": inactive_count,
    }


@router.get("/report/user/trend")
def user_trend(request, days: int = 30):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    users = (
        Users.objects
        .filter(create_datetime__gte=start_date)
        .annotate(date=TruncDate('create_datetime'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )
    
    result = []
    date_dict = {item['date']: item['count'] for item in users}
    
    for i in range(days):
        current_date = (start_date + timedelta(days=i)).date()
        result.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "count": date_dict.get(current_date, 0)
        })
    
    return result


@router.get("/report/user/distribution/gender")
def user_distribution_gender(request):
    result = []
    for value, name in Users.GENDER_CHOICES:
        count = Users.objects.filter(gender=value).count()
        if count > 0:
            result.append({"name": name, "value": count})
    return result


@router.get("/report/user/distribution/status")
def user_distribution_status(request):
    active_count = Users.objects.filter(status=True).count()
    inactive_count = Users.objects.filter(status=False).count()
    return [
        {"name": "启用", "value": active_count},
        {"name": "禁用", "value": inactive_count},
    ]


@router.get("/report/user/distribution/type")
def user_distribution_type(request):
    result = []
    for value, name in Users.USER_TYPE:
        count = Users.objects.filter(user_type=value).count()
        if count > 0:
            result.append({"name": name, "value": count})
    return result


@router.get("/report/log/overview")
def log_overview(request, days: int = 30):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    operation_count = OperationLog.objects.filter(create_datetime__gte=start_date).count()
    login_count = LoginLog.objects.filter(create_datetime__gte=start_date).count()
    success_count = OperationLog.objects.filter(
        create_datetime__gte=start_date,
        status=True
    ).count()
    fail_count = operation_count - success_count
    
    return {
        "operation_count": operation_count,
        "login_count": login_count,
        "success_count": success_count,
        "fail_count": fail_count,
    }


@router.get("/report/log/operation/trend")
def log_operation_trend(request, days: int = 30):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    logs = (
        OperationLog.objects
        .filter(create_datetime__gte=start_date)
        .annotate(date=TruncDate('create_datetime'))
        .values('date', 'status')
        .annotate(count=Count('id'))
        .order_by('date')
    )
    
    result = []
    date_dict = {}
    
    for item in logs:
        date_key = item['date']
        if date_key not in date_dict:
            date_dict[date_key] = {"success_count": 0, "fail_count": 0}
        if item['status']:
            date_dict[date_key]['success_count'] = item['count']
        else:
            date_dict[date_key]['fail_count'] = item['count']
    
    for i in range(days):
        current_date = (start_date + timedelta(days=i)).date()
        data = date_dict.get(current_date, {"success_count": 0, "fail_count": 0})
        result.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "success_count": data.get('success_count', 0),
            "fail_count": data.get('fail_count', 0)
        })
    
    return result


@router.get("/report/log/login/trend")
def log_login_trend(request, days: int = 30):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    logs = (
        LoginLog.objects
        .filter(create_datetime__gte=start_date)
        .annotate(date=TruncDate('create_datetime'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )
    
    result = []
    date_dict = {item['date']: item['count'] for item in logs}
    
    for i in range(days):
        current_date = (start_date + timedelta(days=i)).date()
        result.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "count": date_dict.get(current_date, 0)
        })
    
    return result


@router.get("/report/log/operation/modules")
def log_operation_modules(request, days: int = 30):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    logs = (
        OperationLog.objects
        .filter(create_datetime__gte=start_date)
        .values('request_modular')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    
    result = []
    for item in logs:
        if item['request_modular']:
            result.append({
                "name": item['request_modular'],
                "value": item['count']
            })
    
    return result[:10]


@router.get("/report/dept/overview")
def dept_overview(request):
    total_dept = Dept.objects.count()
    active_dept = Dept.objects.filter(status=True).count()
    total_user = Users.objects.count()
    
    return {
        "total_dept": total_dept,
        "active_dept": active_dept,
        "total_user": total_user,
    }


@router.get("/report/dept/distribution")
def dept_distribution(request):
    depts = Dept.objects.all()
    result = []
    
    for dept in depts:
        user_count = Users.objects.filter(dept=dept).count()
        result.append({
            "name": dept.name,
            "user_count": user_count,
        })
    
    return sorted(result, key=lambda x: x['user_count'], reverse=True)


@router.get("/report/role/overview")
def role_overview(request):
    total_role = Role.objects.count()
    active_role = Role.objects.filter(status=True).count()
    
    return {
        "total_role": total_role,
        "active_role": active_role,
    }


@router.get("/report/role/distribution")
def role_distribution(request):
    roles = Role.objects.all()
    result = []
    
    for role in roles:
        user_count = Users.objects.filter(role=role).count()
        result.append({
            "name": role.name,
            "user_count": user_count,
        })
    
    return sorted(result, key=lambda x: x['user_count'], reverse=True)
