from django.db import models


class Cabinets(models.Model):
    """Кабинеты"""
    cab_id = models.AutoField(primary_key=True)
    cab_num = models.CharField(unique=True, max_length=30, verbose_name='Номер/Название кабинета')

    def __str__(self):
        return self.cab_num

    class Meta:
        verbose_name_plural = 'Кабинеты'
        verbose_name = 'Кабинет'
        db_table = 'cabinets'


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
                                       verbose_name='Количество должностей по штатной численности')
    fk_types_work = models.ForeignKey(TypesWork, db_column='fk_types_work', on_delete=models.SET_NULL, blank=True,
                                      null=True, verbose_name='Вид службы')

    def __str__(self):
        return self.pos_title

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
    fk_types_work = models.ForeignKey(TypesWork, db_column='fk_types_work', on_delete=models.SET_NULL, blank=True,
                                      null=True, verbose_name='Вид службы')

    def __str__(self):
        return '№' + str(self.emp_id) + ' - ' + str(self.emp_surname) + ' ' + str(self.emp_name) + ' ' \
               + str(self.emp_middle_name)

    class Meta:
        verbose_name_plural = 'Сотрудники'
        verbose_name = 'Сотрудник'
        db_table = 'employees'


class ComputersIsod(models.Model):
    """Компьютеры для работы в сети ИСОД МВД"""
    KINDS_ATTESTATION = (('Присоединен', 'Присоединен'), ('Требует присоединения', 'Требует присоединения'))

    comp_id = models.AutoField(primary_key=True)
    comp_reg_num = models.CharField(max_length=10, verbose_name='Регистрационный номер')
    comp_factory_num = models.CharField(max_length=10, verbose_name='Заводской номер')
    comp_mac_address = models.CharField(max_length=100, verbose_name='МАС адрес сетевой карты')
    comp_ip_address = models.GenericIPAddressField(verbose_name='IP-адрес')
    comp_virt_ip_address = models.GenericIPAddressField(verbose_name='Виртуальный IP-адрес')
    comp_id_dst_file = models.CharField(max_length=100, verbose_name='ID DST')
    comp_title_dst_file = models.CharField(max_length=100, verbose_name='Имя DST')
    fk_cabinet_location = models.ForeignKey(Cabinets, db_column='fk_cabinet_location', on_delete=models.SET_NULL,
                                            blank=True, null=True, verbose_name='Кабинет')
    fk_comp_owner = models.ForeignKey(Employees, db_column='fk_comp_owner', on_delete=models.SET_NULL,
                                      blank=True, null=True, verbose_name='Владелец')
    comp_attestation_status = models.CharField(max_length=100, choices=KINDS_ATTESTATION,
                                               verbose_name='Состояние аттестации')

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

    def __str__(self):
        return self.disk_reg_num

    class Meta:
        verbose_name_plural = 'Дисковые хранилища'
        verbose_name = 'Дисковое хранилище'
        db_table = 'disk_storage_isod'