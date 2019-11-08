from django.contrib import admin
from .models import user,role,indicators

class UserAdmin(admin.ModelAdmin):
    list_display = ["username","password","gender","age","description","roleId"]
    search_fields = ('username',)

class RoleAdmin(admin.ModelAdmin):
    list_display = ["roleId",]

class IndicatorsAdmin(admin.ModelAdmin):
    list_display = ("userId__username","heartRate","systolicBloodPressure","diastolicBloodPressure","bloodOxygenation","createDate")
    search_fields = ("userId__username",)
    def userId__username(self,obj):
        return obj.userId.username

admin.site.register(user,UserAdmin)
admin.site.register(role,RoleAdmin)
admin.site.register(indicators,IndicatorsAdmin)
# Register your models here.
