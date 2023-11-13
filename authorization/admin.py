from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from sorl.thumbnail.admin import AdminImageMixin

from .models import CustomUser, WarrantyType, Project, Attribute, SubAttribute, AttributeSubattributePair


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'get_full_name', 'primary_phone', 'secondary_phone', 'is_staff')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('password',)}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'primary_phone', 'secondary_phone', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )


class SubAttributeInline(admin.TabularInline):
    model = SubAttribute


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    inlines = (SubAttributeInline,)


class AttributeSubattributePairInline(admin.TabularInline):
    model = AttributeSubattributePair
    verbose_name = 'Attribute'
    verbose_name_plural = 'Attributes'


@admin.register(Project)
class ProjectAdmin(AdminImageMixin, admin.ModelAdmin):
    inlines = (AttributeSubattributePairInline,)
    fieldsets = (
        (None, {
            'fields': ('name', 'user', 'address', 'start_date', 'end_date', 'cost', 'description', 'cover_image')
        }),
        ('Warranty', {
            'fields': ('warranty_type', 'warranty_start_date', 'warranty_end_date', 'warranty_certificate')
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        """Remove admins from user queryset"""
        form = super().get_form(request, obj, **kwargs)
        field = form.base_fields['user']
        field.queryset = field.queryset.filter(is_staff=False, is_superuser=False)
        return form


@admin.register(WarrantyType)
class WarrantyTypeAdmin(admin.ModelAdmin):
    pass
