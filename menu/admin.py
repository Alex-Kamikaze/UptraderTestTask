from django.contrib import admin
from .models import Menu, MenuItem

class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
    fields = ['title', 'parent', 'url', 'named_url', 'order']

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    inlines = [MenuItemInline]

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'menu', 'parent', 'url', 'named_url', 'order')
    list_filter = ('menu',)
    list_editable = ('order',)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            obj_id = request.resolver_match.kwargs.get('object_id')
            if obj_id:
                obj = MenuItem.objects.get(id=obj_id)
                kwargs["queryset"] = MenuItem.objects.filter(menu=obj.menu)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)