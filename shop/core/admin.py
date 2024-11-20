from django.contrib import admin
from .models import User,Profile, Categories, Suppliers, Products, Orders, OrderItems, ShippingAddress
# Register your models here.


class ProfileInline(admin.StackedInline):
    model = Profile


class OrderItemsInline(admin.StackedInline):
    model = OrderItems



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
         'email', 'first_name', 'last_name', 'phone_number', 'date_joined', 'last_login', 'is_active', 'is_staff',
        'is_superuser')
    inlines = [ProfileInline]
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
    

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'slug', 'date_joined', 'updated_at'
    )

    list_filter = ('date_joined', 'updated_at')
    search_fields = ('name', 'slug')
    date_hierarchy = 'date_joined'
    readonly_fields = ('date_joined',)

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.is_staff
    
    def has_delete_permission(self, request, obj = None):
        return request.user.is_superuser or request.user.is_staff
    
    def has_change_permission(self, request, obj = None):
        return request.user.is_superuser or request.user.is_staff
    
    def has_module_permission(self, request, obj= None):
        return request.user.is_superuser or request.user.is_staff
    
    def has_view_permission(self, request, obj = None):
        return request.user.is_superuser or request.user.is_staff
    
    def has_read_permission(self, request, obj= None):
        return request.user.is_superuser or request.user.is_staff
    


@admin.register(Suppliers)
class SupplierAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'first_name', 'last_name', 'date_joined'
    )

    list_filter = ('date_joined',)
    search_fields = ('user', 'first_name', 'last_name', 'date_joined')
    date_hierarchy = 'date_joined'
    readonly_fields = ('user', 'date_joined')

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.is_staff
    
    def has_delete_permission(self, request, obj = None):
        return request.user.is_superuser or request.user.is_staff
    
    def has_change_permission(self, request, obj = None):
        return request.user.is_superuser or request.user.is_staff
    
    def has_module_permission(self, request):
        return request.user.is_superuser or request.user.is_staff
    
    def has_view_permission(self, request, obj = None):
        return request.user.is_superuser or request.user.is_staff
    
    def has_read_permission(self, request, obj= None):
        return request.user.is_superuser or request.user.is_staff
    


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'slug', 'category', 'price', 'is_sale', 'sale_price', 'status',
        'is_suggestion', 'date_added', 'updated_at'
    )

    list_filter = (
        'category', 'is_sale', 'status', 'is_suggestion'
    )

    date_hierarchy = 'date_added'

    search_fields = (
        'name', 'slug', 'price', 'is_sale', 'sale_price', 'status'
    )

    readonly_fields = ('date_added', 'updated_at')

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.is_staff
    
    def has_delete_permission(self, request, obj = None):
        return request.user.is_superuser or request.user.is_staff
    
    def has_change_permission(self, request, obj = None):
        return request.user.is_superuser or request.user.is_staff
    
    def has_module_permission(self, request):
        return request.user.is_superuser or request.user.is_staff
    
    def has_view_permission(self, request, obj = None):
        return request.user.is_superuser or request.user.is_staff
    
    def has_read_permission(self, request, obj= None):
        return request.user.is_superuser or request.user.is_staff
    


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'full_name', 'city', 'shipping_address', 'amount_paid', 'shipped',
        'date_shipped', 'status','id'
    )

    inlines = [OrderItemsInline]
    list_filter = (
        'city', 'shipped', 'status'
    )

    search_fields = ('fullname', 'city', 'shipping_address', 'status')
    readonly_fields = ('date_shipped',)

    def has_add_permission(self, request):
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj = None):
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj = None):
        return request.user.is_superuser or request.user.is_staff
    
    def has_module_permission(self, request):
        return request.user.is_superuser or request.user.is_staff
    
    def has_view_permission(self, request, obj = None):
        return request.user.is_superuser or request.user.is_staff
    
    def has_read_permission(self, request, obj= None):
        return request.user.is_superuser or request.user.is_staff
        

class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'city' ,'postal_code_1', 'postal_code_2'
    ]

    list_filter = ('city',)
    search_fields = ('city','postal_code_1','postal_code_2')
    readonly_fields = ('user')

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.is_staff
    
    def has_change_permission(self, request, obj = None):
        return request.user.is_superuser or request.user.is_staff
    
    def has_delete_permission(self, request, obj = None):
        return request.user.is_superuser or request.user.is_staff
    
    def has_module_permission(self, request):
        return request.user.is_superuser or request.user.is_staff
    
    def has_view_permission(self, request, obj = None):
        return request.user.is_superuser or request.user.is_staff
    
    def has_read_permission(self, request, obj= None):
        return request.user.is_superuser or request.user.is_staff
    


admin.site.register(ShippingAddress)