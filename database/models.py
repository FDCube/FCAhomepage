# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
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
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Competition(models.Model):
    competition_name = models.CharField(primary_key=True, max_length=30)
    competition_turn = models.CharField(max_length=20)
    cubeevent = models.CharField(db_column='CubeEvent', max_length=20)  # Field name made lowercase.
    competition_time = models.DateTimeField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    scramble1 = models.CharField(max_length=100, blank=True, null=True)
    scramble2 = models.CharField(max_length=100, blank=True, null=True)
    scramble3 = models.CharField(max_length=100, blank=True, null=True)
    scramble4 = models.CharField(max_length=100, blank=True, null=True)
    scramble5 = models.CharField(max_length=100, blank=True, null=True)
    scramble_extra1 = models.CharField(max_length=100, blank=True, null=True)
    scramble_extra2 = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'competition'
        unique_together = (('competition_name', 'competition_turn', 'cubeevent'),)


class CompetitionTime(models.Model):
    competition_name = models.CharField(primary_key=True, max_length=30)
    competition_turn = models.CharField(max_length=20)
    cubeevent = models.CharField(db_column='CubeEvent', max_length=20)  # Field name made lowercase.
    studentnumber = models.CharField(max_length=20)
    time1 = models.CharField(max_length=20, blank=True, null=True)
    time2 = models.CharField(max_length=20, blank=True, null=True)
    time3 = models.CharField(max_length=20, blank=True, null=True)
    time4 = models.CharField(max_length=20, blank=True, null=True)
    time5 = models.CharField(max_length=20, blank=True, null=True)
    single = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    average = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'competition_time'
        unique_together = (('competition_name', 'competition_turn', 'cubeevent', 'studentnumber'),)


class DatabaseLogin(models.Model):
    student_no = models.CharField(primary_key=True, max_length=12)
    password = models.CharField(max_length=16)

    class Meta:
        managed = False
        db_table = 'database_login'


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


class Login(models.Model):
    username = models.CharField(primary_key=True, max_length=20)
    passwd = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'login'


class Person(models.Model):
    studentnumber = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=20)
    college = models.CharField(max_length=20, blank=True, null=True)
    major = models.CharField(max_length=30, blank=True, null=True)
    passwd = models.CharField(max_length=20)
    wcaid = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'person'


class Record(models.Model):
    cubeevent = models.CharField(db_column='CubeEvent', primary_key=True, max_length=20)  # Field name made lowercase.
    name_single = models.CharField(max_length=20, blank=True, null=True)
    time_single = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    name_average = models.CharField(max_length=20, blank=True, null=True)
    time_average = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'record'
