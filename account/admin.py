from django.contrib import admin
from .models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'telephone', 'company', 'country', 'service', 'service_expire')
    ordering = ('username', )

admin.site.register(User, UserAdmin)
