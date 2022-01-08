from django.db import models
# Импортируем модель Divisions (Подразделения) из приложения IC (Информационный центр)
from ic.models import Divisions


class InformationSystems(models.Model):
    """Информационные системы"""
    is_id = models.AutoField(primary_key=True)
    is_title = models.CharField(max_length=250, verbose_name='Название информационной системы')
    is_note = models.TextField(blank=True, null=True, verbose_name='Примечание')

    def __str__(self):
        return str(self.is_title)

    class Meta:
        verbose_name_plural = 'Информационные системы'
        verbose_name = 'Информационная система'
        db_table = 'information_systems'



class UsersInformationSystems(models.Model):
    """Пользователи информационных систем"""
    uis_id = models.AutoField(primary_key=True)
    fk_is_title = models.ForeignKey(InformationSystems, db_column='fk_is_title', on_delete=models.SET_NULL, blank=True,
   	                                null=True, verbose_name='Название информационной системы')
    uis_surname = models.CharField(max_length=100, verbose_name='Фамилия')
    uis_name = models.CharField(max_length=100, verbose_name='Имя')
    uis_middle_name = models.CharField(max_length=100, verbose_name='Отчество')
    fk_div = models.ForeignKey(Divisions, db_column='fk_div', on_delete=models.SET_NULL, blank=True, null=True,
                               verbose_name='Подразделение')
    uis_position = models.CharField(blank=True, null=True, max_length=250, verbose_name='Должность')
    uis_email = models.EmailField(blank=True, null=True, verbose_name='Электронная почта')
    uis_login = models.CharField(blank=True, null=True, max_length=50, verbose_name='Логин')
    uis_password = models.CharField(blank=True, null=True, max_length=50, verbose_name='Пароль')
    uis_phone = models.CharField(max_length=100, blank=True, null=True, verbose_name='Телефон')
    uis_note = models.TextField(blank=True, null=True, verbose_name='Примечание')

    def __str__(self):
        return str(self.fk_is_title) + ' ' + str(self.uis_surname)

    class Meta:
        verbose_name_plural = 'Пользователи информационных систем'
        verbose_name = 'Пользователь информационной системы'
        db_table = 'users_information_systems'


class Raions(models.Model):
    """Районы"""
    r_id = models.AutoField(primary_key=True)
    r_title = models.CharField(max_length=250, verbose_name='Рассылка район')
    r_surname = models.CharField(max_length=100, verbose_name='Фамилия')
    r_name = models.CharField(max_length=100, verbose_name='Имя')
    r_middle_name = models.CharField(max_length=100, verbose_name='Отчество')
    r_position = models.CharField(blank=True, null=True, max_length=250, verbose_name='Должность')
    r_email = models.EmailField(blank=True, null=True, verbose_name='Электронная почта')
    r_phone = models.CharField(max_length=100, blank=True, null=True, verbose_name='Телефон')
    r_note = models.TextField(blank=True, null=True, verbose_name='Примечание')

    def __str__(self):
        return str(self.r_title)

    class Meta:
        verbose_name_plural = 'Районы'
        verbose_name = 'Район'
        db_table = 'Raions'