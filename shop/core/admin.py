from django.contrib import admin
from .models import User
# Register your models here.



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
         'email', 'first_name', 'last_name', 'phone_number', 'date_joined', 'last_login', 'is_active', 'is_staff',
        'is_superuser')
    list_filter = ('date_joined', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    date_hierarchy = 'date_joined'
    readonly_fields = ('date_joined', 'last_login')

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_module_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

    def has_read_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff