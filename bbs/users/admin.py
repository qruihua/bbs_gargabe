from django.contrib import admin
from users.models import User
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','username','password']
    list_per_page = 20
admin.site.register(User,UserAdmin)


