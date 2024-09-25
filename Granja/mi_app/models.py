# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Alimentacion(models.Model):
    idalimentacion = models.AutoField(db_column='idAlimentacion', primary_key=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', max_length=1000)  # Field name made lowercase.
    dosis = models.FloatField()

    class Meta:
        managed = False
        db_table = 'alimentacion'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Clientes(models.Model):
    cedula = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=120)
    apellidos = models.CharField(max_length=45)
    direccion = models.CharField(max_length=45)
    telefono = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'clientes'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Porcinos(models.Model):
    idporcinos = models.AutoField(db_column='idPorcinos', primary_key=True)  # Field name made lowercase.
    edad = models.IntegerField(db_column='Edad', blank=True, null=True)  # Field name made lowercase.
    peso = models.IntegerField(db_column='Peso', blank=True, null=True)  # Field name made lowercase.
    razas_idrazas = models.ForeignKey('Razas', models.DO_NOTHING, db_column='Razas_idRazas')  # Field name made lowercase.
    clientes_cedula = models.ForeignKey(Clientes, models.DO_NOTHING, db_column='Clientes_cedula')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'porcinos'


class PorcinosHasAlimentacion(models.Model):
    porcinos_idporcinos = models.OneToOneField(Porcinos, models.DO_NOTHING, db_column='Porcinos_idPorcinos', primary_key=True)  # Field name made lowercase. The composite primary key (Porcinos_idPorcinos, Alimentacion_idAlimentacion) found, that is not supported. The first column is selected.
    alimentacion_idalimentacion = models.ForeignKey(Alimentacion, models.DO_NOTHING, db_column='Alimentacion_idAlimentacion')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'porcinos_has_alimentacion'
        unique_together = (('porcinos_idporcinos', 'alimentacion_idalimentacion'),)


class Razas(models.Model):
    idrazas = models.IntegerField(db_column='idRazas', primary_key=True)  # Field name made lowercase.
    name = models.CharField(unique=True, max_length=45)

    class Meta:
        managed = False
        db_table = 'razas'
