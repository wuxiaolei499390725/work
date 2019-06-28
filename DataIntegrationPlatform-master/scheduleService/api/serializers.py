from django.contrib.auth.models import User, Group
from rest_framework import serializers

# Serializers define the API representation.
from api.models import Task, TaskLog, TaskStatus, EtlServer, Server


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ('taskId', 'taskName', 'executionType', 'taskType', 'scheduleType', 'startExecuteDate', 'enabled', 'preConditionType')


class TaskStatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TaskStatus
        fields = (
        'taskid', 'lastsucceededexecutedateid', 'lastexecutedateid', 'starttime', 'completetime', 'errorcount',
        'status', 'errorinfo')


class EtlServerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EtlServer
        fields = ('ipaddress', 'etlservername', 'packagerootpath', 'enabled', 'lastupdatetime')


class TaskLogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TaskLog
        fields = ('tasklogid', 'taskid', 'taskname', 'etlserverip', 'packagepath', 'dcdate', 'issuccess', 'errorinfo',
                  'starttime', 'completetime', 'isreload')

   
# class briefInfoSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = briefinfo
#         fields = "__all__"
#         depth = 1

class ServerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Server
        fields = ('server_id', 'server_ip', 'server_name', 'business', 'desc', 'enabled')
