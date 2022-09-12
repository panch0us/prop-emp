from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from django.db.models import CharField, Value
from django.db.models.functions import Concat
import re
import csv
import xlwt
import xlsxwriter
import datetime
from .models import Employees, DepartmentsFirst, Positions, Property, DiskStorageIsod, ComputersIsod, OtherNetworkProperty


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
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем текущего (object берется из контекста модели )
        context['my_obj'] = self.object
        # -- Имущество, закрепленное за сотрудником
        context['emp_property'] = Property.objects.filter(fk_prop_owner=context['my_obj'])
        # -- Дисковые хранилища ИСОД МВД, закрепленные за сотрудником
        context['emp_disk_storage_isod'] = DiskStorageIsod.objects.filter(fk_disk_owner=context['my_obj'])
        # -- Компьютеры сети ИСОД, закрепленные за сотрудником
        context['emp_comp_isod'] = ComputersIsod.objects.filter(fk_prop__fk_prop_owner=context['my_obj'])
        return context


class PhonebookView(LoginRequiredMixin, ListView):
    """Телефонный справочник сотрдуников"""
    model = Employees
    template_name = 'ic/phone_book.html'
    queryset = Employees.objects.filter(fk_emp_status__emp_status='Действующий')
    context_object_name = 'employees'
    # Если пользователь не авторизован, его перенаправит на страницу авторизации
    login_url = '/ic/accounts/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = DepartmentsFirst.objects.all()
        return context


class CompIsodView(LoginRequiredMixin, ListView):
    """Компьютеры для работы в сети ИСОД МВД"""
    model = ComputersIsod
    queryset = ComputersIsod.objects.all()
    template_name = 'ic/comp_isod.html'
    context_object_name = 'computers_isod'
    # Если пользователь не авторизован, его перенаправит на страницу авторизации
    login_url = '/ic/accounts/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['other_net_prop'] = OtherNetworkProperty.objects.all()
        return context


class AnalyticsIc(LoginRequiredMixin, ListView):
    """Аналитическая справка по ИЦ"""
    model = Positions
    template_name = 'ic/analytics_ic.html'
    queryset = Positions.objects.all()
    context_object_name = 'positions'
    # Если пользователь не авторизован, его перенаправит на страницу авторизации
    login_url = '/ic/accounts/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Выбираем сотрудников со статусом "Действующий"
        context['employees'] = Employees.objects.filter(fk_emp_status__emp_status='Действующий')
        return context


class DownloadListsView(LoginRequiredMixin, ListView):
    """Списки для скачивания"""
    template_name = 'ic/download_lists.html'
    model = Employees
    queryset = Employees.objects.all()
    context_object_name = 'employees_list'
    # Если пользователь не авторизован, его перенаправит на страницу авторизации
    login_url = '/ic/accounts/login/'

    def get_xlsx_emp_all(self, **kwargs):
        """
        Скачать xls файл со всеми дейсвтующими сотрудниками, ФГГС и работниками
        """
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="emp.xls"'
        employees = Employees.objects.filter(fk_emp_status__emp_status='Действующий')
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Список')

        # Стиль заголовка 
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        # Стиль даты
        date_format = xlwt.XFStyle()
        date_format.num_format_str = 'dd/mm/yyyy'

        row_num = 0
        columns = [
                'Фамилия', 
                'Имя', 
                'Отчество', 
                'День рождения', 
                'Пол', 
                'Семейное положение', 
                'С какого года в ОВД', 
                'Дата поступления на службу в ИЦ', 
                'Дата назначения на текущую должность', 
                'Вид службы', 
                'Отдел', 
                'Отделение', 
                'Полное название должности', 
                'Звание', 
                'Кабинет', 
                'Служебный телефон', 
                'Домашний телефон', 
                'Мобильный телефон', 
                'Адрес проживания', 
                'Адрес регистрации', 
                'Стаж вождения', 
                'Категория водительского удостоверения', 
                'Квалификационное звание', 
                'Дата присвоения квалификационного звания', 
                'Дата приказа о присвоении квал. звания', 
                '№ приказа о присвоении квал. звания', 
                'Год последнего повышения квалификации', 
                'Район проживания', 
                'Дата увольнения (перевода)'
                ]
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        rows = employees.values_list(
                'emp_surname', 
                'emp_name', 
                'emp_middle_name', 
                'emp_birthday', 
                'emp_gender', 
                'emp_family_status', 
                'emp_date_start_work', 
                'emp_date_start_work_ic', 
                'emp_date_start_position', 
                'fk_position__fk_types_work__tw_title', 
                'fk_position__fk_dep_first__dep_first_title', 
                'fk_position__fk_dep_second__dep_second_title', 
                'fk_position__pos_title_full', 
                'fk_rank__r_title', 
                'fk_cabinet_location__cab_num', 
                'emp_phone', 
                'emp_phone_home', 
                'emp_phone_mobile', 
                'emp_home_address', 
                'emp_home_address_reg', 
                'emp_date_driving_experience', 
                'emp_driving_license_category', 
                'emp_sport_class', 
                'emp_date_sport_class', 
                'emp_date_document_sport_class', 
                'emp_number_sport_class', 
                'emp_date_quali_upgrade', 
                'fk_depart_region_lvl__drl_title_area', 
                'emp_date_end_work'
                )

        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                # если строка подходит под '4числа-2числа-2числа', то в ексель файле ячейка форматируется как "Дата", иначе обычный формат
                regex_row = re.search(r'\b\d\d\d\d[-]\d\d[-]\d\d\b', str(row[col_num]))
                if regex_row:
                    ws.write(row_num, col_num, row[col_num], date_format)
                else:
                    ws.write(row_num, col_num, row[col_num])

        wb.save(response)
        return response

    def get_xlsx_arm_isod(self, **kwargs):
        """
        Создает файл '.xlsx' для cкачивания, включающий АРМ ИЦ сети ИСОД МВД
        """
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ARM_ISOD_IC.xlsx"'

        # Получаем все АРМ ИСОД
        arms = ComputersIsod.objects.all()
        # Получаем все МНИ
        mni =  DiskStorageIsod.objects.all()
        
        book = xlsxwriter.Workbook(response, {'in_memory': True})
        sheet = book.add_worksheet('arm')
        format_curency = book.add_format({'num_format': '$#,##0.00'})
        # Формат для включения переноса строк по символу \n 
        format_wrap = book.add_format({'text_wrap': True})
        
        columns = [
                '№ п/п',
                'Заводской номер АРМ', 
                'Модель МНИ / объем', 
                'Заводской номер МНИ', 
                'Регистрационный номер МНИ', 
                'МАС адрес сетевой карты', 
                'IP-адрес', 
                'Виртуальный IP-адрес', 
                'ID DST', 
                'ИМЯ DST', 
                'Адрес дислокации АРМ', 
                'Ф.И.О., должность пользователя', 
                'Состояние аттестации АРМ',
                ]
        row_num = 0

        # Заполняем заголовок таблицы
        for num, col in enumerate(columns):
            sheet.write(row_num, num, col)

        # Получаем конкретные строки из модели ComputersIsod
        rows = arms.values_list(
                'comp_reg_num', 
                'fk_prop__prop_factory_num', 
                'comp_mac_address', 
                'comp_ip_address', 
                'comp_virt_ip_address', 
                'comp_id_dst_file', 
                'comp_title_dst_file', 
                'fk_prop__fk_cabinet_location__cab_num', 
                'fk_prop__fk_prop_owner__emp_surname', 
                'fk_prop__fk_prop_owner__emp_name', 
                'fk_prop__fk_prop_owner__emp_middle_name', 
                'fk_prop__fk_prop_owner__fk_position__pos_title_full', 
                'comp_attestation_status',
                )
        
        # Заполняем строки таблицы
        for row in rows:
            row_num += 1
            col_num = 0

            # Заполняем столбец "№ п/п" - создается из rows(comp_reg_num) (row[0])
            sheet.write(row_num, col_num, int(row[0]))

            # Заполняем столбец "Заводской номер АРМ" - создается из rows(fk_prop__prop_factory_num) (row[1])
            col_num += 1
            sheet.write(row_num, col_num, row[1])
                
            # Заполняем столбец "Модель МНИ / объем" - создается из двух значений 'disk_model' (row_mni[0]) и 'disk_size' (row_mni[1])
            col_num += 1
            rows_mni = mni.filter(fk_install_in_comp__comp_reg_num=row[0]).values_list('disk_model', 'disk_size', 'disk_factory_num', 'disk_reg_num')
            row_mni_str = ''
            for row_mni in rows_mni:
                row_mni_str = row_mni_str + row_mni[0] + ' / ' + row_mni[1] + "; \n"
            sheet.write(row_num, col_num, str(row_mni_str), format_wrap)
                
            # Заполняем столбец "Заводской номер МНИ" - создается из значения 'disk_factory_num' (row_mni[2])
            col_num += 1
            row_mni_fact_num = ''
            for row_mni in rows_mni:
                row_mni_fact_num = row_mni_fact_num + row_mni[2] + "; \n"
            sheet.write(row_num, col_num, str(row_mni_fact_num), format_wrap)

            # Заполняем столбец "Регистрационный номер МНИ" - создается из значения 'disk_reg_num' (row_mni[3])
            col_num += 1
            row_str = ''
            for row_mni in rows_mni:
                row_str = row_str + row_mni[3] + "; \n"
            sheet.write(row_num, col_num, row_str, format_wrap)
        
            # Заполняем столбец "МАС адрес сетевой карты" - создается из rows('comp_mac_address') (row[2])
            col_num += 1
            sheet.write(row_num, col_num, row[2])

            # Заполняем столбец "IP-адрес" - создается из rows('comp_ip_address') (row[3])
            col_num += 1
            sheet.write(row_num, col_num, row[3])

            # Заполняем столбец "Виртуальный IP-адрес" - создается из rows('comp_virt_ip_address') (row[4])
            col_num += 1
            sheet.write(row_num, col_num, row[4])

            # Заполняем столбец "ID DST" - создается из rows('comp_id_dst_file') (row[5])
            col_num += 1
            sheet.write(row_num, col_num, row[5])

            # Заполняем столбец "Имя DST" - создается из rows('comp_title_dst_file') (row[6])
            col_num += 1
            sheet.write(row_num, col_num, row[6])
            
            # Заполняем столбец "Адрес дислокации АРМ" - создается из rows('fk_prop__fk_cabinet_location__cab_num') (row[7])
            col_num += 1
            sheet.write(row_num, col_num, 'г. Брянск, пр-т Ленина д. 18, кабинет № ' + str(row[7]))

            # Заполняем столбец "Ф.И.О., должность пользователя" - создается из rows(
            #   'fk_prop__fk_prop_owner__emp_surname/name/middle_name' (row[8,9,10])
            #   'fk_prop__fk_prop_owner__fk_position__pos_title_full') (row[11])
            col_num += 1
            sheet.write(row_num, col_num, str(row[8]) + ' ' + str(row[9]) + ' '+ str(row[10]) + ', ' + str(row[11]))

            # Заполняем столбец "Состояние аттестации АРМ" - создается из rows('comp_attestation_status') (row[12])
            col_num += 1
            sheet.write(row_num, col_num, row[12])

            #rows_prop = prop.filter(fk_install_in_comp__comp_reg_num=row[0]).values_list('disk_model', 'disk_size', 'disk_factory_num', 'disk_reg_num')
            #row_mni_str = ''

        # test merge cells
        #arms_concat = ComputersIsod.objects.all().annotate(full_name=Concat('comp_reg_num', Value('/ '), 'comp_ip_address', output_field=CharField()))
        #rows = arms_concat.values_list('full_name')
        
        book.close() 
        return response

#class Asd(ListView):
    """Дни рождения сотрудников в текущем месяце (ДОРАБОТАТЬ ПОСЛЕ)"""
    # current_month = datetime.now().month
#    pass
