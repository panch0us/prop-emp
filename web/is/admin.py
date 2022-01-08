from django.contrib import admin
# Из моделей своего приложения (файл models.py) импортируем нужные для отображения в административной части сайта
from .models import InformationSystems, UsersInformationSystems, Raions

"""Добавляем "классы редакторы" для отображения названий полей в админке"""


class InformationSystemsAdmin(admin.ModelAdmin):
    """Информационные системы"""
    list_display = ('is_title', 'is_note',)
    list_display_links = ('is_title', 'is_note',)
    search_fields = ('is_title', 'is_note',)


class UsersInformationSystemsAdmin(admin.ModelAdmin):
    """Пользователи информационных систем"""
    list_display = ('fk_is_title', 'uis_surname', 'uis_name', 'uis_middle_name', 'fk_div', 'uis_position', 'uis_email',
    				'uis_login', 'uis_password', 'uis_phone', 'uis_note',)
    list_display_links = ('fk_is_title', 'uis_surname', 'uis_name', 'uis_middle_name', 'fk_div', 'uis_position',
    					  'uis_email', 'uis_login', 'uis_password', 'uis_phone', 'uis_note',)
    search_fields = ('fk_is_title__is_title', 'uis_surname', 'uis_name', 'uis_middle_name', 'fk_div__div_title',
					 'uis_position', 'uis_email', 'uis_login', 'uis_password', 'uis_phone', 'uis_note',)


class RaionsAdmin(admin.ModelAdmin):
    """Информационные системы"""
    list_display = ('r_title', 'r_surname', 'r_name', 'r_middle_name', 'r_position', 'r_email', 'r_phone', 'r_note',)
    list_display_links = ('r_title', 'r_surname', 'r_name', 'r_middle_name', 'r_position', 'r_email', 'r_phone', 'r_note',)
    search_fields = ('r_title', 'r_surname', 'r_name', 'r_middle_name', 'r_position', 'r_email', 'r_phone', 'r_note',)


admin.site.register(InformationSystems, InformationSystemsAdmin)
admin.site.register(UsersInformationSystems, UsersInformationSystemsAdmin)
admin.site.register(Raions, RaionsAdmin)