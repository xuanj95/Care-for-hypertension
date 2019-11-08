from django.db import models

# Create your models here.
class user(models.Model):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=20)
    gender=models.BooleanField() # 1. 男性 0 女性
    age=models.IntegerField()
    description=models.CharField(max_length=200,null=True)
    roleId=models.IntegerField(null=True)

    def _str_(self):
        return "%s" % self.username

class role(models.Model):
    roleId = models.BooleanField(); # 1 病人 0 医生

    def _str_(self):
        return "%s" % self.roleId

class indicators(models.Model):
    # userId=models.IntegerField()
    userId=models.ForeignKey(user,related_name="user",null=True,on_delete=models.SET_NULL)
    # heartRate=models.CharField(max_length=20,null=True)
    heartRate=models.IntegerField(null=True)
    # systolicBloodPressure=models.CharField(max_length=20,null=True)
    systolicBloodPressure=models.IntegerField(null=True)
    # diastolicBloodPressure=models.CharField(max_length=20,null=True)
    diastolicBloodPressure=models.IntegerField(null=True)
    # bloodOxygenation=models.CharField(max_length=20,null=True)
    bloodOxygenation=models.IntegerField(null=True)
    # createDate=models.DateField(auto_created=True,auto_now=True);
    createDate = models.DateField(); # 方便测试，不自动产生

    def _str_(self):
        return "%s" % self.userId__username


