from django.shortcuts import render
from django.http.response import  JsonResponse
from django.http import HttpResponse
import numpy as np
import random
from medical.models import *
from medical.get15DaysTime import date_list
from medical.utils import floatToInt
import datetime
from django.db.models import Avg, Count
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, reverse

# Create your views here.

def login(request):
    return render(request,"login.html")

@csrf_exempt
def checkUser(request):
    uesrname=request.POST.get("username")
    password=request.POST.get("password")
    ps=""
    if uesrname !='' and password!='' :
        un=user.objects.filter(username=uesrname)
        if un.exists():
            ps=list(un)[0].password
            role=list(un)[0].roleId
            if ps==password:
                if role==1:
                    request.session['userPatient']=uesrname
                    return redirect("/patientUser/"+uesrname, )
                if role==0:
                    request.session['userDoctor']=uesrname
                    return redirect("/doctor/"+uesrname, )
    return redirect("/")

def register(request):
    return render(request,"register.html")

@csrf_exempt
def createNewUser(request):
    username=request.POST.get("username")
    password=request.POST.get("password")
    age=request.POST.get("age")
    gender=request.POST.get("gender")
    newUser=user(username=username,password=password,gender=gender,age=age)
    newUser.save()
    return redirect("/")


def patientUser(request,username):
    # 获取username对应的id
    id=list(user.objects.filter(username=username))[0].id
    result=list(indicators.objects.filter(userId=id,createDate__lte=datetime.datetime.now())) #roleid=1 是病人
    data=[]
    i=0
    for d in result:
        arr=[int(d.heartRate),int(d.systolicBloodPressure),int(d.diastolicBloodPressure),int(d.bloodOxygenation),d.createDate.strftime("%Y%m%d")]
        data.insert(i,arr)
        i+=1
    # print(data)
    datetime.date.today()
    return render(request,"patientUser.html",{"username":username,"data":data})

def doctor(request, username, heartRate=None, __lt=None):
    patients=list(user.objects.filter(roleId=1))
    # 男女血压平均数计算
    obj=indicators.objects.filter(userId__gender=1 ,userId__roleId=1).aggregate(
        systolicBloodPressure=Avg('systolicBloodPressure'),
        diastolicBloodPressure=Avg('diastolicBloodPressure'))
    for o in obj:
        obj[o]=int(obj[o])
    dataPressure={}
    dataPressure["male"]=obj
    obj2=indicators.objects.filter(userId__gender=0,userId__roleId=1).aggregate(
        systolicBloodPressure=Avg('systolicBloodPressure'),
        diastolicBloodPressure=Avg('diastolicBloodPressure'))
    for o in obj2:
        obj2[o]=int(obj2[o])

    dataPressure["female"]=obj2

    # 男女心率计算
    obj3={}
    obj3["id06"]=indicators.objects.filter(heartRate__lte=60,userId__gender=1).aggregate(id06=Count("id"))["id06"]
    obj3["id67"]=indicators.objects.filter(heartRate__range=(61,70),userId__gender=1).aggregate(id67=Count("id"))["id67"]
    obj3["id78"]=indicators.objects.filter(heartRate__range=(71,80),userId__gender=1).aggregate(id78=Count("id"))["id78"]
    obj3["id89"]=indicators.objects.filter(heartRate__range=(81,90),userId__gender=1).aggregate(id89=Count("id"))["id89"]
    obj3["id910"]=indicators.objects.filter(heartRate__range=(91,100),userId__gender=1).aggregate(id910=Count("id"))["id910"]
    obj3["id100"]=indicators.objects.filter(heartRate__gt=100,userId__gender=1).aggregate(id100=Count("id"))["id100"]

    obj4={}
    obj4["id06"]=indicators.objects.filter(heartRate__lte=60,userId__gender=0).aggregate(id06=Count("id"))["id06"]
    obj4["id67"]=indicators.objects.filter(heartRate__range=(61,70),userId__gender=0).aggregate(id67=Count("id"))["id67"]
    obj4["id78"]=indicators.objects.filter(heartRate__range=(71,80),userId__gender=0).aggregate(id78=Count("id"))["id78"]
    obj4["id89"]=indicators.objects.filter(heartRate__range=(81,90),userId__gender=0).aggregate(id89=Count("id"))["id89"]
    obj4["id910"]=indicators.objects.filter(heartRate__range=(91,100),userId__gender=0).aggregate(id910=Count("id"))["id910"]
    obj4["id100"]=indicators.objects.filter(heartRate__gt=100,userId__gender=0).aggregate(id100=Count("id"))["id100"]

    #男女血氧计算
    obj5={}
    obj5["id00"] = indicators.objects.filter(bloodOxygenation__lte=90, userId__gender=1).aggregate(id00=Count("id"))["id00"]
    obj5["id05"] = indicators.objects.filter(bloodOxygenation__range=(91, 95), userId__gender=1).aggregate(id05=Count("id"))["id05"]
    obj5["id50"] = indicators.objects.filter(bloodOxygenation__range=(96, 100), userId__gender=1).aggregate(id50=Count("id"))["id50"]

    obj6={}
    obj6["id00"] = indicators.objects.filter(bloodOxygenation__lte=90, userId__gender=0).aggregate(id00=Count("id"))["id00"]
    obj6["id05"] = indicators.objects.filter(bloodOxygenation__range=(91, 95), userId__gender=0).aggregate(id05=Count("id"))["id05"]
    obj6["id50"] = indicators.objects.filter(bloodOxygenation__range=(96, 100), userId__gender=0).aggregate(id50=Count("id"))["id50"]



    return render(request, 'doctor.html', {
                "username":username,
                "patients":patients,
                "dataPressure":dataPressure,
                "rateMale":obj3,
                "rateFemale":obj4,
                "oxyMale":obj5,
                "oxyFemale":obj6})

def searchPatient(request,username):
    return JsonResponse({"username":username})

def insertTestData(request):
    #删除之前所有的数据
    user.objects.filter().delete()
    role.objects.filter().delete()
    indicators.objects.filter().delete()

    # 收缩压的随机数
    systolicRandom=np.random.normal(115,15,150)
    # 舒张压的随机数
    diastolicRandom=np.random.normal(75,10,150)
    #心率的随机数
    rateRandom=np.random.normal(85,15,150)
    #血氧额随机数
    oxyRandom=np.random.normal(93,5,150)

    # 转换成整数
    systolicRandom=list(map(floatToInt,systolicRandom))
    diastolicRandom=list(map(floatToInt,diastolicRandom))
    rateRandom=list(map(floatToInt,rateRandom))
    oxyRandom=list(map(floatToInt,oxyRandom))

    # 病人的随机数
    patientRandom =[]
    doctorRandom=[]
    counter=0
    while counter<10:
        i=1
        name=''
        name2=''
        while i<5:
            name+=random.choice('abcdefghigklmnopqrstuvwxyz')
            name2+=random.choice('abcdefghigklmnopqrstuvwxyz')
            i+=1
        patientRandom.insert(counter,name)
        doctorRandom.insert(counter,name2)
        counter+=1

    # 初始化病人表
    i=0
    while i<10:
        patient=user(username=patientRandom[i],password="123",gender=random.choice([0,1]),
                     age=random.choice([21,22,30,50,60]),description="this is test",roleId=1)
        patient.save()
        doctor=user(username=doctorRandom[i],password="123",gender=random.choice([0,1]),
                    age=random.choice([21,22,30,50,60]),description="this is test",roleId=0)
        doctor.save()
        i+=1

    # 初始化角色表
    i=0
    while i<2:
        roletable=role(roleId=i)
        roletable.save()
        i+=1

    # 初始化病人信息表
    i=0
    while i<10:
        u=user.objects.filter(username=patientRandom[i])
        u=list(u)[0]
        j=i*15
        k = 0
        while j<i*15+15:
            userIndicator=indicators(userId=u,heartRate=rateRandom[j],systolicBloodPressure=systolicRandom[j],
                                     diastolicBloodPressure=diastolicRandom[j],bloodOxygenation=oxyRandom[j],
                                     createDate=date_list[k])
            userIndicator.save()
            j+=1
            k+=1
        i+=1
    return JsonResponse({'patientRandom':patientRandom,'doctor':doctorRandom,'date':date_list})
