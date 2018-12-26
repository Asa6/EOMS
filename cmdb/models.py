from django.db import models

# Create your models here.

class Role(models.Model):
    role_name = models.CharField(max_length=32, null=True)

class UserInfo(models.Model):
    # id列，自增， 主键（自动创建）
    email = models.CharField(max_length=32)
    #username = models.CharField(max_length=32,null=True)
    password = models.CharField(max_length=64)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)

class Business(models.Model):
    name = models.CharField(max_length=32, null=True)

class Host_Status(models.Model):
    name = models.CharField(max_length=32, null=True)
    color = models.CharField(max_length=32, null=True)
    describe = models.CharField(max_length=16, null=True)
    iconstyle = models.CharField(max_length=64, null=True)

class Hosts(models.Model):
    hostname = models.CharField(max_length=128, null=True)   #  null =True 表示可以为空
    ip = models.GenericIPAddressField(unique=True, null=True)   # unique 表示唯一值
    port = models.PositiveIntegerField(null=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True)
    status = models.ForeignKey(Host_Status, on_delete=models.CASCADE, null=True)
