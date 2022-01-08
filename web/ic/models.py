from django.db import models


class TypesProperty(models.Model):
    """Вид имущества"""
    tp_id = models.AutoField(primary_key=True)
    tp_type = models.CharField(unique=True, max_length=100, verbose_name='Вид имущества')
    tp_note = models.TextField(blank=True, null=True, verbose_name='Примечание')

    def __str__(self):
        return self.tp_type

    class Meta:
        verbose_name_plural = 'Виды имущества'
        verbose_name = 'Вид имущества'
        db_table = 'types_property'


class Cabinets(models.Model):
    """Кабинеты"""
    cab_id = models.AutoField(primary_key=True)
    cab_num = models.CharField(unique=True, max_length=30, verbose_name='Номер/Название кабинета')
    cab_note = models.TextField(blank=True, null=True, verbose_name='Примечание')

    def __str__(self):
        return self.cab_num

    class Meta:
        verbose_name_plural = 'Кабинеты'
        verbose_name = 'Кабинет'
        db_table = 'cabinets'


class PropertyStandarts(models.Model):
	"""Нормы положенности имущества ИЦ"""
	KINDS_TYPES_PROPERTY = (('Средства связи','Средства связи'), ('Средства вычислительной техники', 'Средства вычислительной техники'),
						    ('Средства электронной организационной техники','Средства электронной организационной техники'),
						    ('Специальная техника','Специальная техника'))

	ps_id = models.AutoField(primary_key=True)
	ps_name = models.CharField(unique=True, max_length=250, verbose_name='Наименование имущества')
	ps_type = models.CharField(blank=True, null=True, max_length=50, choices=KINDS_TYPES_PROPERTY,
							   verbose_name='Тип имущества')
	ps_quantity_limit = models.IntegerField(blank=True, null=True, verbose_name='Количество положенного имущества')
	ps_note = models.TextField(blank=True, null=True, verbose_name='Примечание')

	def __str__(self):
		return self.ps_name

	class Meta:
		verbose_name_plural = 'Нормы положенности'
		verbose_name = 'Норма положенности'
		db_table = 'property_standarts'


class Property(models.Model):
	"""Имущество ИЦ"""
	# выбор вариантов из указанного кортежа
	KINDS_UNITS_MEASURES = (('Комплект', 'Комплект'), ('Штука', 'Штука'))
	KINDS_STATUS = (('Исправно','Исправно'), ('Неисправно','Неисправно'))

	prop_id = models.AutoField(primary_key=True)
	fk_tp = models.ForeignKey(TypesProperty, db_column='fk_tp', on_delete=models.SET_NULL, blank=True, null=True,
		    				  verbose_name='Вид имущества внутренний')
	fk_ps = models.ForeignKey(PropertyStandarts, db_column='fk_ps', on_delete=models.SET_NULL, blank=True, null=True,
                              verbose_name='Вид имущества по нормам положенности')
	prop_name = models.CharField(max_length=250, verbose_name='Наименование имущества')
	prop_ic_num = models.CharField(unique=True, max_length=50, verbose_name='Учетный номер в ИЦ')
	prop_inventory_num = models.CharField(unique=True, max_length=250, verbose_name='Номер учета УМВД (инв. номер)')
	prop_factory_num = models.CharField(max_length=250, verbose_name='Заводской/серийный номер')
	prop_unit_measure = models.CharField(max_length=50, choices=KINDS_UNITS_MEASURES,
									     verbose_name='Единица измерения')
	fk_prop_owner = models.ForeignKey('Employees', db_column='fk_prop_owner', on_delete=models.SET_NULL,
                                      blank=True, null=True, verbose_name='Владелец имущества')
	fk_cabinet_location = models.ForeignKey(Cabinets, db_column='fk_cabinet_location', on_delete=models.SET_NULL,
                                            blank=True, null=True, verbose_name='Кабинет')
	prop_date_exploitation = models.DateField(blank=True, null=True, verbose_name='Дата начала эксплуатации')
	prop_status = models.CharField(max_length=100, choices=KINDS_STATUS, verbose_name='Состояние имущества')
	prop_note = models.TextField(blank=True, null=True, verbose_name='Примечание')

	def __str__(self):
		return '№' + str(self.prop_id) + ' - ' + str(self.prop_name)

	class Meta:
		verbose_name_plural = 'Имущество'
		verbose_name = 'Имущество'
		db_table = 'property'


class TypesWork(models.Model):
    """Вид службы"""
    tw_id = models.AutoField(primary_key=True)
    tw_title = models.CharField(unique=True, max_length=100, verbose_name='Вид службы')

    def __str__(self):
        return self.tw_title

    class Meta:
        verbose_name_plural = 'Виды служб'
        verbose_name = 'Вид службы'
        db_table = 'types_work'


class Divisions(models.Model):
    """Подразделения"""
    div_id = models.AutoField(primary_key=True)
    div_title = models.CharField(unique=True, max_length=100, verbose_name='Название подразделения')

    def __str__(self):
        return self.div_title

    class Meta:
        verbose_name_plural = 'Подразделения'
        verbose_name = 'Подразделение'
        db_table = 'divisions'


class DepartmentsFirst(models.Model):
    """Отделы"""
    dep_first_id = models.AutoField(primary_key=True)
    dep_first_title = models.CharField(unique=True, max_length=150, verbose_name='Название отдела')
    fk_div = models.ForeignKey(Divisions, db_column='fk_div', on_delete=models.SET_NULL, blank=True, null=True,
                               verbose_name='Подразделение')

    def __str__(self):
        return self.dep_first_title

    class Meta:
        verbose_name_plural = 'Отделы'
        verbose_name = 'Отдел'
        db_table = 'departments_first'


class DepartmentsSecond(models.Model):
    """Отделения"""
    dep_second_id = models.AutoField(primary_key=True)
    dep_second_title = models.CharField(unique=True, max_length=150, verbose_name='Название отделения')
    fk_dep_first = models.ForeignKey(DepartmentsFirst, db_column='fk_dep_first', on_delete=models.SET_NULL, blank=True,
                                     null=True, verbose_name='Отдел')

    def __str__(self):
        return self.dep_second_title

    class Meta:
        verbose_name_plural = 'Отделения'
        verbose_name = 'Отделение'
        db_table = 'departments_second'


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
    	if self.fk_dep_second == None and self.fk_dep_first == None:
    		return str(self.pos_title)
    	# Если сотрудник не входит в отделение, НО входит в отдел, то должность пишется без отделений, но с отделом
    	elif self.fk_dep_second == None and self.fk_dep_first != None:
    		return str(self.fk_dep_first) + ', ' + str(self.pos_title)
    	# Если сотрудник и в отделении и в отделе - пишется полная должность с названиями отделений и отделов
    	else:
       		return str(self.fk_dep_first) + ', ' + str(self.fk_dep_second) + ', ' + str(self.pos_title)

    class Meta:
        verbose_name_plural = 'Должности'
        verbose_name = 'Должность'
        db_table = 'positions'


class EmployeesStatus(models.Model):
    """Статусы сотрудников"""
    emp_st_id = models.AutoField(primary_key=True)
    emp_status = models.CharField(unique=True, max_length=100, verbose_name='Статус сотрудника')

    def __str__(self):
        return self.emp_status

    class Meta:
        verbose_name_plural = 'Статусы сотрудников'
        verbose_name = 'Статус сотрудника'
        db_table = 'employees_status'


class Employees(models.Model):
    """Сотрудники"""
    emp_id = models.AutoField(primary_key=True)
    emp_surname = models.CharField(max_length=50, verbose_name='Фамилия')
    emp_name = models.CharField(max_length=50, verbose_name='Имя')
    emp_middle_name = models.CharField(max_length=50, verbose_name='Отчество')
    emp_birthday = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    fk_emp_status = models.ForeignKey(EmployeesStatus, db_column='fk_emp_status', on_delete=models.SET_NULL, blank=True,
                                      null=True, verbose_name='Статус сотрудника')
    fk_position = models.ForeignKey(Positions, db_column='fk_position', on_delete=models.SET_NULL, blank=True,
                                    null=True, verbose_name='Должность')
    fk_cabinet_location = models.ForeignKey(Cabinets, db_column='fk_cabinet_location', on_delete=models.SET_NULL,
                                            blank=True, null=True, verbose_name='Кабинет')
    emp_phone = models.CharField(max_length=50, blank=True, null=True, verbose_name='Телефон')
    emp_note = models.TextField(blank=True, null=True, verbose_name='Примечание')

    def __str__(self):
        return '№' + str(self.emp_id) + ' - ' + str(self.emp_surname) + ' ' + str(self.emp_name) + ' ' \
               + str(self.emp_middle_name)

    class Meta:
        verbose_name_plural = 'Сотрудники'
        verbose_name = 'Сотрудник'
        db_table = 'employees'


class ComputersIsod(models.Model):
    """Компьютеры для работы в сети ИСОД МВД"""
    # выбор вариантов из указанного кортежа
    KINDS_ATTESTATION = (('Присоединен', 'Присоединен'), ('Требует присоединения', 'Требует присоединения'))

    comp_id = models.AutoField(primary_key=True)
    comp_reg_num = models.CharField(max_length=10, verbose_name='Регистрационный номер')
    comp_mac_address = models.CharField(max_length=100, verbose_name='МАС адрес сетевой карты')
    comp_ip_address = models.GenericIPAddressField(verbose_name='IP-адрес')
    comp_virt_ip_address = models.GenericIPAddressField(verbose_name='Виртуальный IP-адрес')
    comp_id_dst_file = models.CharField(max_length=100, verbose_name='ID DST')
    comp_title_dst_file = models.CharField(max_length=100, verbose_name='Имя DST')
    fk_prop = models.ForeignKey(Property, db_column='fk_prop', on_delete=models.SET_NULL,
                                      blank=True, null=True, verbose_name='Имущество')
    comp_attestation_status = models.CharField(max_length=100, choices=KINDS_ATTESTATION,
                                               verbose_name='Состояние аттестации')
    comp_note = models.TextField(blank=True, null=True, verbose_name='Примечание')

    def __str__(self):
        return self.comp_reg_num

    class Meta:
        verbose_name_plural = 'Компьютеры сети ИСОД'
        verbose_name = 'Компьютер сети ИСОД'
        db_table = 'computers_isod'


class DiskStorageIsod(models.Model):
    """Дисковые хранилища для компьютеров, подключенных к сети ИСОД МВД"""
    disk_id = models.AutoField(primary_key=True)
    disk_reg_num = models.CharField(max_length=10, verbose_name='Регистрационный номер')
    disk_model = models.CharField(max_length=100, verbose_name='Модель диска')
    disk_size = models.CharField(max_length=100, verbose_name='Объем диска')
    disk_factory_num = models.CharField(max_length=100, verbose_name='Заводской номер диска')
    fk_disk_owner = models.ForeignKey(Employees, db_column='fk_disk_owner',
                                      on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Владелец')
    fk_install_in_comp = models.ForeignKey(ComputersIsod, db_column='fk_install_in_comp', on_delete=models.SET_NULL,
                                      blank=True, null=True, verbose_name='Установлен в компьютер')
    disk_note = models.TextField(blank=True, null=True, verbose_name='Примечание')

    def __str__(self):
        return self.disk_reg_num

    class Meta:
        verbose_name_plural = 'Дисковые хранилища'
        verbose_name = 'Дисковое хранилище'
        db_table = 'disk_storage_isod'