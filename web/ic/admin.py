from django.contrib import admin
from django import forms
from django.db import models as django_models

from .models import Cabinets, TypesWork, Divisions, DepartmentsFirst, DepartmentsSecond, Positions, EmployeesStatus, \
                    Employees, ComputersIsod, DiskStorageIsod, PropertyStandarts, Property, TypesProperty, Ranks, \
                    IssueOfficeProducts, AccountingCryptographicSecurity, OtherNetworkProperty, \
                    OtherInformationAboutComputers, DepartmentsRegionalLevel, EmployeesAutomoto, EmployeesChildren, \
                    EmployeesSpouse, EmployeesWeapons, TimeKeepingDoc, TimeKeeping, PropertyAction, \
                    InformationSystem, InformationSystemProperty

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
    autocomplete_fields = ('fk_div',)


class DepartmentsSecondAdmin(admin.ModelAdmin):
    """Отделения"""
    list_display = ('dep_second_title', 'fk_dep_first',)
    list_display_links = ('dep_second_title', 'fk_dep_first',)
    search_fields = ('dep_second_title',)
    autocomplete_fields = ('fk_dep_first',)


class PositionsAdmin(admin.ModelAdmin):
    """Должности"""
    list_display = ('pos_title', 'fk_dep_second', 'fk_dep_first', 'fk_division', 'pos_quantity', 'fk_types_work')
    list_display_links = ('pos_title', 'fk_dep_second', 'fk_dep_first', 'fk_division', 'pos_quantity', 'fk_types_work')
    search_fields = ('pos_title', 'pos_title_full', 'pos_quantity',)
    autocomplete_fields = ('fk_dep_second', 'fk_dep_first', 'fk_division', 'fk_types_work')


class EmployeesStatusAdmin(admin.ModelAdmin):
    """Статусы сотруднков"""
    list_display = ('emp_status',)
    list_display_links = ('emp_status',)
    search_fields = ('emp_status',)


class EmployeesSpouseInline(admin.TabularInline):
    model = EmployeesSpouse
    extra = 1
    fields = ('emps_surname', 'emps_name', 'emps_middle_name', 'emps_birthday')
    verbose_name_plural = 'Супруги'


class EmployeesChildrenInline(admin.TabularInline):
    model = EmployeesChildren
    extra = 1
    fields = (
        'empc_surname', 'empc_name', 'empc_middle_name', 'empc_birthday', 'empc_gender',
        'empc_home_address', 'empc_study_place', 'empc_mobile_phone',
    )
    verbose_name_plural = 'Дети'


class EmployeesAutomotoInline(admin.TabularInline):
    model = EmployeesAutomoto
    fk_name = 'fk_auto_owner'
    extra = 1
    fields = ('empa_model', 'empa_reg_num', 'empa_owner_type', 'empa_note')
    verbose_name_plural = 'Личный автотранспорт'
    formfield_overrides = {
        django_models.TextField: {'widget': forms.Textarea(attrs={'rows': 2, 'cols': 70})},
    }


class EmployeesWeaponsInline(admin.TabularInline):
    model = EmployeesWeapons
    fk_name = 'fk_weapon_owner'
    extra = 1
    fields = (
        'empw_model', 'empw_caliber', 'empw_serial_number', 'empw_weapon_permit',
        'empw_weapon_permit_serial_number', 'empw_start_weapon_permit',
        'empw_end_weapon_permit', 'empw_type_permit', 'empw_note',
    )
    verbose_name_plural = 'Личное оружие'
    formfield_overrides = {
        django_models.TextField: {'widget': forms.Textarea(attrs={'rows': 2, 'cols': 70})},
    }


class EmployeesAdmin(admin.ModelAdmin):
    """Сотрудники"""
    list_display = ('emp_surname', 'emp_name', 'emp_middle_name', 'fk_emp_status', 'fk_position',
                    'emp_phone', 'emp_phone_home', 'emp_phone_mobile',
                    'emp_home_address', 'fk_depart_region_lvl', 'emp_sport_class', 'emp_date_sport_class',
                    'emp_date_document_sport_class', 'emp_number_sport_class', 'emp_note', 'emp_url')
    list_display_links = ('emp_surname', 'emp_name', 'emp_middle_name', 'fk_emp_status', 'fk_position',
                    'emp_phone', 'emp_phone_home', 'emp_phone_mobile',
                    'emp_home_address', 'fk_depart_region_lvl', 'emp_sport_class', 'emp_date_sport_class',
                    'emp_date_document_sport_class', 'emp_number_sport_class', 'emp_note',)
    search_fields = ('emp_surname', 'emp_name', 'emp_middle_name', 'emp_note',)
    list_filter = ('fk_position__fk_dep_first',)
    autocomplete_fields = ('fk_emp_status', 'fk_position', 'fk_rank', 'fk_cabinet_location',
                           'fk_depart_region_lvl')
    inlines = (EmployeesSpouseInline, EmployeesChildrenInline, EmployeesAutomotoInline, EmployeesWeaponsInline)

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
    autocomplete_fields = ('fk_prop',)


class ComputersIsodAdmin(admin.ModelAdmin):
    """Компьютеры для работы в сети ИСОД МВД"""
    list_per_page = 9999 # Отключаем пагинацию
    list_display = ('comp_reg_num', 'comp_mac_address', 'comp_ip_address',
                    'comp_virt_ip_address', 'comp_id_dst_file', 'comp_title_dst_file', 'comp_attestation_status',
                    'fk_prop', 'comp_note',)
    list_display_links = ('comp_reg_num', 'comp_mac_address', 'comp_ip_address',
                          'comp_virt_ip_address', 'comp_id_dst_file', 'comp_title_dst_file', 'comp_attestation_status',
                          'fk_prop', 'comp_note',)
    search_fields = ('comp_reg_num', 'comp_mac_address', 'comp_ip_address',
                     'comp_virt_ip_address', 'comp_id_dst_file', 'comp_title_dst_file', 'comp_attestation_status',
                     'comp_note',)
    autocomplete_fields = ('fk_prop', 'fk_admin')


class DiskStorageIsodAdmin(admin.ModelAdmin):
    """Дисковые хранилища для компьютеров, подключенных к сети ИСОД МВД"""
    list_per_page = 9999 # Отключаем пагинацию
    list_display = ('disk_reg_num', 'disk_model', 'disk_size', 'disk_factory_num', 'fk_disk_owner',
                    'fk_install_in_comp', 'disk_note',)
    list_display_links = ('disk_reg_num', 'disk_model', 'disk_size', 'disk_factory_num', 'fk_disk_owner',
                          'fk_install_in_comp', 'disk_note',)
    search_fields = ('disk_reg_num', 'disk_model', 'disk_factory_num', 'disk_note',)
    autocomplete_fields = ('fk_disk_owner', 'fk_install_in_comp')


class PropertyStandartsAdmin(admin.ModelAdmin):
    """Нормы положенности имущества ИЦ"""
    list_display = ('ps_name', 'ps_type', 'ps_quantity_limit', 'ps_note',)
    list_display_links = ('ps_name', 'ps_type', 'ps_quantity_limit', 'ps_note',)
    search_fields = ('ps_name', 'ps_type', 'ps_quantity_limit', 'ps_note',)


class PropertyActionInline(admin.TabularInline):
    model = PropertyAction
    extra = 1
    fields = ('action_text', 'action_date')
    formfield_overrides = {
        django_models.TextField: {'widget': forms.Textarea(attrs={'rows': 2, 'cols': 70})},
    }


class PropertyInformationSystemInline(admin.TabularInline):
    model = InformationSystemProperty
    extra = 1
    fields = ('fk_information_system', 'isp_description')
    autocomplete_fields = ('fk_information_system',)
    verbose_name_plural = 'Используется в информационных системах'
    formfield_overrides = {
        django_models.TextField: {'widget': forms.Textarea(attrs={'rows': 2, 'cols': 70})},
    }


class InformationSystemPropertyInline(admin.TabularInline):
    model = InformationSystemProperty
    extra = 1
    fields = ('fk_property', 'isp_description')
    autocomplete_fields = ('fk_property',)
    formfield_overrides = {
        django_models.TextField: {'widget': forms.Textarea(attrs={'rows': 2, 'cols': 70})},
    }


class PropertyAdmin(admin.ModelAdmin):
    """Имущество"""
    fieldsets = (
        (None, {
            'fields': (
                'fk_tp', 'fk_ps', 'prop_name', 'prop_ic_num',
                'prop_inventory_num', 'prop_factory_num', 'prop_unit_measure', 'fk_prop_owner',
                'fk_cabinet_location', 'prop_date_delivery', 'prop_date_exploitation',
                'prop_warranty_until',
            )
        }),
        ('Назначение и размещение', {
            'fields': (
                'prop_purpose', 'fk_installed_in',
            )
        }),
        (None, {
            'fields': (
                'prop_status', 'prop_date_deregistration', 'prop_note',
            )
        }),
    )
    list_display = ('fk_tp', 'prop_name', 'prop_ic_num', 'prop_inventory_num', 'prop_factory_num', 'prop_unit_measure',
                    'fk_ps', 'prop_purpose', 'fk_installed_in', 'fk_prop_owner', 'fk_cabinet_location', 'prop_date_delivery',
                    'prop_date_exploitation', 'prop_warranty_until', 'prop_status', 'prop_date_deregistration', 'prop_note',)
    list_display_links = ('fk_tp', 'prop_name', 'prop_ic_num', 'prop_inventory_num', 'prop_factory_num', 'prop_unit_measure',
                    'fk_ps', 'prop_purpose', 'fk_installed_in', 'fk_prop_owner', 'fk_cabinet_location', 'prop_date_delivery',
                    'prop_date_exploitation', 'prop_warranty_until', 'prop_status', 'prop_date_deregistration', 'prop_note',)
    search_fields = ('fk_tp__tp_type', 'prop_name', 'prop_ic_num', 'prop_inventory_num', 'prop_factory_num',
                     'prop_unit_measure', 'prop_date_exploitation', 'prop_status', 'prop_note',
                     'fk_installed_in__prop_name', 'fk_installed_in__prop_ic_num',)
    
    autocomplete_fields = ('fk_tp', 'fk_ps', 'fk_prop_owner', 'fk_cabinet_location', 'fk_installed_in')
    inlines = (PropertyActionInline, PropertyInformationSystemInline,)


class InformationSystemAdmin(admin.ModelAdmin):
    """Информационные системы"""
    fieldsets = (
        (None, {
            'fields': (
                'is_name', 'is_date_commissioning',
                'is_security_level', 'is_security_class',
                'is_threat_model', 'is_certificate',
                'is_access_permit_system',
                'is_technological_process_description',
                'is_security_admin_instruction',
                'is_user_instruction', 'is_password_protection_instruction',
                'is_antivirus_instruction', 'is_confidential_information_list',
                'is_room_access_instruction', 'is_access_rights_regulation',
                'is_server_room_access_persons', 'is_date_decommissioning',
            )
        }),
    )
    list_display = ('is_name', 'is_date_commissioning', 'is_security_level',
                    'is_security_class', 'is_date_decommissioning',)
    list_display_links = ('is_name', 'is_date_commissioning', 'is_security_level',
                          'is_security_class', 'is_date_decommissioning',)
    search_fields = ('is_name', 'is_date_commissioning', 'is_security_level', 'is_security_class')
    inlines = (InformationSystemPropertyInline,)
    formfield_overrides = {
        django_models.TextField: {'widget': forms.Textarea(attrs={'rows': 2, 'cols': 90})},
    }


class IssueOfficeProductsAdmin(admin.ModelAdmin):
    """Выдача канцелярских и иных расходных товаров"""
    list_display = ('fk_tp', 'iop_title', 'iop_quantity', 'fk_op_owner', 'iop_date_issue', 'iop_note',)
    list_display_links = ('fk_tp', 'iop_title', 'iop_quantity', 'fk_op_owner', 'iop_date_issue', 'iop_note',)
    search_fields = ('iop_title', 'iop_quantity', 'iop_date_issue', 'iop_note',)
    autocomplete_fields = ('fk_tp', 'fk_op_owner')


class AccountingCryptographicSecurityAdmin(admin.ModelAdmin):
    """Учет средств криптографической защиты информации (сокр. СКЗИ)"""
    list_display = ('fk_prop', 'acs_purpose', 'acs_received_organization', 'acs_start_date', 'acs_final_date',
                    'acs_status', 'acs_note')
    list_display_links = ('fk_prop', 'acs_purpose', 'acs_received_organization', 'acs_start_date', 'acs_final_date',
                          'acs_status', 'acs_note')
    search_fields = ('acs_purpose', 'acs_received_organization', 'acs_start_date', 'acs_final_date', 'acs_status',
                     'acs_note')
    autocomplete_fields = ('fk_prop',)


class OtherNetworkPropertyAdmin(admin.ModelAdmin):
    """Иное имущество, подключенное к сети"""
    list_display = ('fk_prop', 'onp_network_type', 'onp_ip_address', 'onp_virt_ip_address', 'onp_note',)
    list_display_links = ('fk_prop', 'onp_network_type', 'onp_ip_address', 'onp_virt_ip_address', 'onp_note',)
    search_fields = ('fk_prop__prop_name', 'fk_prop__prop_ic_num', 'onp_network_type', 'onp_ip_address',
                     'onp_virt_ip_address', 'onp_note',)
    autocomplete_fields = ('fk_prop',)


class DepartmentsRegionalLevelAdmin(admin.ModelAdmin):
    list_display = ('drl_title', 'drl_title_area', 'fk_self_subordinate', 'drl_note')
    list_display_links = ('drl_title', 'drl_title_area', 'fk_self_subordinate', 'drl_note')
    search_fields = ('drl_title', 'drl_title_area')
    autocomplete_fields = ('fk_self_subordinate',)


class EmployeesAutomotoAdmin(admin.ModelAdmin):
    list_display = ('fk_auto_owner', 'empa_model', 'empa_reg_num',)
    list_display_links = ('fk_auto_owner',)
    search_fields = ('fk_auto_owner__emp_surname', 'empa_model',)
    autocomplete_fields = ('fk_auto_owner',)


class EmployeesChildrenAdmin(admin.ModelAdmin):
    list_display = ('fk_emp', 'empc_surname', 'empc_name', 'empc_middle_name', 'empc_birthday',
                    'empc_gender', 'empc_home_address', 'empc_study_place', 'empc_mobile_phone',)
    list_display_links = ('fk_emp',)
    search_fields = ('fk_emp__emp_surname', 'fk_emp__emp_name', 'fk_emp__emp_middle_name',
                     'empc_surname', 'empc_name', 'empc_middle_name', 'empc_home_address',
                     'empc_study_place', 'empc_mobile_phone',)
    autocomplete_fields = ('fk_emp',)


class EmployeesSpouseAdmin(admin.ModelAdmin):
    list_display = ('fk_emp', 'emps_surname', 'emps_name', 'emps_middle_name', 'emps_birthday',)
    list_display_links = ('fk_emp',)
    search_fields = ('fk_emp__emp_surname',)
    autocomplete_fields = ('fk_emp',)


class EmployeesWeaponsAdmin(admin.ModelAdmin):
    list_display = ('fk_weapon_owner', 'empw_model', 'empw_caliber', 'empw_serial_number',)
    list_display_links = ('fk_weapon_owner',)
    search_fields = ('fk_weapon_owner__emp_surname',)
    autocomplete_fields = ('fk_weapon_owner',)


class TimeKeepingDocAdmin(admin.ModelAdmin):
    list_display = ('tkd_doc_reg_num', 'tkd_date', 'tkd_doc_name', 'tkd_file',)
    list_display_links = ('tkd_doc_reg_num',)
    search_fields = ('tkd_doc_reg_num', 'tkd_date', 'tkd_doc_name',)

class TimeKeepingAdmin(admin.ModelAdmin):
    list_display = ('fk_emp_name', 'fk_doc_reg_num', 'tk_quantity_hours_all',) 
    list_display_links = ('fk_emp_name',)
    search_fields = ('fk_emp_name__emp_surname',)
    autocomplete_fields = ('fk_emp_name', 'fk_doc_reg_num')


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
admin.site.register(InformationSystem, InformationSystemAdmin)
admin.site.register(TypesProperty, TypesPropertyAdmin)
admin.site.register(IssueOfficeProducts, IssueOfficeProductsAdmin)
admin.site.register(AccountingCryptographicSecurity, AccountingCryptographicSecurityAdmin)
admin.site.register(OtherNetworkProperty, OtherNetworkPropertyAdmin)
admin.site.register(OtherInformationAboutComputers, OtherInformationAboutComputersAdmin)
admin.site.register(DepartmentsRegionalLevel, DepartmentsRegionalLevelAdmin)
admin.site.register(EmployeesAutomoto, EmployeesAutomotoAdmin)
admin.site.register(EmployeesChildren, EmployeesChildrenAdmin)
admin.site.register(EmployeesSpouse, EmployeesSpouseAdmin)
admin.site.register(EmployeesWeapons, EmployeesWeaponsAdmin)
admin.site.register(TimeKeepingDoc, TimeKeepingDocAdmin)
admin.site.register(TimeKeeping, TimeKeepingAdmin)

