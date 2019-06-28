"""
author wanghaiying
date 20190601
description django模型类定义
"""
from django.db import models
from sqlalchemy import Column, DateTime, String, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


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
    first_name = models.CharField(max_length=30)
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


class ColumnModel(models.Model):
    columnid = models.IntegerField(primary_key=True)
    tableid = models.IntegerField()
    columnname = models.CharField(max_length=50)
    datatype = models.BigIntegerField(blank=True, null=True)
    datatypename = models.CharField(max_length=50, blank=True, null=True)
    length = models.IntegerField(blank=True, null=True)
    precisiona = models.IntegerField(blank=True, null=True)
    scale = models.IntegerField(blank=True, null=True)
    nullable = models.TextField()  # This field type is a guess.
    indexa = models.IntegerField()
    description = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'column'


class CriticalTask(models.Model):
    taskid = models.AutoField(primary_key=True)
    recordtime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'criticaltask'


class CustomSchedule(models.Model):
    customscheduleid = models.AutoField(primary_key=True)
    taskid = models.IntegerField()
    dateid = models.IntegerField()
    description = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'customschedule'


class Database(models.Model):
    databaseid = models.IntegerField(primary_key=True)
    databasename = models.CharField(max_length=50)
    dbserverip = models.CharField(max_length=50)
    connectionstring = models.CharField(max_length=200)
    connectionstringexpression = models.CharField(max_length=1000, blank=True, null=True)
    databasetype = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    uid = models.CharField(max_length=50)
    pwd = models.CharField(max_length=50)
    enabled = models.TextField()  # This field type is a guess.
    lastupdatetime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'database'


class DbServer(models.Model):
    servername = models.CharField(max_length=50)
    ipaddress = models.CharField(primary_key=True, max_length=50)
    enabled = models.TextField()  # This field type is a guess.
    lastupdatetime = models.DateField()

    class Meta:
        managed = False
        db_table = 'dbserver'


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


class DsaBcpQuery(models.Model):
    taskid = models.IntegerField()
    querysql = models.CharField(max_length=1024)
    remark = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dsabcpquery'


class EtlServer(models.Model):
    ipaddress = models.CharField(primary_key=True, max_length=50)
    etlservername = models.CharField(max_length=50)
    packagerootpath = models.CharField(max_length=200)
    enabled = models.TextField()  # This field type is a guess.
    lastupdatetime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'etlserver'


class PreTask(models.Model):
    taskid = models.IntegerField(primary_key=True)
    pretaskid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pretask'
        unique_together = (('taskid', 'pretaskid'),)


class Schedule(models.Model):
    originaldate = models.DateTimeField(primary_key=True)
    dateid = models.IntegerField()
    istradedate = models.TextField()  # This field type is a guess.
    isweeklydate = models.TextField()  # This field type is a guess.
    ismonthlydate = models.TextField()  # This field type is a guess.
    memo = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'schedule'


# class SmsLog(models.Model):
#     id = models.IntegerField()
#     mobiles = models.CharField(max_length=1024, blank=True, null=True)
#     content = models.CharField(max_length=1024, blank=True, null=True)
#     recordtime = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'sms_log'


class SSISTask(models.Model):
    taskname = models.CharField(max_length=255, blank=True, null=True)
    ssispackagename = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ssis_task'


class SSISTask1(models.Model):
    ssispackagename = models.CharField(max_length=255, blank=True, null=True)
    where_u6761_u4ef6 = models.CharField(db_column='where\\u6761\\u4ef6', max_length=255, blank=True,
                                         null=True)  # Field renamed to remove unsuitable characters.
    f3 = models.CharField(db_column='F3', max_length=255, blank=True, null=True)  # Field name made lowercase.
    f4 = models.CharField(db_column='F4', max_length=255, blank=True, null=True)  # Field name made lowercase.
    f5 = models.CharField(db_column='F5', max_length=255, blank=True, null=True)  # Field name made lowercase.
    f6 = models.CharField(db_column='F6', max_length=255, blank=True, null=True)  # Field name made lowercase.
    f7 = models.CharField(db_column='F7', max_length=255, blank=True, null=True)  # Field name made lowercase.
    f8 = models.CharField(db_column='F8', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ssis_task1'


class StepLog(models.Model):
    steplogid = models.IntegerField(primary_key=True)
    tasklogid = models.IntegerField()
    taskid = models.IntegerField(blank=True, null=True)
    taskname = models.CharField(max_length=200, blank=True, null=True)
    stepname = models.CharField(max_length=200)
    dcdate = models.IntegerField()
    srcrecordcount = models.IntegerField(blank=True, null=True)
    dstrecordcount = models.IntegerField(blank=True, null=True)
    stepissuccess = models.TextField()  # This field type is a guess.
    steperrorinfo = models.TextField(blank=True, null=True)
    errorfile = models.CharField(max_length=1000, blank=True, null=True)
    stepstarttime = models.DateTimeField(blank=True, null=True)
    stepcompletetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'steplog'


class SysDiagrams(models.Model):
    name = models.CharField(max_length=128)
    principal_id = models.IntegerField()
    diagram_id = models.AutoField(primary_key=True)
    version = models.IntegerField(blank=True, null=True)
    definition = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sysdiagrams'
        unique_together = (('principal_id', 'name'),)


class SystemCode(models.Model):
    id = models.IntegerField(primary_key=True)
    codetype = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    isbuildin = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'systemcode'


class SystemParameter(models.Model):
    type = models.SmallIntegerField()
    typename = models.CharField(max_length=100)
    key = models.CharField(unique=True, max_length=100)
    value = models.CharField(max_length=1000)
    description = models.CharField(max_length=200)
    lastoperator = models.CharField(max_length=200, blank=True, null=True)
    lastmodify = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'systemparameter'


class SystemVariable(models.Model):
    key = models.CharField(primary_key=True, max_length=100)
    value = models.CharField(max_length=1000)
    description = models.CharField(max_length=200)
    isbuildin = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'systemvariable'


class Table(models.Model):
    tableid = models.IntegerField(primary_key=True)
    tablename = models.CharField(max_length=50)
    originaltablename = models.CharField(max_length=50)
    tablenameexpression = models.CharField(max_length=100, blank=True, null=True)
    databaseid = models.IntegerField()
    schemaid = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=50)
    enabled = models.TextField()  # This field type is a guess.
    lastupdatetime = models.DateTimeField()
    extractionexpression = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'table'


class TablePartitionConfig(models.Model):
    dstdbname = models.CharField(primary_key=True, max_length=100)
    tablename = models.CharField(max_length=100)
    partitionperiod = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tablepartitionconfig'
        unique_together = (('dstdbname', 'tablename'),)


class Task(models.Model):
    taskId = models.IntegerField(primary_key=True)
    etlserverip = models.CharField(max_length=50)
    taskName = models.CharField(max_length=100)
    executionType = models.CharField(max_length=50)
    taskType = models.CharField(max_length=50)
    scheduleType = models.CharField(max_length=50)
    databaseid = models.IntegerField(blank=True, null=True)
    executionexpression = models.CharField(max_length=200, blank=True, null=True)
    syninformaticatime = models.DateTimeField(blank=True, null=True)
    startExecuteDate = models.IntegerField()
    enabled = models.TextField()  # This field type is a guess.
    preConditionType = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'task'


class TaskDataLog(models.Model):
    taskdatalogid = models.AutoField(primary_key=True)
    tasklogid = models.IntegerField()
    taskid = models.IntegerField()
    dcdate = models.IntegerField()
    tableid = models.IntegerField()
    destdbserverip = models.CharField(max_length=50)
    destdatabase = models.CharField(max_length=50)
    desttablename = models.CharField(max_length=50)
    logdatetime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'taskdatalog'


class TaskDestTable(models.Model):
    taskdesttableid = models.AutoField(primary_key=True)
    taskid = models.IntegerField()
    desttableid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'taskdesttable'


# class TaskIdList(models.Model):
#     id = models.IntegerField(blank=True, null=True)
#     taskid = models.IntegerField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'taskid_list'


class TaskLog(models.Model):
    tasklogid = models.IntegerField(primary_key=True)
    taskid = models.IntegerField()
    taskname = models.CharField(max_length=100)
    etlserverip = models.CharField(max_length=50)
    packagepath = models.CharField(max_length=500)
    dcdate = models.IntegerField()
    issuccess = models.TextField()  # This field type is a guess.
    errorinfo = models.CharField(max_length=1000, blank=True, null=True)
    starttime = models.DateTimeField()
    completetime = models.DateTimeField(blank=True, null=True)
    isreload = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'tasklog'


class TaskParameterLog(models.Model):
    taskid = models.IntegerField(primary_key=True)
    paraname = models.CharField(max_length=100)
    paravalue = models.CharField(max_length=4000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'taskparameterlog'
        unique_together = (('taskid', 'paraname'),)


class TaskSrcTable(models.Model):
    tasksrctableid = models.AutoField(primary_key=True)
    taskid = models.IntegerField()
    srctableid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tasksrctable'


class TaskStatus(models.Model):
    taskid = models.AutoField(primary_key=True)
    lastsucceededexecutedateid = models.IntegerField(blank=True, null=True)
    lastexecutedateid = models.IntegerField()
    starttime = models.DateTimeField()
    completetime = models.DateTimeField(blank=True, null=True)
    errorcount = models.IntegerField()
    status = models.CharField(max_length=50)
    errorinfo = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'taskstatus'


class TaskType(models.Model):
    tasktype = models.CharField(primary_key=True, max_length=50)
    description = models.CharField(max_length=200)
    priority = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tasktype'


class Zqyejs(models.Model):
    scdm = models.CharField(max_length=2, blank=True, null=True)
    qsbh = models.CharField(max_length=8, blank=True, null=True)
    zqzh = models.CharField(max_length=10, blank=True, null=True)
    xwh = models.CharField(max_length=5, blank=True, null=True)
    zqdm = models.CharField(max_length=6, blank=True, null=True)
    zqlb = models.CharField(max_length=2, blank=True, null=True)
    ltlx = models.CharField(max_length=1, blank=True, null=True)
    qylb = models.CharField(max_length=2, blank=True, null=True)
    gpnf = models.CharField(max_length=4, blank=True, null=True)
    ye1 = models.CharField(max_length=36, blank=True, null=True)
    ye2 = models.CharField(max_length=36, blank=True, null=True)
    by = models.CharField(max_length=20, blank=True, null=True)
    jzrq = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zqyejs'


class briefinfo(models.Model):
    taskType = models.CharField(max_length=32, db_index=True)
    totalTaskCount = models.IntegerField('总任务数', null=True)
    runningTaskCount = models.IntegerField('运行中的任务数', null=True)
    idleTaskCount = models.IntegerField('未运行的任务数', null=True)
    successTaskCount = models.IntegerField('运行成功的任务数', null=True)
    failureTaskCount = models.IntegerField('运行失败的任务数', null=True)

    class Meta:
        verbose_name = '实例执行概况'


class Server(models.Model):
    server_id = models.AutoField(primary_key=True)
    server_ip = models.CharField(max_length=32, null=False)
    server_name = models.CharField(max_length=64)
    business = models.CharField(max_length=64)
    desc = models.CharField(max_length=128)
    enabled = models.IntegerField()
    createtime = models.DateTimeField(null=False)
    updatetime = models.DateTimeField(null=False)

    class Meta:
        managed = False
        db_table = 'server'
