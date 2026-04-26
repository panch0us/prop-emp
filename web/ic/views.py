from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from django.shortcuts import redirect
from django.db.models import CharField, Value, Q
from django.db.models.functions import Concat
import re
import csv
import xlwt
import xlsxwriter
from datetime import date, datetime, timedelta
from .models import Employees, DepartmentsFirst, Positions, Property, DiskStorageIsod, ComputersIsod, OtherInformationAboutComputers, OtherNetworkProperty, EmployeesAutomoto, EmployeesWeapons, EmployeesSpouse, EmployeesChildren, TimeKeepingDoc, TimeKeeping, InformationSystem


def toggle_theme(request):
    """Переключает светлую/темную тему сайта и запоминает выбор в сессии."""
    current_theme = request.session.get('site_theme', 'dark')
    request.session['site_theme'] = 'light' if current_theme == 'dark' else 'dark'
    return redirect(request.META.get('HTTP_REFERER', '/ic/'))


class EmployeesView(LoginRequiredMixin, ListView):
    """Список сотрудников, подставляет к названию модели _list (НЕ ЗАДЕЙСТВОВАН!)"""
    model               = Employees
    queryset            = Employees.objects.all()
    # current_month = datetime.now().month
    context_object_name = 'employees_list'
    # Если пользователь не авторизован, его перенаправит на страницу авторизации
    login_url           = '/ic/accounts/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        employees = Employees.objects.filter(emp_birthday__isnull=False).select_related('fk_position')
        birthday_rows = []

        for employee in employees:
            try:
                birthday_this_year = employee.emp_birthday.replace(year=today.year)
            except ValueError:
                birthday_this_year = date(today.year, 2, 28)
            if birthday_this_year < today:
                try:
                    birthday_this_year = employee.emp_birthday.replace(year=today.year + 1)
                except ValueError:
                    birthday_this_year = date(today.year + 1, 2, 28)

            days_left = (birthday_this_year - today).days
            if days_left <= 3:
                birthday_rows.append({
                    'employee': employee,
                    'birthday': birthday_this_year,
                    'days_left': days_left,
                })

        birthday_rows.sort(key=lambda item: (item['days_left'], item['employee'].emp_surname))
        context['birthdays_today'] = [item for item in birthday_rows if item['days_left'] == 0]
        context['birthdays_soon'] = [item for item in birthday_rows if 0 < item['days_left'] <= 3]
        return context


class EmployeesDetailView(LoginRequiredMixin, DetailView):
    """Полное описание сотрудника по url (slug)"""
    model                                   = Employees
    slug_field                              = "emp_url"
    # Если пользователь не авторизован, его перенаправит на страницу авторизации
    login_url                               = '/ic/accounts/login/'
    def get_context_data(self, **kwargs):
        context                             = super().get_context_data(**kwargs)
        # Получаем текущего (object берется из контекста модели )
        context['my_obj']                   = self.object
        # -- Имущество, закрепленное за сотрудником
        context['emp_property']             = Property.objects.filter(fk_prop_owner=context['my_obj'])
        # -- Дисковые хранилища ИСОД МВД, закрепленные за сотрудником
        context['emp_disk_storage_isod']    = DiskStorageIsod.objects.filter(fk_disk_owner=context['my_obj'])
        # -- Компьютеры сети ИСОД, закрепленные за сотрудником
        context['emp_comp_isod']            = ComputersIsod.objects.filter(fk_prop__fk_prop_owner=context['my_obj'])
        # -- Учет времени: переработка
        context['time_keeping']             = TimeKeeping.objects.filter(fk_emp_name=context['my_obj'])
        return context


class PhonebookView(LoginRequiredMixin, ListView):
    """Телефонный справочник сотрдуников"""
    model               = Employees
    template_name       = 'ic/phone_book.html'
    queryset            = Employees.objects.filter(fk_emp_status__emp_status='Действующий')
    context_object_name = 'employees'
    # Если пользователь не авторизован, его перенаправит на страницу авторизации
    login_url           = '/ic/accounts/login/'

    def get_context_data(self, **kwargs):
        context                 = super().get_context_data(**kwargs)
        context['departments']  = DepartmentsFirst.objects.all()
        return context


class CompIsodView(LoginRequiredMixin, ListView):
    """Компьютеры для работы в сети ИСОД МВД"""
    model               = ComputersIsod
    #queryset           = ComputersIsod.objects.all() # 02.11.2024 в разделе компьютеры сети ИСОД выводятся все АРМ, в том числе и исключенные
    queryset            = ComputersIsod.objects.filter(~Q(comp_attestation_status='Исключен')) #02.11.2024 в разделе компьютеры сети ИСОД выводятся АРМ за исключением исключенных
    template_name       = 'ic/comp_isod.html'
    context_object_name = 'computers_isod'
    # Если пользователь не авторизован, его перенаправит на страницу авторизации
    login_url           = '/ic/accounts/login/'

    def get_context_data(self, **kwargs):
        context                     = super().get_context_data(**kwargs)
        context['other_net_prop']   = OtherNetworkProperty.objects.all()
        return context


class AnalyticsIc(LoginRequiredMixin, ListView):
    """Аналитическая справка по ИЦ"""
    model               = Positions
    template_name       = 'ic/analytics_ic.html'
    queryset            = Positions.objects.all()
    context_object_name = 'positions'
    # Если пользователь не авторизован, его перенаправит на страницу авторизации
    login_url           = '/ic/accounts/login/'

    def get_context_data(self, **kwargs):
        context                 = super().get_context_data(**kwargs)
        # Выбираем сотрудников со статусом "Действующий"
        context['employees']    = Employees.objects.filter(fk_emp_status__emp_status='Действующий')
        return context


class DownloadListsView(LoginRequiredMixin, ListView):
    """Списки для скачивания"""
    template_name       = 'ic/download_lists.html'
    model               = Employees
    queryset            = Employees.objects.all()
    context_object_name = 'employees_list'
    # Если пользователь не авторизован, его перенаправит на страницу авторизации
    login_url           = '/ic/accounts/login/'

    def get_xlsx_emp_all(self, **kwargs):
        """
        Скачать xls файл со всеми дейсвтующими сотрудниками, ФГГС и работниками
        """
        response                        = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="emp.xls"'
        employees                       = Employees.objects.filter(fk_emp_status__emp_status='Действующий')
        # Все автомото сотрудников
        emp_auto_moto                   = EmployeesAutomoto.objects.all()

        wb                              = xlwt.Workbook(encoding='utf-8')
        ws                              = wb.add_sheet('Список')
        
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
                'Дата увольнения (перевода)',
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
                'emp_date_end_work',
                )

        rows_concat = employees.values_list('emp_surname',)

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


    def get_xlsx_emp_all_new(self, **kwargs):
        """
        Создает файл '.xlsx' для cкачивания, список сотрудников
        """
        response                        = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="emp.xlsx"'

        # Получаем всех сотрудников
        emps                            = Employees.objects.all()
        
        book                            = xlsxwriter.Workbook(response, {'in_memory': True})
        sheet                           = book.add_worksheet('emp')
        format_curency                  = book.add_format({'num_format': '$#,##0.00'})
        # Формат для включения переноса строк по символу \n 
        format_wrap                     = book.add_format({'text_wrap': True})
        # Формат для корректного отображения даты
        format_date                     = book.add_format({'num_format': 'dd/mm/yyyy'})
        
        columns = [
                'Фамилия', 
                'Имя', 
                'Отчество',
                'ФИО',
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
                'Должность и звание',
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
                'Статус',
                'Дата увольнения (перевода)',
                ]

        row_num = 0

        # Заполняем заголовок таблицы
        for num, col in enumerate(columns):
            sheet.write(row_num, num, col)

        # Получаем конкретные строки из модели ComputersIsod
        rows = emps.values_list(
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
                'fk_emp_status__emp_status',
                'emp_date_end_work',
                )
        
        # Заполняем строки таблицы
        for row in rows:
            row_num += 1
            col_num = 0

            # Заполняем столбец "Фамилия" - создается из rows(comp_reg_num) (row[0])
            sheet.write(row_num, col_num, row[0])

            # Заполняем столбец "Имя" - создается из rows(fk_prop__prop_factory_num) (row[1])
            col_num += 1
            sheet.write(row_num, col_num, row[1])
                
            # Заполняем столбец "Отчество" - создается из двух значений 'disk_model' (row_mni[0]) и 'disk_size' (row_mni[1])
            col_num += 1
            sheet.write(row_num, col_num, row[2])
            
            # ФИО
            col_num += 1
            fio= row[0] + ' ' + row[1] + ' ' + row[2] 
            sheet.write(row_num, col_num, str(fio), format_wrap)

            #Дата рождения
            col_num += 1
            sheet.write(row_num, col_num, row[3], format_date)

            # Пол
            col_num += 1
            sheet.write(row_num, col_num, row[4])

            # Семейное положение
            col_num += 1
            sheet.write(row_num, col_num, row[5])

            # С какого года в ОВД
            col_num += 1
            sheet.write(row_num, col_num, row[6])

            # Дата поступления на службу в ИЦ
            col_num += 1
            sheet.write(row_num, col_num, row[7], format_date)

            # Дата назначения на текущую должность
            col_num += 1
            sheet.write(row_num, col_num, row[8], format_date)

            # Вид службы
            col_num += 1
            sheet.write(row_num, col_num, row[9])

            # Отдел
            col_num += 1
            sheet.write(row_num, col_num, row[10])

            # Отделение
            col_num += 1
            sheet.write(row_num, col_num, row[11])

            # Полное название должности
            col_num += 1
            sheet.write(row_num, col_num, row[12])

            # Звание
            col_num += 1
            sheet.write(row_num, col_num, row[13])

            # Должность + звание
            col_num += 1
            rank = str(row[13])
            if rank == 'None':
                rank = ''
            else:
                rank = ', ' + rank

            position_and_rank = str(row[12]) + rank
            sheet.write(row_num, col_num, position_and_rank)
            
            # Кабинет
            col_num += 1
            sheet.write(row_num, col_num, row[14])

            # Служебный телефон
            col_num += 1
            sheet.write(row_num, col_num, row[15])

            # Домашний телефон
            col_num += 1
            sheet.write(row_num, col_num, row[16])

            # Мобильный телефон
            col_num += 1
            sheet.write(row_num, col_num, row[17])

            # Адрес проживания
            col_num += 1
            sheet.write(row_num, col_num, row[18])

            # Адрес регистрации   
            col_num += 1
            sheet.write(row_num, col_num, row[19])

            # Стаж вождения
            col_num += 1
            sheet.write(row_num, col_num, row[20])

            # Категория водительского удостоверения
            col_num += 1
            sheet.write(row_num, col_num, row[21])

            # Квалификационное звание
            col_num += 1
            sheet.write(row_num, col_num, row[22])

            #Дата присвоения квалификационного звания 
            col_num += 1
            sheet.write(row_num, col_num, row[23], format_date)

            # Дата приказа о присвоении квал. звания
            col_num += 1
            sheet.write(row_num, col_num, row[24], format_date)

            # № приказа о присвоении квал. звания
            col_num += 1
            sheet.write(row_num, col_num, row[25])

            # Год последнего повышения квалификации
            col_num += 1
            sheet.write(row_num, col_num, row[26])

            # Район проживания
            col_num += 1
            sheet.write(row_num, col_num, row[27])
            
            # Статус
            col_num += 1
            sheet.write(row_num, col_num, row[28])

            # Дата увольнения (перевода)
            col_num += 1
            sheet.write(row_num, col_num, row[29], format_date)

        
        book.close()
        return response

    def get_xlsx_arm_isod(self, **kwargs):
        """
        Создает файл '.xlsx' для cкачивания, включающий АРМ ИЦ сети ИСОД МВД
        """
        response                        = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ARM_ISOD_IC.xlsx"'

        # Получаем все АРМ ИСОД
        arms                            = ComputersIsod.objects.all()
        # Получаем все МНИ
        mni                             =  DiskStorageIsod.objects.all()
        # Получаем все Иная информация о вычислительной технике
        oiac                            = OtherInformationAboutComputers.objects.all()

        book                            = xlsxwriter.Workbook(response, {'in_memory': True})
        sheet                           = book.add_worksheet('arm')
        format_curency                  = book.add_format({'num_format': '$#,##0.00'})
        # Формат для включения переноса строк по символу \n 
        format_wrap                     = book.add_format({'text_wrap': True})
        
        columns = [
                '№ п/п',
                'Заводской номер АРМ',
                'Инвентарный номер АРМ',
                'Тип',
                'Тип АРМ',
                'Модель МНИ / объем', 
                'Заводской номер МНИ', 
                'Регистрационный номер МНИ', 
                'МАС адрес сетевой карты', 
                'IP-адрес', 
                'Виртуальный IP-адрес',
                'Операционная система',
                'Администратор безопасности',
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
                'fk_prop__prop_inventory_num',
                'comp_type',
                'comp_type_2',
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
                'fk_prop__prop_id',
                'fk_admin__emp_surname',
                'fk_admin__emp_name',
                'fk_admin__emp_middle_name',
                'comp_os',
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
                
            # Заполняем столбец "Инвентарный номер АРМ" - создается из rows(fk_prop__prop_inventory_num) (row[2])
            col_num += 1
            sheet.write(row_num, col_num, row[2])

            # Заполняем столбец "Тип" - создается из rows(comp_type) (row[3])
            col_num += 1
            sheet.write(row_num, col_num, row[3])

            # Заполняем столбец "Тип АРМ" - создается из rows(comp_type_2) (row[4])
            col_num += 1
            sheet.write(row_num, col_num, row[4])

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
        
            # Заполняем столбец "МАС адрес сетевой карты" - создается из rows('comp_mac_address') (row[5])
            col_num += 1
            sheet.write(row_num, col_num, row[5])

            # Заполняем столбец "IP-адрес" - создается из rows('comp_ip_address') (row[6])
            col_num += 1
            sheet.write(row_num, col_num, row[6])

            # Заполняем столбец "Виртуальный IP-адрес" - создается из rows('comp_virt_ip_address') (row[7])
            col_num += 1
            sheet.write(row_num, col_num, row[7])

            # Заполняем столбец "Операционная система" - создается из rows(comp_os) (row[21])
            col_num += 1
            sheet.write(row_num, col_num, row[20])
            #rows_oiac = oiac.filter(fk_prop__prop_id=row[16]).values_list('oiac_os')
            #row_oiac_str = ''
            #for row_oiac in rows_oiac:
            #    row_oiac_str = row_oiac_str + row_oiac[0]
            #sheet.write(row_num, col_num, str(row_oiac_str), format_wrap)
            
            # Заполняем столбец "Администратор безопасности" - создается из rows('fk_admin') (row[16])
            col_num += 1
            sheet.write(row_num, col_num, str(row[17]) + ' ' + str(row[18]) + ' ' + str(row[19]))

            # Заполняем столбец "ID DST" - создается из rows('comp_id_dst_file') (row[8])
            col_num += 1
            sheet.write(row_num, col_num, row[8])

            # Заполняем столбец "Имя DST" - создается из rows('comp_title_dst_file') (row[9])
            col_num += 1
            sheet.write(row_num, col_num, row[9])
            
            # Заполняем столбец "Адрес дислокации АРМ" - создается из rows('fk_prop__fk_cabinet_location__cab_num') (row[10])
            col_num += 1
            address_comp = 'г. Брянск, ул. Советская д. 102, кабинет № ' + str(row[10])
            sheet.write(row_num, col_num, address_comp if row[10] != None else '')

            # Заполняем столбец "Ф.И.О., должность пользователя" - создается из rows(
            #   'fk_prop__fk_prop_owner__emp_surname/name/middle_name' (row[11,12,13])
            #   'fk_prop__fk_prop_owner__fk_position__pos_title_full') (row[14])
            col_num += 1
            sheet.write(row_num, col_num, str(row[11] + ' '  if row[11] != None else '') + \
                                          str(row[12] + ' '  if row[12] != None else '') + \
                                          str(row[13] + ', ' if row[13] != None else '') + (', ' if row[14] != None else '') + \
                                          str(row[14] if row[14] != None else ''))

            # Заполняем столбец "Состояние аттестации АРМ" - создается из rows('comp_attestation_status') (row[15])
            col_num += 1
            sheet.write(row_num, col_num, row[15])

        book.close() 
        return response


    def get_xlsx_property(self, **kwargs):
        """
        Создает файл '.xlsx' для cкачивания, включающий имущество
        """
        response                        = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Property_IC.xlsx"'

        # Получаем все имущество
        properties = Property.objects.select_related(
            'fk_tp', 'fk_ps', 'fk_prop_owner', 'fk_cabinet_location', 'fk_installed_in'
        ).prefetch_related('property_actions')

        book                            = xlsxwriter.Workbook(response, {'in_memory': True})
        sheet                           = book.add_worksheet('property')
        format_curency                  = book.add_format({'num_format': '$#,##0.00'})
        # Формат для включения переноса строк по символу \n
        format_wrap                     = book.add_format({'text_wrap': True})
        # Формат для корректного отображения даты
        format_date                     = book.add_format({'num_format': 'dd/mm/yyyy'})

        columns = [
                '№ id',
                'Вид имущества внутренний',
                'Вид имущества по нормам положенности',
                'Наименование имущества',
                'Номер учета ИЦ',
                'Номер учета УМВД (инв.№)',
                'Заводской / серийный номер',
                'Единица измерения',
                'Владелец имущества',
                'Кабинет',
                'Дата поставки',
                'Дата выдачи',
                'Назначение',
                'Установлено в',
                'Гарантия',
                'Состояние имущества',
                'Дата списания',
                'Действия с имуществом',
                'Примечание',
                ]
        row_num = 0

        # Заполняем заголовок таблицы
        for num, col in enumerate(columns):
            sheet.write(row_num, num, col)

        # Заполняем строки таблицы
        for prop in properties:
            row_num += 1
            col_num = 0

            # Заполняем столбец "№ id"
            sheet.write(row_num, col_num, int(prop.prop_id))

            # Заполняем столбец "Вид имущества внутренний"
            col_num += 1
            sheet.write(row_num, col_num, str(prop.fk_tp) if prop.fk_tp else '')

            # Заполняем столбец "Вид имущества по нормам положенности"
            col_num += 1
            sheet.write(row_num, col_num, str(prop.fk_ps) if prop.fk_ps else '')

            # Заполняем столбец "Наименование имущества"
            col_num += 1
            sheet.write(row_num, col_num, prop.prop_name)

            # Заполняем столбец "Номер учета ИЦ"
            col_num += 1
            sheet.write(row_num, col_num, prop.prop_ic_num)

            # Заполняем столбец "Номер учета УМВД (инв.№)"
            col_num += 1
            sheet.write(row_num, col_num, prop.prop_inventory_num)

            # Заполняем столбец "Заводской / серийный номер"
            col_num += 1
            sheet.write(row_num, col_num, prop.prop_factory_num)

            # Заполняем столбец "Единица измерения"
            col_num += 1
            sheet.write(row_num, col_num, prop.prop_unit_measure)

            # Заполняем столбец "Владелец имущества"
            col_num += 1
            owner = prop.fk_prop_owner
            if owner:
                owner_str = f"{owner.emp_surname} {owner.emp_name} {owner.emp_middle_name}".strip()
            else:
                owner_str = ''
            sheet.write(row_num, col_num, owner_str)

            # Заполняем столбец "Кабинет"
            col_num += 1
            sheet.write(row_num, col_num, str(prop.fk_cabinet_location) if prop.fk_cabinet_location else '')

            # Заполняем столбец "Дата поставки"
            col_num += 1
            sheet.write(row_num, col_num, prop.prop_date_delivery, format_date)

            # Заполняем столбец "Дата выдачи"
            col_num += 1
            sheet.write(row_num, col_num, prop.prop_date_exploitation, format_date)

            # Заполняем столбец "Назначение"
            col_num += 1
            sheet.write(row_num, col_num, prop.prop_purpose)

            # Заполняем столбец "Установлено в"
            col_num += 1
            if prop.fk_installed_in:
                installed_in_str = f"{prop.fk_installed_in.prop_name} (№{prop.fk_installed_in.prop_ic_num})"
            else:
                installed_in_str = ''
            sheet.write(row_num, col_num, installed_in_str)

            # Заполняем столбец "Гарантия"
            col_num += 1
            sheet.write(row_num, col_num, prop.prop_warranty_until, format_date)

            # Заполняем столбец "Состояние имущества"
            col_num += 1
            sheet.write(row_num, col_num, prop.prop_status)

            # Заполняем столбец "Дата списания"
            col_num += 1
            sheet.write(row_num, col_num, prop.prop_date_deregistration, format_date)

            # Заполняем столбец "Действия с имуществом"
            col_num += 1
            actions = []
            for action in prop.property_actions.all():
                action_text = action.action_text or ''
                if action.action_date:
                    action_text = f"{action_text} {action.action_date.strftime('%d.%m.%Y')}"
                actions.append(action_text.strip())
            sheet.write(row_num, col_num, '; \n'.join(actions), format_wrap)

            # Заполняем столбец "Примечание"
            col_num += 1
            sheet.write(row_num, col_num, prop.prop_note)

        book.close()
        return response

    def get_xlsx_information_systems(self, **kwargs):
        """
        Создает файл '.xlsx' с отдельной карточкой для каждой информационной системы.
        """
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Information_systems.xlsx"'

        systems = InformationSystem.objects.prefetch_related(
            'system_properties__fk_property',
            'system_properties__fk_property__property_actions',
            'system_properties__fk_property__othernetworkproperty_set',
        )

        book = xlsxwriter.Workbook(response, {'in_memory': True})
        format_title = book.add_format({
            'bold': True, 'font_size': 16, 'font_color': '#FFFFFF', 'bg_color': '#17324D',
            'align': 'left', 'valign': 'vcenter', 'border': 1,
        })
        format_section = book.add_format({
            'bold': True, 'font_size': 12, 'font_color': '#17324D', 'bg_color': '#DDEAF3',
            'border': 1,
        })
        format_label = book.add_format({
            'bold': True, 'font_color': '#17324D', 'bg_color': '#F3F7FA',
            'border': 1, 'text_wrap': True, 'valign': 'top',
        })
        format_cell = book.add_format({'border': 1, 'text_wrap': True, 'valign': 'top'})
        format_table_header = book.add_format({
            'bold': True, 'font_color': '#FFFFFF', 'bg_color': '#2F5D7C',
            'border': 1, 'text_wrap': True, 'align': 'center', 'valign': 'vcenter',
        })
        format_note = book.add_format({'italic': True, 'font_color': '#666666', 'text_wrap': True})

        def make_sheet_name(title, used_names):
            clean_title = re.sub(r'[\[\]\:\*\?\/\\]', ' ', title or 'ИС').strip() or 'ИС'
            clean_title = clean_title[:31]
            sheet_name = clean_title
            counter = 2
            while sheet_name in used_names:
                suffix = f" {counter}"
                sheet_name = f"{clean_title[:31 - len(suffix)]}{suffix}"
                counter += 1
            used_names.add(sheet_name)
            return sheet_name

        def property_short_title(prop):
            if not prop:
                return ''
            parts = []
            if prop.prop_name:
                parts.append(prop.prop_name)
            if prop.prop_ic_num:
                parts.append(f"№{prop.prop_ic_num}")
            return ' '.join(parts).strip()

        def write_section(sheet, row_num, title):
            sheet.merge_range(row_num, 0, row_num, 11, title, format_section)
            return row_num + 1

        def write_system_field(sheet, row_num, label, value):
            sheet.merge_range(row_num, 0, row_num, 3, label, format_label)
            sheet.merge_range(row_num, 4, row_num, 11, value or '', format_cell)
            return row_num + 1

        def write_table_header(sheet, row_num, headers):
            for col_num, header in enumerate(headers):
                sheet.write(row_num, col_num, header, format_table_header)
            return row_num + 1

        used_sheet_names = set()
        for system in systems:
            links = list(system.system_properties.all())
            linked_properties = [link.fk_property for link in links if link.fk_property]
            sheet = book.add_worksheet(make_sheet_name(system.is_name, used_sheet_names))
            sheet.set_landscape()
            sheet.fit_to_pages(1, 0)
            sheet.freeze_panes(3, 0)
            sheet.hide_gridlines(2)
            sheet.set_column(0, 0, 22)
            sheet.set_column(1, 1, 26)
            sheet.set_column(2, 2, 16)
            sheet.set_column(3, 3, 20)
            sheet.set_column(4, 4, 22)
            sheet.set_column(5, 5, 15)
            sheet.set_column(6, 6, 14)
            sheet.set_column(7, 7, 16)
            sheet.set_column(8, 8, 24)
            sheet.set_column(9, 9, 18)
            sheet.set_column(10, 10, 15)
            sheet.set_column(11, 11, 32)

            row_num = 0
            sheet.merge_range(row_num, 0, row_num, 11, f"Информационная система: {system.is_name}", format_title)
            sheet.set_row(row_num, 28)
            row_num += 2

            row_num = write_section(sheet, row_num, '1. Оборудование')
            equipment_headers = [
                'Вид имущества внутренний', 'Наименование имущества', 'Номер учета ИЦ',
                'Номер учета УМВД (инв. номер)', 'Заводской/серийный номер', 'Дата поставки',
                'Гарантия', 'Назначение', 'Установлено в / Предназначено для',
                'Состояние имущества', 'Дата списания', 'Примечание',
            ]
            row_num = write_table_header(sheet, row_num, equipment_headers)

            if linked_properties:
                for prop in linked_properties:
                    row = [
                        str(prop.fk_tp) if prop.fk_tp else '',
                        prop.prop_name,
                        prop.prop_ic_num,
                        prop.prop_inventory_num,
                        prop.prop_factory_num,
                        prop.prop_date_delivery.strftime('%d.%m.%Y') if prop.prop_date_delivery else '',
                        prop.prop_warranty_until.strftime('%d.%m.%Y') if prop.prop_warranty_until else '',
                        prop.prop_purpose,
                        property_short_title(prop.fk_installed_in),
                        prop.prop_status,
                        prop.prop_date_deregistration.strftime('%d.%m.%Y') if prop.prop_date_deregistration else '',
                        prop.prop_note,
                    ]
                    for col_num, value in enumerate(row):
                        sheet.write(row_num, col_num, value, format_cell)
                    row_num += 1
            else:
                sheet.merge_range(row_num, 0, row_num, 11, 'Оборудование не привязано.', format_note)
                row_num += 1

            row_num += 1
            row_num = write_section(sheet, row_num, '2. Сетевые настройки')
            network_header_row = row_num
            sheet.merge_range(network_header_row, 0, network_header_row, 2, 'Имущество', format_table_header)
            sheet.merge_range(network_header_row, 3, network_header_row, 4, 'Вид сети', format_table_header)
            sheet.merge_range(network_header_row, 5, network_header_row, 6, 'IP-адрес', format_table_header)
            sheet.merge_range(network_header_row, 7, network_header_row, 8, 'Виртуальный IP-адрес', format_table_header)
            sheet.merge_range(network_header_row, 9, network_header_row, 11, 'Примечание', format_table_header)
            row_num += 1
            has_networks = False
            for prop in linked_properties:
                for network in prop.othernetworkproperty_set.all():
                    has_networks = True
                    sheet.merge_range(row_num, 0, row_num, 2, property_short_title(prop), format_cell)
                    sheet.merge_range(row_num, 3, row_num, 4, network.onp_network_type or '', format_cell)
                    sheet.merge_range(row_num, 5, row_num, 6, network.onp_ip_address or '', format_cell)
                    sheet.merge_range(row_num, 7, row_num, 8, network.onp_virt_ip_address or '', format_cell)
                    sheet.merge_range(row_num, 9, row_num, 11, network.onp_note or '', format_cell)
                    row_num += 1
            if not has_networks:
                sheet.merge_range(row_num, 0, row_num, 11, 'Сетевые настройки для привязанного имущества не найдены.', format_note)
                row_num += 1

            row_num += 1
            row_num = write_section(sheet, row_num, '3. Действия с имуществом')
            action_header_row = row_num
            sheet.merge_range(action_header_row, 0, action_header_row, 2, 'Имущество', format_table_header)
            sheet.write(action_header_row, 3, 'Дата', format_table_header)
            sheet.merge_range(action_header_row, 4, action_header_row, 11, 'Действие', format_table_header)
            row_num += 1
            has_actions = False
            for prop in linked_properties:
                for action in prop.property_actions.all():
                    has_actions = True
                    sheet.merge_range(row_num, 0, row_num, 2, property_short_title(prop), format_cell)
                    sheet.write(row_num, 3, action.action_date.strftime('%d.%m.%Y') if action.action_date else '', format_cell)
                    sheet.merge_range(row_num, 4, row_num, 11, action.action_text or '', format_cell)
                    row_num += 1
            if not has_actions:
                sheet.merge_range(row_num, 0, row_num, 11, 'Действия с привязанным имуществом не найдены.', format_note)
                row_num += 1

            row_num += 1
            row_num = write_section(sheet, row_num, f"4. Сведения об информационной системе {system.is_name}")
            row_num = write_system_field(sheet, row_num, 'Введена в эксплуатацию', system.is_date_commissioning)
            row_num = write_system_field(sheet, row_num, 'Уровень защищенности', system.is_security_level)
            row_num = write_system_field(sheet, row_num, 'Класс защищенности', system.is_security_class)
            row_num = write_system_field(sheet, row_num, 'Модель угроз безопасности', system.is_threat_model)
            row_num = write_system_field(sheet, row_num, 'Аттестат соответствия по требованиям безопасности информации ИС', system.is_certificate)
            row_num = write_system_field(sheet, row_num, 'Разрешительная система доступа', system.is_access_permit_system)
            row_num = write_system_field(sheet, row_num, 'Описание технологического процесса', system.is_technological_process_description)
            row_num = write_system_field(sheet, row_num, 'Инструкция администратора безопасности', system.is_security_admin_instruction)
            row_num = write_system_field(sheet, row_num, 'Инструкция пользователя', system.is_user_instruction)
            row_num = write_system_field(sheet, row_num, 'Инструкция по созданию и применению парольной защиты', system.is_password_protection_instruction)
            row_num = write_system_field(sheet, row_num, 'Инструкция по организации антивирусной защиты', system.is_antivirus_instruction)
            row_num = write_system_field(sheet, row_num, 'Перечень сведений конфиденциального характера', system.is_confidential_information_list)
            row_num = write_system_field(sheet, row_num, 'Инструкция доступа в помещение, в которых ведется обработка персональных данных', system.is_room_access_instruction)
            row_num = write_system_field(sheet, row_num, 'Положение о разграничении прав доступа к обрабатываемой информации', system.is_access_rights_regulation)
            row_num = write_system_field(sheet, row_num, 'Список лиц, имеющих право доступа в серверное помещение', system.is_server_room_access_persons)
            row_num = write_system_field(sheet, row_num, 'Выведена из эксплуатации', system.is_date_decommissioning)

        if not used_sheet_names:
            sheet = book.add_worksheet('information_systems')
            sheet.write(0, 0, 'Информационные системы не найдены', format_cell)

        book.close()
        return response

    def _employee_full_name(employee):
        if not employee:
            return ''
        return f"{employee.emp_surname} {employee.emp_name} {employee.emp_middle_name}".strip()

    def _write_simple_xlsx(response, sheet_name, columns, rows):
        book = xlsxwriter.Workbook(response, {'in_memory': True})
        sheet = book.add_worksheet(sheet_name)
        sheet.freeze_panes(1, 0)
        sheet.autofilter(0, 0, 0, len(columns) - 1)

        header_format = book.add_format({
            'bold': True, 'font_color': '#FFFFFF', 'bg_color': '#2F5D7C',
            'border': 1, 'text_wrap': True, 'valign': 'vcenter',
        })
        cell_format = book.add_format({'border': 1, 'text_wrap': True, 'valign': 'top'})
        date_format = book.add_format({'border': 1, 'num_format': 'dd/mm/yyyy', 'valign': 'top'})

        for col_num, column in enumerate(columns):
            sheet.write(0, col_num, column, header_format)
            sheet.set_column(col_num, col_num, 22)

        for row_num, row in enumerate(rows, start=1):
            for col_num, value in enumerate(row):
                if isinstance(value, (date, datetime)):
                    sheet.write(row_num, col_num, value, date_format)
                else:
                    sheet.write(row_num, col_num, value if value is not None else '', cell_format)

        book.close()

    def get_xlsx_employees_children(self, **kwargs):
        """Создает файл '.xlsx' со списком детей сотрудников."""
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Employees_children.xlsx"'

        children = EmployeesChildren.objects.select_related('fk_emp')
        columns = [
            'Родитель', 'Фамилия ребенка', 'Имя ребенка', 'Отчество ребенка',
            'Дата рождения ребенка', 'Пол ребенка', 'Адрес проживания',
            'Обучается в', 'Мобильный телефон',
        ]

        def is_younger_than_18(birthday):
            if not birthday:
                return True
            today = date.today()
            try:
                eighteenth_birthday = birthday.replace(year=birthday.year + 18)
            except ValueError:
                eighteenth_birthday = date(birthday.year + 18, 2, 28)
            return eighteenth_birthday > today

        rows = []
        for child in children:
            if not is_younger_than_18(child.empc_birthday):
                continue
            rows.append([
                DownloadListsView._employee_full_name(child.fk_emp),
                child.empc_surname,
                child.empc_name,
                child.empc_middle_name,
                child.empc_birthday,
                child.empc_gender,
                child.empc_home_address,
                child.empc_study_place,
                child.empc_mobile_phone,
            ])
        DownloadListsView._write_simple_xlsx(response, 'children', columns, rows)
        return response

    def get_xlsx_employees_spouses(self, **kwargs):
        """Создает файл '.xlsx' со списком супругов сотрудников."""
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Employees_spouses.xlsx"'

        spouses = EmployeesSpouse.objects.select_related('fk_emp')
        columns = [
            'Сотрудник', 'Фамилия супруга(и)', 'Имя супруга(и)',
            'Отчество супруга(и)', 'Дата рождения супруга(и)',
        ]
        rows = [
            [
                DownloadListsView._employee_full_name(spouse.fk_emp),
                spouse.emps_surname,
                spouse.emps_name,
                spouse.emps_middle_name,
                spouse.emps_birthday,
            ]
            for spouse in spouses
        ]
        DownloadListsView._write_simple_xlsx(response, 'spouses', columns, rows)
        return response

    def get_xlsx_employees_automoto(self, **kwargs):
        """Создает файл '.xlsx' со списком личного автотранспорта сотрудников."""
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Employees_automoto.xlsx"'

        automoto = EmployeesAutomoto.objects.select_related('fk_auto_owner')
        columns = ['Владелец', 'Марка авто', 'Регистрационный знак', 'Форма собственности', 'Примечание']
        rows = [
            [
                DownloadListsView._employee_full_name(auto.fk_auto_owner),
                auto.empa_model,
                auto.empa_reg_num,
                auto.empa_owner_type,
                auto.empa_note,
            ]
            for auto in automoto
        ]
        DownloadListsView._write_simple_xlsx(response, 'automoto', columns, rows)
        return response

    def get_xlsx_employees_weapons(self, **kwargs):
        """Создает файл '.xlsx' со списком личного оружия сотрудников."""
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Employees_weapons.xlsx"'

        weapons = EmployeesWeapons.objects.select_related('fk_weapon_owner')
        columns = [
            'Владелец', 'Модель оружия', 'Калибр оружия', 'Серия, номер',
            'Название разрешения', 'Серийный номер разрешения',
            'Разрешение выдано с', 'Разрешение действительно до',
            'Тип разрешения', 'Примечание',
        ]
        rows = [
            [
                DownloadListsView._employee_full_name(weapon.fk_weapon_owner),
                weapon.empw_model,
                weapon.empw_caliber,
                weapon.empw_serial_number,
                weapon.empw_weapon_permit,
                weapon.empw_weapon_permit_serial_number,
                weapon.empw_start_weapon_permit,
                weapon.empw_end_weapon_permit,
                weapon.empw_type_permit,
                weapon.empw_note,
            ]
            for weapon in weapons
        ]
        DownloadListsView._write_simple_xlsx(response, 'weapons', columns, rows)
        return response
