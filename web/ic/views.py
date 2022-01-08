from django.shortcuts import render
from .models import Employees

from datetime import datetime


def index(request):
    """Главная страница"""
    # Выбираем список сотрудников, у кого в текущем месяце день рождения
    employees = Employees.objects.all()
    current_month = datetime.now().month
    return render(request, 'ic/index.html', {'employees': employees,
                                             'current_month': current_month})

