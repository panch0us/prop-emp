from django.db import models
# импорт reverse для создания ссылки url
from django.urls import reverse


class TypesProperty(models.Model):
    """Вид имущества"""
    tp_id = models.AutoField(primary_key=True)
    tp_type = models.CharField(unique=True, max_length=100, verbose_name='Вид имущества')
    tp_note = models.TextField(blank=True, verbose_name='Примечание')

    def __str__(self):
        return f"{self.tp_type}"

    class Meta:
        verbose_name_plural = 'Виды имущества'
        verbose_name = 'Вид имущества'
        db_table = 'types_property'
        ordering = ['tp_type']


class Ranks(models.Model):
    """Звания"""
    r_id = models.AutoField(primary_key=True)
    r_title = models.CharField(unique=True, max_length=250, verbose_name='Звание')
    r_note = models.TextField(blank=True, verbose_name='Примечание')

    def __str__(self):
        return f"{self.r_title}"

    class Meta:
        verbose_name_plural = 'Звания'
        verbose_name = 'Звание'
        db_table = 'ranks'
        ordering = ['r_title']


class Cabinets(models.Model):
    """Кабинеты"""
    cab_id = models.AutoField(primary_key=True)
    cab_num = models.CharField(unique=True, max_length=30, verbose_name='Номер/Название кабинета')
    cab_note = models.TextField(blank=True, verbose_name='Примечание')

    def __str__(self):
        return f"{self.cab_num}"

    class Meta:
        verbose_name_plural = 'Кабинеты'
        verbose_name = 'Кабинет'
        db_table = 'cabinets'
        ordering = ['cab_num']


class PropertyStandarts(models.Model):
    """Нормы положенности имущества ИЦ"""
    KINDS_TYPES_PROPERTY = (('Средства связи', 'Средства связи'),
                            ('Средства вычислительной техники', 'Средства вычислительной техники'),
                            ('Средства электронной организационной техники',
                             'Средства электронной организационной техники'),
                            ('Специальная техника', 'Специальная техника'))

    ps_id = models.AutoField(primary_key=True)
    ps_name = models.CharField(unique=True, max_length=250, verbose_name='Наименование имущества')
    ps_type = models.CharField(blank=True, max_length=50, choices=KINDS_TYPES_PROPERTY,
                               verbose_name='Тип имущества')
    ps_quantity_limit = models.IntegerField(blank=True, null=True, verbose_name='Количество положенного имущества')
    ps_note = models.TextField(blank=True, verbose_name='Примечание')

    def __str__(self):
        return f"{self.ps_name}"

    class Meta:
        verbose_name_plural = 'Нормы положенности'
        verbose_name = 'Норма положенности'
        db_table = 'property_standarts'
        ordering = ['ps_name', 'ps_type']


class Property(models.Model):
    """Имущество ИЦ"""
    # выбор вариантов из указанного кортежа
    KINDS_UNITS_MEASURES = (('Комплект', 'Комплект'), ('Штука', 'Штука'))
    KINDS_STATUS = (('Исправно', 'Исправно'),
                    ('Неисправно', 'Неисправно'),
                    ('В процессе списания', 'В процессе списания'),
                    ('Списано', 'Списано'))

    prop_id = models.AutoField(primary_key=True)
    fk_tp = models.ForeignKey(TypesProperty, db_column='fk_tp', on_delete=models.SET_NULL, blank=True, null=True,
                              verbose_name='Вид имущества внутренний')
    fk_ps = models.ForeignKey(PropertyStandarts, db_column='fk_ps', on_delete=models.SET_NULL, blank=True, null=True,
                              verbose_name='Вид имущества по нормам положенности')
    prop_name = models.CharField(blank=True, max_length=250, verbose_name='Наименование имущества')
    prop_ic_num = models.CharField(blank=True, max_length=50, verbose_name='Номер учета ИЦ')
    prop_inventory_num = models.CharField(blank=True, max_length=250, verbose_name='Номер учета УМВД (инв. номер)')
    prop_factory_num = models.CharField(blank=True, max_length=250, verbose_name='Заводской/серийный номер')
    prop_unit_measure = models.CharField(max_length=50, choices=KINDS_UNITS_MEASURES, blank=True,
                                         verbose_name='Единица измерения')
    fk_prop_owner = models.ForeignKey('Employees', db_column='fk_prop_owner', on_delete=models.SET_NULL,
                                      blank=True, null=True, verbose_name='Владелец имущества')
    fk_cabinet_location = models.ForeignKey(Cabinets, db_column='fk_cabinet_location', on_delete=models.SET_NULL,
                                            blank=True, null=True, verbose_name='Кабинет')
    prop_date_delivery = models.DateField(blank=True, null=True, verbose_name='Дата поставки')
    prop_date_exploitation = models.DateField(blank=True, null=True, verbose_name='Дата выдачи')
    prop_status = models.CharField(max_length=100, choices=KINDS_STATUS, verbose_name='Состояние имущества')
    prop_date_deregistration = models.DateField(blank=True, null=True, verbose_name='Дата списания')
    prop_note = models.TextField(blank=True, verbose_name='Примечание')

    def __str__(self):
        return f"вид: {self.fk_tp}, назв: {self.prop_name}, влад: {self.fk_prop_owner}, " \
               f"зав.№: {self.prop_factory_num}, уч.№ИЦ: {self.prop_ic_num}" \
            .replace('вид: None,', '') \
            .replace('назв: None,', '') \
            .replace('влад: None,', '') \
            .replace('зав.№: None,', '') \
            .replace('уч.№ИЦ: None', '')

    class Meta:
        verbose_name_plural = 'Имущество'
        verbose_name = 'Имущество'
        db_table = 'property'
        ordering = ['fk_tp', 'prop_name', 'fk_prop_owner']


class TypesWork(models.Model):
    """Вид службы"""
    tw_id = models.AutoField(primary_key=True)
    tw_title = models.CharField(unique=True, max_length=100, verbose_name='Вид службы')

    def __str__(self):
        return f"{self.tw_title}"

    class Meta:
        verbose_name_plural = 'Виды служб'
        verbose_name = 'Вид службы'
        db_table = 'types_work'


class Divisions(models.Model):
    """Подразделения"""
    div_id = models.AutoField(primary_key=True)
    div_title = models.CharField(unique=True, max_length=100, verbose_name='Название подразделения')

    def __str__(self):
        return f"{self.div_title}"

    class Meta:
        verbose_name_plural = 'Подразделения'
        verbose_name = 'Подразделение'
        db_table = 'divisions'
        ordering = ['div_title']


class DepartmentsFirst(models.Model):
    """Отделы"""
    dep_first_id = models.AutoField(primary_key=True)
    dep_first_title = models.CharField(unique=True, max_length=150, verbose_name='Название отдела')
    fk_div = models.ForeignKey(Divisions, db_column='fk_div', on_delete=models.SET_NULL, blank=True, null=True,
                               verbose_name='Подразделение')

    def __str__(self):
        return f"{self.dep_first_title}"

    class Meta:
        verbose_name_plural = 'Отделы'
        verbose_name = 'Отдел'
        db_table = 'departments_first'
        ordering = ['dep_first_title', 'fk_div']


class DepartmentsSecond(models.Model):
    """Отделения"""
    dep_second_id = models.AutoField(primary_key=True)
    dep_second_title = models.CharField(unique=True, max_length=150, verbose_name='Название отделения')
    fk_dep_first = models.ForeignKey(DepartmentsFirst, db_column='fk_dep_first', on_delete=models.SET_NULL, blank=True,
                                     null=True, verbose_name='Отдел')

    def __str__(self):
        return f"{self.dep_second_title}"

    class Meta:
        verbose_name_plural = 'Отделения'
        verbose_name = 'Отделение'
        db_table = 'departments_second'
        ordering = ['dep_second_title', 'fk_dep_first']


class DepartmentsRegionalLevel(models.Model):
    """Территориальный ОВД на районном уровне"""
    drl_id = models.AutoField(primary_key=True)
    drl_title = models.CharField(unique=True, max_length=250, verbose_name='Название ОВД')
    drl_title_area = models.CharField(unique=True, max_length=100, verbose_name='Название района',)
    fk_self_subordinate = models.ForeignKey('self', db_column='fk_self_subordinate', on_delete=models.SET_NULL,
                                             blank=True, null=True, verbose_name='Входит в состав ОВД')
    drl_note = models.TextField(blank=True, verbose_name='Примечание')

    def __str__(self):
        return f"{self.drl_title_area} ({self.drl_title})"

    class Meta:
        verbose_name_plural = 'Территориальные ОВД на районном уровне'
        verbose_name = 'Территориальный ОВД на районном уровне'
        db_table = 'departments_regional_level'
        ordering = ['drl_title_area']


class Positions(models.Model):
    """Должности"""
    pos_id = models.AutoField(primary_key=True)
    pos_title = models.CharField(max_length=100, verbose_name='Название должности')
    fk_dep_second = models.ForeignKey(DepartmentsSecond, db_column='fk_dep_second', on_delete=models.SET_NULL,
                                      blank=True, null=True, verbose_name='Отделение')
    fk_dep_first = models.ForeignKey(DepartmentsFirst, db_column='fk_dep_first', on_delete=models.SET_NULL,
                                     blank=True, null=True, verbose_name='Отдел')
    fk_division = models.ForeignKey(Divisions, db_column='fk_division', on_delete=models.SET_NULL, blank=True,
                                    null=True, verbose_name='Подразделение')
    pos_quantity = models.IntegerField(blank=True, null=True,
                                       verbose_name='Кол-во должностей по ШР')
    fk_types_work = models.ForeignKey(TypesWork, db_column='fk_types_work', on_delete=models.SET_NULL, blank=True,
                                      null=True, verbose_name='Вид службы')

    def __str__(self):
        # Если сотрудник не входит в отделение и не входит в отдел, то должность пишется без отделений и отделов
        if self.fk_dep_second is None and self.fk_dep_first is None:
            return f"{self.pos_title} ({self.fk_types_work})"
        # Если сотрудник не входит в отделение, НО входит в отдел, то должность пишется без отделений, но с отделом
        elif self.fk_dep_second is None and self.fk_dep_first is not None:
            return f"{self.fk_dep_first}, {self.pos_title} ({self.fk_types_work})"
        # Если сотрудник и в отделении и в отделе - пишется полная должность с названиями отделений и отделов
        else:
            return f"{self.fk_dep_first}, {self.fk_dep_second}, {self.pos_title} ({self.fk_types_work})"

    class Meta:
        verbose_name_plural = 'Должности'
        verbose_name = 'Должность'
        db_table = 'positions'
        ordering = ['-fk_dep_first', 'fk_dep_second', 'pos_title']


class EmployeesStatus(models.Model):
    """Статусы сотрудников"""
    emp_st_id = models.AutoField(primary_key=True)
    emp_status = models.CharField(unique=True, max_length=100, verbose_name='Статус сотрудника')

    def __str__(self):
        return f"{self.emp_status}"

    class Meta:
        verbose_name_plural = 'Статусы сотрудников'
        verbose_name = 'Статус сотрудника'
        db_table = 'employees_status'
        ordering = ['emp_status']


class Employees(models.Model):
    """Сотрудники"""
    EMP_CHOICES_SPORT_CLASS = (('Мастер', 'Мастер'),
                               ('Специалист 1 класса', 'Специалист 1 класса'),
                               ('Специалист 2 класса', 'Специалист 2 класса'),
                               ('Специалист 3 класса', 'Специалист 3 класса'))

    emp_id = models.AutoField(primary_key=True)
    emp_surname = models.CharField(max_length=50, verbose_name='Фамилия')
    emp_name = models.CharField(max_length=50, verbose_name='Имя')
    emp_middle_name = models.CharField(max_length=50, verbose_name='Отчество')
    emp_birthday = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    fk_emp_status = models.ForeignKey(EmployeesStatus, db_column='fk_emp_status', on_delete=models.SET_NULL, blank=True,
                                      null=True, verbose_name='Статус сотрудника')
    fk_position = models.ForeignKey(Positions, db_column='fk_position', on_delete=models.SET_NULL, blank=True,
                                    null=True, verbose_name='Должность')
    fk_rank = models.ForeignKey(Ranks, db_column='fk_rank', on_delete=models.SET_NULL, blank=True, null=True,
                                verbose_name='Звание, чин, категория')
    fk_cabinet_location = models.ForeignKey(Cabinets, db_column='fk_cabinet_location', on_delete=models.SET_NULL,
                                            blank=True, null=True, verbose_name='Каб.')
    emp_phone = models.CharField(max_length=50, blank=True, verbose_name='Сл. тел', help_text='Формат: 11-11')
    emp_phone_home = models.CharField(max_length=50, blank=True, verbose_name='Дом. тел.', help_text='Формат: 11-11-11')
    emp_phone_mobile = models.CharField(max_length=100, blank=True, verbose_name='Моб. тел.',
                                        help_text='Формат: 1-111-111-11-11')
    emp_home_address = models.CharField(max_length=250, blank=True, verbose_name='Дом. адрес',
                                        help_text='Формат: с указанием города (г. Брянск, ул. ...)')
    emp_sport_class = models.CharField(blank=True, max_length=50, choices=EMP_CHOICES_SPORT_CLASS,
                                        verbose_name='Квалификационное звание')
    emp_date_sport_class = models.DateField(blank=True, null=True,
                                            verbose_name='Дата присвоения квал. звания')
    emp_date_document_sport_class = models.DateField(blank=True, null=True,
                                            verbose_name='Дата приказа о присвоении квал. звания')
    emp_number_sport_class = models.CharField(max_length=100, blank=True,
                                              verbose_name='№ приказа о присвоении квал. звания',
                                              help_text='Символ "№" не вносить')
    fk_depart_region_lvl = models.ForeignKey(DepartmentsRegionalLevel, db_column='fk_depart_region_lvl',
                                             on_delete=models.SET_NULL, blank=True, null=True,
                                             verbose_name='Район проживания',
                                             help_text='Район проживания (соотносится с адресом проживания)')

    emp_note = models.TextField(blank=True, verbose_name='Примечание')
    emp_url = models.SlugField(max_length=130, help_text='Указать анг. буквами ссылку на сотрудника (например: ivanov)')

    def __str__(self):
        return f"{self.emp_surname} {self.emp_name} {self.emp_middle_name}"

    def get_absolute_url(self):
        """
        Получение ссылки на сотрудника
        employee_detail - имя шаблона в urls.py приложения ic
        """
        return reverse('employee_detail', kwargs={"slug": self.emp_url})

    class Meta:
        verbose_name_plural = 'Сотрудники'
        verbose_name = 'Сотрудник'
        db_table = 'employees'
        ordering = ['emp_surname', 'emp_name', 'emp_middle_name', 'fk_position__fk_dep_first']


class OtherInformationAboutComputers(models.Model):
    """Иная информация о вычислительной технике"""
    oiac_id = models.AutoField(primary_key=True)
    fk_prop = models.ForeignKey(Property, db_column='fk_prop', on_delete=models.SET_NULL,
                                blank=True, null=True, verbose_name='Имущество')
    oiac_os = models.CharField(blank=True, max_length=250, verbose_name='Операционная система')
    oiac_user_name = models.CharField(blank=True, max_length=50, verbose_name='Имя пользователя')
    oiac_user_pass = models.CharField(blank=True, max_length=50, verbose_name='Пароль пользователя')
    oiac_comp_name = models.CharField(blank=True, max_length=50, verbose_name='Имя компьютера')
    oiac_comp_workgroup = models.CharField(blank=True, max_length=50, verbose_name='Рабочая группа компьютера')
    oiac_note = models.TextField(blank=True, verbose_name='Примечание')

    def __str__(self):
        return f"{self.oiac_comp_name}"

    class Meta:
        verbose_name_plural = 'Иная информация о вычислительной технике'
        verbose_name = 'Иная информация о вычислительной технике'
        db_table = 'other_information_about_computers'


class OtherNetworkProperty(models.Model):
    """Иное имущество, подключенное к сети"""
    ONP_CHOICES_NETWORK_TYPE = (('Локальная (не ИСОД)', 'Локальная (не ИСОД)'),
                                ('Интернет', 'Интернет'))
    onp_id = models.AutoField(primary_key=True)
    fk_prop = models.ForeignKey(Property, db_column='fk_prop', on_delete=models.SET_NULL,
                                blank=True, null=True, verbose_name='Имущество')
    onp_network_type = models.CharField(blank=True, max_length=100, choices=ONP_CHOICES_NETWORK_TYPE,
                                        verbose_name='Вид сети')
    onp_ip_address = models.GenericIPAddressField(unique=True, blank=True, null=True, verbose_name='IP-адрес')
    onp_note = models.TextField(blank=True, verbose_name='Примечание')

    def __str__(self):
        return f"{self.onp_ip_address}"

    class Meta:
        verbose_name_plural = 'Иное имущество, подключенное к сети'
        verbose_name = 'Иное имущество, подключенное к сети'
        db_table = 'other_network_property'


class AccountingCryptographicSecurity(models.Model):
    """Учет средств криптографической защиты информации (сокр. СКЗИ)"""
    ACS_CHOICES_STATUS = (('Выдано', 'Выдано'), ('Изъято', 'Изъято'))
    ACS_CHOICES_PURPOSE = (('(Должн. лицо) подпись СЭД', '(Должн. лицо) подпись СЭД'),
                           ('(Юр. лицо) подтверждение личности на интернет порт. "Гос. услуг"',
                            '(Юр. лицо) подтверждение личности на интернет порт. "Гос. услуг"'),
                           ('Администратор ГС ПВДНП', 'Администратор ГС ПВДНП'),
                           ('Пользователь ГС ПВДНП', 'Пользователь ГС ПВДНП'),
                           ('Пользователь ГАС ПС', 'Пользователь ГАС ПС'),
                           )

    acs_id = models.AutoField(primary_key=True)
    fk_prop = models.ForeignKey(Property, db_column='fk_prop', on_delete=models.SET_NULL, blank=True, null=True,
                                verbose_name='Имущество')
    acs_purpose = models.CharField(blank=True, choices=ACS_CHOICES_PURPOSE, max_length=100,
                                   verbose_name='Предназначение')
    acs_received_organization = models.CharField(blank=True, max_length=100, verbose_name='От кого получено',
                                                 help_text='Например, ЦИТСиЗИ, ГИАЦ или ИЦ')
    acs_start_date = models.DateField(blank=True, null=True, verbose_name='Начало срока действия')
    acs_final_date = models.DateField(blank=True, null=True, verbose_name='Окончание срока действия')
    acs_status = models.CharField(max_length=50, choices=ACS_CHOICES_STATUS, blank=True, verbose_name='Статус')
    acs_note = models.TextField(blank=True, verbose_name='Примечание')

    def __str__(self):
        return f"{self.acs_purpose}"

    class Meta:
        verbose_name_plural = 'СКЗИ'
        verbose_name = 'СКЗИ'
        db_table = 'accounting_cryptographic_security'


class IssueOfficeProducts(models.Model):
    """Выдача канцелярских и иных расходных товаров"""
    iop_id = models.AutoField(primary_key=True)
    fk_tp = models.ForeignKey(TypesProperty, db_column='fk_tp', on_delete=models.SET_NULL, blank=True, null=True,
                              verbose_name='Вид имущества внутренний')
    iop_title = models.CharField(blank=True, max_length=100, verbose_name='Название имущества')
    iop_quantity = models.IntegerField(blank=True, null=True, verbose_name='Кол-во выданного')
    fk_op_owner = models.ForeignKey(Employees, db_column='fk_op_owner', on_delete=models.SET_NULL,
                                    blank=True, null=True, verbose_name='Владелец')
    iop_date_issue = models.DateField(blank=True, null=True, verbose_name='Дата выдачи')
    iop_note = models.TextField(blank=True, verbose_name='Примечание')

    def __str__(self):
        return f"{self.iop_title}"

    class Meta:
        verbose_name_plural = 'Выдача канц. товаров'
        verbose_name = 'Выдача канц. товара'
        db_table = 'issue_office_products'
        ordering = ['iop_title']


class ComputersIsod(models.Model):
    """Компьютеры для работы в сети ИСОД МВД"""
    # выбор вариантов из указанного кортежа
    KINDS_ATTESTATION = (('Присоединен', 'Присоединен'), ('Требует присоединения', 'Требует присоединения'))

    comp_id = models.AutoField(primary_key=True)
    comp_reg_num = models.CharField(unique=True, max_length=10, verbose_name='Рег. номер',
                                    help_text='Данный номер наклен на системный блок ПК сети ИСОД')
    comp_mac_address = models.CharField(max_length=100, verbose_name='МАС адрес сетевой карты')
    comp_ip_address = models.GenericIPAddressField(unique=True, blank=True, null=True, verbose_name='IP-адрес')
    comp_virt_ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name='Виртуальный IP-адрес')
    comp_id_dst_file = models.CharField(blank=True, max_length=100, verbose_name='ID DST')
    comp_title_dst_file = models.CharField(blank=True, max_length=100, verbose_name='Имя DST')
    fk_prop = models.ForeignKey(Property, db_column='fk_prop', on_delete=models.SET_NULL, blank=True, null=True,
                                verbose_name='Имущество')
    comp_attestation_status = models.CharField(max_length=100, choices=KINDS_ATTESTATION,
                                               verbose_name='Состояние аттестации')
    comp_note = models.TextField(blank=True, verbose_name='Примечание')

    def __str__(self):
        return f"№АРМ: {self.comp_reg_num}"

    class Meta:
        verbose_name_plural = 'Компьютеры сети ИСОД'
        verbose_name = 'Компьютер сети ИСОД'
        db_table = 'computers_isod'


class DiskStorageIsod(models.Model):
    """Дисковые хранилища для компьютеров, подключенных к сети ИСОД МВД"""
    disk_id = models.AutoField(primary_key=True)
    disk_reg_num = models.CharField(unique=True, max_length=10, verbose_name='Регистрационный номер')
    disk_model = models.CharField(max_length=100, verbose_name='Модель диска')
    disk_size = models.CharField(max_length=100, verbose_name='Объем диска',
                                 help_text='Например, 10 GB, 1 TB (между пробел)')
    disk_factory_num = models.CharField(max_length=100, verbose_name='Заводской номер диска')
    fk_disk_owner = models.ForeignKey(Employees, db_column='fk_disk_owner',
                                      on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Владелец')
    fk_install_in_comp = models.ForeignKey(ComputersIsod, db_column='fk_install_in_comp', on_delete=models.SET_NULL,
                                           blank=True, null=True, verbose_name='Установлен в компьютер',
                                           help_text='Номер компьютера в таблице "Компьютеры в сети ИСОД"')
    disk_note = models.TextField(blank=True, verbose_name='Примечание')

    def __str__(self):
        return f"{self.disk_reg_num}"

    class Meta:
        verbose_name_plural = 'Дисковые хранилища'
        verbose_name = 'Дисковое хранилище'
        db_table = 'disk_storage_isod'
        ordering = ['fk_install_in_comp']