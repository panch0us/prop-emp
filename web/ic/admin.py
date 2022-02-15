from django.contrib import admin

from .models import Cabinets, TypesWork, Divisions, DepartmentsFirst, DepartmentsSecond, Positions, EmployeesStatus, \
                    Employees, ComputersIsod, DiskStorageIsod, PropertyStandarts, Property, TypesProperty, Ranks, \
                    IssueOfficeProducts, AccountingCryptographicSecurity, OtherNetworkProperty, \
                    OtherInformationAboutComputers, DepartmentsRegionalLevel

# Определяем главную страницу сайта (в Админке при нажатии "Открыть сайт" перенаправит на этот адрес)
admin.site.site_url = '/ic'

"""Добавляем "классы редакторы" для отображения названий полей в админке"""


class RanksAdmin(admin.ModelAdmin):
    """Вид имущества"""
    list_display = ('r_title', 'r_note',)
    list_display_links = ('r_title', 'r_note',)
    search_fields = ('r_title', 'r_note',)


class TypesPropertyAdmin(admin.ModelAdmin):
    """Звания"""
    list_display = ('tp_type', 'tp_note',)
    list_display_links = ('tp_type', 'tp_note',)
    search_fields = ('tp_type', 'tp_note',)


class CabinetsAdmin(admin.ModelAdmin):
    """Кабинеты"""
    list_display = ('cab_num', 'cab_note',)
    list_display_links = ('cab_num', 'cab_note',)
    search_fields = ('cab_num', 'cab_note',)


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
                    'fk_rank', 'fk_cabinet_location', 'emp_phone', 'emp_phone_home', 'emp_phone_mobile',
                    'emp_home_address', 'fk_depart_region_lvl', 'emp_sport_class', 'emp_date_sport_class',
                    'emp_date_document_sport_class', 'emp_number_sport_class', 'emp_note', 'emp_url')
    list_display_links = ('emp_surname', 'emp_name', 'emp_middle_name', 'emp_birthday', 'fk_emp_status', 'fk_position',
                    'fk_rank', 'fk_cabinet_location', 'emp_phone', 'emp_phone_home', 'emp_phone_mobile',
                    'emp_home_address', 'fk_depart_region_lvl', 'emp_sport_class', 'emp_date_sport_class',
                    'emp_date_document_sport_class', 'emp_number_sport_class', 'emp_note',)
    search_fields = ('emp_surname', 'emp_name', 'emp_middle_name', 'emp_birthday',
                     'fk_cabinet_location__cab_num', 'emp_note',)
    list_filter = ('fk_position__fk_dep_first',)

    def get_queryset(self, request):
        qs = super(EmployeesAdmin, self).get_queryset(request)
        # Если текущий пользователь суперюзер возвращаем всё:
        if request.user.is_superuser:
            return qs
        # Если текущий пользователь принадлежит к группе "Вычислительный центр":
        if request.user.groups.filter(name='Отдел оперативного учета и специальных фондов').exists():
            return qs.filter(fk_position__fk_dep_first=1)
        if request.user.groups.filter(name='Отдел разыскных и криминалистических учетов').exists():
            return qs.filter(fk_position__fk_dep_first=2)
        if request.user.groups.filter(name='Отдел пофамильного и дактилоскопического учета').exists():
            return qs.filter(fk_position__fk_dep_first=3)
        if request.user.groups.filter(name='Отдел статистической информации').exists():
            return qs.filter(fk_position__fk_dep_first=4)
        if request.user.groups.filter(name='Отдел предоставления государственных услуг').exists():
            return qs.filter(fk_position__fk_dep_first=5)
        if request.user.groups.filter(name='Вычислительный центр').exists():
            return qs.filter(fk_position__fk_dep_first=6)
        if request.user.groups.filter(name='Канцелярия').exists():
            return qs.filter(fk_position__fk_dep_first=7)
        return qs


class OtherInformationAboutComputersAdmin(admin.ModelAdmin):
    """Иная информация о вычислительной технике"""
    list_display = ('fk_prop', 'oiac_os', 'oiac_user_name', 'oiac_user_pass', 'oiac_comp_name', 'oiac_comp_workgroup',
                    'oiac_note',)
    list_display_links = ('fk_prop', 'oiac_os', 'oiac_user_name', 'oiac_user_pass', 'oiac_comp_name',
                          'oiac_comp_workgroup', 'oiac_note',)
    search_fields = ('oiac_os', 'oiac_user_name', 'oiac_user_pass', 'oiac_comp_name', 'oiac_comp_workgroup',
                     'oiac_note',)


class ComputersIsodAdmin(admin.ModelAdmin):
    """Компьютеры для работы в сети ИСОД МВД"""
    list_display = ('comp_reg_num', 'comp_mac_address', 'comp_ip_address',
                    'comp_virt_ip_address', 'comp_id_dst_file', 'comp_title_dst_file', 'comp_attestation_status',
                    'fk_prop', 'comp_note',)
    list_display_links = ('comp_reg_num', 'comp_mac_address', 'comp_ip_address',
                          'comp_virt_ip_address', 'comp_id_dst_file', 'comp_title_dst_file', 'comp_attestation_status',
                          'fk_prop', 'comp_note',)
    search_fields = ('comp_reg_num', 'comp_mac_address', 'comp_ip_address',
                     'comp_virt_ip_address', 'comp_id_dst_file', 'comp_title_dst_file', 'comp_attestation_status',
                     'comp_note',)


class DiskStorageIsodAdmin(admin.ModelAdmin):
    """Дисковые хранилища для компьютеров, подключенных к сети ИСОД МВД"""
    list_display = ('disk_reg_num', 'disk_model', 'disk_size', 'disk_factory_num', 'fk_disk_owner',
                    'fk_install_in_comp', 'disk_note',)
    list_display_links = ('disk_reg_num', 'disk_model', 'disk_size', 'disk_factory_num', 'fk_disk_owner',
                          'fk_install_in_comp', 'disk_note',)
    search_fields = ('disk_reg_num', 'disk_model', 'disk_factory_num', 'disk_note',)


class PropertyStandartsAdmin(admin.ModelAdmin):
    """Нормы положенности имущества ИЦ"""
    list_display = ('ps_name', 'ps_type', 'ps_quantity_limit', 'ps_note',)
    list_display_links = ('ps_name', 'ps_type', 'ps_quantity_limit', 'ps_note',)
    search_fields = ('ps_name', 'ps_type', 'ps_quantity_limit', 'ps_note',)


class PropertyAdmin(admin.ModelAdmin):
    """Имущество"""
    list_display = ('fk_tp', 'prop_name', 'prop_ic_num', 'prop_inventory_num', 'prop_factory_num', 'prop_unit_measure',
                    'fk_ps', 'fk_prop_owner', 'fk_cabinet_location', 'prop_date_delivery', 'prop_date_exploitation',
                    'prop_status', 'prop_date_deregistration', 'prop_note',)
    list_display_links = ('fk_tp', 'prop_name', 'prop_ic_num', 'prop_inventory_num', 'prop_factory_num', 'prop_unit_measure',
                    'fk_ps', 'fk_prop_owner', 'fk_cabinet_location', 'prop_date_delivery', 'prop_date_exploitation',
                    'prop_status', 'prop_date_deregistration', 'prop_note',)
    search_fields = ('fk_tp__tp_type', 'prop_name', 'prop_ic_num', 'prop_inventory_num', 'prop_factory_num',
                     'prop_unit_measure', 'prop_date_exploitation', 'prop_status', 'prop_note',)


class IssueOfficeProductsAdmin(admin.ModelAdmin):
    """Выдача канцелярских и иных расходных товаров"""
    list_display = ('fk_tp', 'iop_title', 'iop_quantity', 'fk_op_owner', 'iop_date_issue', 'iop_note',)
    list_display_links = ('fk_tp', 'iop_title', 'iop_quantity', 'fk_op_owner', 'iop_date_issue', 'iop_note',)
    search_fields = ('iop_title', 'iop_quantity', 'iop_date_issue', 'iop_note',)


class AccountingCryptographicSecurityAdmin(admin.ModelAdmin):
    """Учет средств криптографической защиты информации (сокр. СКЗИ)"""
    list_display = ('fk_prop', 'acs_purpose', 'acs_received_organization', 'acs_start_date', 'acs_final_date',
                    'acs_status', 'acs_note')
    list_display_links = ('fk_prop', 'acs_purpose', 'acs_received_organization', 'acs_start_date', 'acs_final_date',
                          'acs_status', 'acs_note')
    search_fields = ('acs_purpose', 'acs_received_organization', 'acs_start_date', 'acs_final_date', 'acs_status',
                     'acs_note')


class OtherNetworkPropertyAdmin(admin.ModelAdmin):
    """Иное имущество, подключенное к сети"""
    list_display = ('fk_prop', 'onp_network_type', 'onp_ip_address', 'onp_note',)
    list_display_links = ('fk_prop', 'onp_network_type', 'onp_ip_address', 'onp_note',)
    search_fields = ('fk_prop', 'onp_network_type', 'onp_ip_address', 'onp_note',)


class DepartmentsRegionalLevelAdmin(admin.ModelAdmin):
    list_display = ('drl_title', 'drl_title_area', 'fk_self_subordinate', 'drl_note')
    list_display_links = ('drl_title', 'drl_title_area', 'fk_self_subordinate', 'drl_note')
    search_fields = ('drl_title', 'drl_title_area')


admin.site.register(Cabinets, CabinetsAdmin)
admin.site.register(TypesWork, TypesWorkAdmin)
admin.site.register(Ranks, RanksAdmin)
admin.site.register(Divisions, DivisionsAdmin)
admin.site.register(DepartmentsFirst, DepartmentsFirstAdmin)
admin.site.register(DepartmentsSecond, DepartmentsSecondAdmin)
admin.site.register(Positions, PositionsAdmin)
admin.site.register(EmployeesStatus, EmployeesStatusAdmin)
admin.site.register(Employees, EmployeesAdmin)
admin.site.register(ComputersIsod, ComputersIsodAdmin)
admin.site.register(DiskStorageIsod, DiskStorageIsodAdmin)
admin.site.register(PropertyStandarts, PropertyStandartsAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(TypesProperty, TypesPropertyAdmin)
admin.site.register(IssueOfficeProducts, IssueOfficeProductsAdmin)
admin.site.register(AccountingCryptographicSecurity, AccountingCryptographicSecurityAdmin)
admin.site.register(OtherNetworkProperty, OtherNetworkPropertyAdmin)
admin.site.register(OtherInformationAboutComputers, OtherInformationAboutComputersAdmin)
admin.site.register(DepartmentsRegionalLevel, DepartmentsRegionalLevelAdmin)