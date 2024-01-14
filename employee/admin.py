from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea, CharField
from django import forms
from django.db import models

# Register your models here.
from .models import Employee, PhoneNumber
admin.site.register(PhoneNumber)

class EmployeeAdmin(UserAdmin):
    """
    Custom Admin Configuration for the Employee Model.

    This class extends the UserAdmin class provided by Django to customize the appearance
    and behavior of the Employee model in the Django Admin interface.

    Attributes:
    - model (Employee): The Employee model to be managed.
    - list_display (tuple): The fields to be displayed in the list view.
    - fieldsets (tuple): The configuration of the fieldsets in the detail view.

    Usage:
    - Register the Employee model with this admin configuration in the Django Admin interface.
    """
    model = Employee
    list_display = ('username', 'email', 'salary', 'position', 'address')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('salary', 'position', 'address')}),
    )

admin.site.register(Employee, EmployeeAdmin)



# class UserAdminConfig(UserAdmin):
#     model = Employee
#     search_fields = ('name', 'salary', 'position',)
#     list_filter = ('name', 'salary', 'position', 'address')
#     ordering = ('name',)
#     list_display = ('name', 'salary', 'position', 'address')
#     fieldsets = (
#         (None, {'fields': ('name', 'salary', 'position', 'address')}),
#         ('Permissions', {'fields': ('is_staff', 'is_active')}),
#     )
#     formfield_overrides = {
#         models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
#     }
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('name', 'salary', 'position', 'address', 'password1', 'password2', 'is_active', 'is_staff')}
#          ),
#     )

# admin.site.register(Employee, UserAdminConfig)