from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from django.views.generic import ListView, DetailView

from .models import Employees, DepartmentsFirst

from datetime import datetime


class EmployeesView(LoginRequiredMixin, ListView):
    """Список сотрудников, подставляет к названию модели _list (НЕ ЗАДЕЙСТВОВАН!)"""
    model = Employees
    queryset = Employees.objects.all()
    # current_month = datetime.now().month
    context_object_name = 'employees_list'
    # Если пользователь не авторизован, его перенаправит на страницу авторизации
    login_url = '/ic/accounts/login/'


class EmployeesDetailView(LoginRequiredMixin, DetailView):
    """Полное описание сотрудника по url (slug)"""
    model = Employees
    slug_field = "emp_url"
    # Если пользователь не авторизован, его перенаправит на страницу авторизации
    login_url = '/ic/accounts/login/'


class PhonebookView(LoginRequiredMixin, ListView):
    """Телефонный справочник сотрдуников"""
    model = Employees
    template_name = 'ic/phone_book.html'
    queryset = Employees.objects.all()
    context_object_name = 'employees'
    # Если пользователь не авторизован, его перенаправит на страницу авторизации
    login_url = '/ic/accounts/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = DepartmentsFirst.objects.all()
        return context


class Asd(ListView):
    """Дни рождения сотрудников в текущем месяце (ДОРАБОТАТЬ ПОСЛЕ)"""
    # current_month = datetime.now().month
    pass
