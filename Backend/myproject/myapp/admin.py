from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Organization, Role, User

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_at')
    search_fields = ('name', 'description')

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'organization')
    search_fields = ('name', 'description')
    list_filter = ('organization',)

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'email', 'organization', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('organization', 'roles', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('organization', 'roles')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'organization', 'password1', 'password2'),
        }),
    )
    ordering = ('email',)
    filter_horizontal = ('roles', 'groups', 'user_permissions')

admin.site.register(User, CustomUserAdmin)