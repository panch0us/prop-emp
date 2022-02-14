from django.shortcuts import render

from django.views.generic import ListView, DetailView

from .models import Employees

from datetime import datetime


class EmployeesView(ListView):
    """Список сотрудников, подставляет к названию модели _list"""
    model = Employees
    queryset = Employees.objects.all()
    current_month = datetime.now().month
    context_object_name = 'employees_list'


class EmployeesDetailView(DetailView):
    """Полное описание сотрудника по url (slug)"""
    model = Employees
    slug_field = "emp_url"


class Asd(ListView):
    """Дни рождения сотрудников в текущем месяце (ДОРАБОТАТЬ ПОСЛЕ)"""
    # current_month = datetime.now().month
    pass
