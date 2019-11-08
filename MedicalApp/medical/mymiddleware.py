
from django.shortcuts import HttpResponseRedirect, redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

class Middlerware1(MiddlewareMixin):
    def process_request(self,request):
        url = ['/register/','/','/checkUser/','/admin/','/admin/login/','/createNewUser/','/insertTestData/']  # 请求白名单
        if request.path in url or request.path.startswith('/admin'):
            return None
        else:
            bb=request.session.get('userPatient',None)
            username=request.path.split('/')[2]
            if bb != None and bb==username :
                return None
            elif bb!=None:
                bb = request.session.get("userDoctor")
                return None
        return HttpResponseRedirect('/')