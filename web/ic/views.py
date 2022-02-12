from django.shortcuts import render
# Ниже одна строка импортируется для класса EmployeesBirthMonth
from django.views.generic.base import View
from .models import Employees

from datetime import datetime


class EmployeesBirthMonth(View):
    """Месяц рождения сотрудников"""
    def get(self, request):
        """Главная страница"""
        # Выбираем список сотрудников, у кого в текущем месяце день рождения
        employees = Employees.objects.all()
        current_month = datetime.now().month
        return render(request, 'ic/employees.html', {'employees': employees, 'current_month': current_month})

