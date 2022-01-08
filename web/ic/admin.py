from django.contrib import admin

from .models import Cabinets, TypesWork, Divisions, DepartmentsFirst, DepartmentsSecond, Positions, EmployeesStatus, \
                    Employees, ComputersIsod, DiskStorageIsod

"""Добавляем "классы редакторы" для отображения названий полей в админке"""


class CabinetsAdmin(admin.ModelAdmin):
    """Кабинеты"""
    list_display = ('cab_num',)
    list_display_links = ('cab_num',)
    search_fields = ('cab_num',)


class TypesWorkAdmin(admin.ModelAdmin):
    """Виды служб"""
    list_display = ('tw_title',)
    list_display_links = ('tw_title',)
    search_fields = ('tw_title',)


class DivisionsAdmin(admin.ModelAdmin):
    """Подразделения"""
    list_display = ('div_title',)
    list_display_links = ('div_title',)
    search_fields = ('div_title',)


class DepartmentsFirstAdmin(admin.ModelAdmin):
    """Отделы"""
    list_display = ('dep_first_title', 'fk_div')
    list_display_links = ('dep_first_title', 'fk_div')
    search_fields = ('dep_first_title',)


class DepartmentsSecondAdmin(admin.ModelAdmin):
    """Отделения"""
    list_display = ('dep_second_title', 'fk_dep_first',)
    list_display_links = ('dep_second_title', 'fk_dep_first',)
    search_fields = ('dep_second_title',)


class PositionsAdmin(admin.ModelAdmin):
    """Должности"""
    list_display = ('pos_title', 'fk_dep_second', 'fk_dep_first', 'fk_division', 'pos_quantity', 'fk_types_work')
    list_display_links = ('pos_title', 'fk_dep_second', 'fk_dep_first', 'fk_division', 'pos_quantity', 'fk_types_work')
    search_fields = ('pos_title', 'pos_quantity',)


class EmployeesStatusAdmin(admin.ModelAdmin):
    """Статусы сотруднков"""
    list_display = ('emp_status',)
    list_display_links = ('emp_status',)
    search_fields = ('emp_status',)


class EmployeesAdmin(admin.ModelAdmin):
    """Сотрудники"""
    list_display = ('emp_surname', 'emp_name', 'emp_middle_name', 'emp_birthday', 'fk_emp_status', 'fk_position',
                    'fk_types_work',)
    list_display_links = ('emp_surname', 'emp_name', 'emp_middle_name', 'emp_birthday', 'fk_emp_status', 'fk_position',
                          'fk_types_work',)
    search_fields = ('emp_surname', 'emp_name', 'emp_middle_name', 'emp_birthday',)


class ComputersIsodAdmin(admin.ModelAdmin):
    """Компьютеры для работы в сети ИСОД МВД"""
    list_display = ('comp_reg_num', 'comp_factory_num', 'comp_mac_address', 'comp_ip_address',
                    'comp_virt_ip_address', 'comp_id_dst_file', 'comp_title_dst_file', 'fk_cabinet_location',
                    'fk_comp_owner', 'comp_attestation_status',)
    list_display_links = ('comp_reg_num', 'comp_factory_num', 'comp_mac_address', 'comp_ip_address',
                          'comp_virt_ip_address', 'comp_id_dst_file', 'comp_title_dst_file', 'fk_cabinet_location',
                          'fk_comp_owner', 'comp_attestation_status',)
    search_fields = ('comp_reg_num', 'comp_factory_num', 'comp_mac_address', 'comp_ip_address',
                     'comp_virt_ip_address', 'comp_id_dst_file', 'comp_title_dst_file', 'comp_attestation_status',)


class DiskStorageIsodAdmin(admin.ModelAdmin):
    """Дисковые хранилища для компьютеров, подключенных к сети ИСОД МВД"""
    list_display = ('disk_reg_num', 'disk_model', 'disk_size', 'disk_factory_num', 'fk_disk_owner', 'fk_install_in_comp')
    list_display_links = ('disk_reg_num', 'disk_model', 'disk_size', 'disk_factory_num', 'fk_disk_owner',
                          'fk_install_in_comp')
    search_fields = ('disk_reg_num', 'disk_model', 'disk_factory_num',)


admin.site.register(Cabinets, CabinetsAdmin)
admin.site.register(TypesWork, TypesWorkAdmin)
admin.site.register(Divisions, DivisionsAdmin)
admin.site.register(DepartmentsFirst, DepartmentsFirstAdmin)
admin.site.register(DepartmentsSecond, DepartmentsSecondAdmin)
admin.site.register(Positions, PositionsAdmin)
admin.site.register(EmployeesStatus, EmployeesStatusAdmin)
admin.site.register(Employees, EmployeesAdmin)
admin.site.register(ComputersIsod, ComputersIsodAdmin)
admin.site.register(DiskStorageIsod, DiskStorageIsodAdmin)

