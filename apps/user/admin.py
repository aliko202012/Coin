from django.contrib import admin
from .models import User
# Register your models here.
@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['id','username','balance']
    search_fields = ['id','username']