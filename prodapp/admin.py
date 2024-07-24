"""
from django.contrib import admin
from .models import Order, Part, Component, PartComponent
class OrderAdmin(admin.ModelAdmin):
    list_display = ('part_no', 'serial_number', 'created_by', 'created_at')  # Dodane pole

admin.site.register(Order, OrderAdmin)
admin.site.register(Part)
admin.site.register(Component)
admin.site.register(PartComponent)
"""

from django.contrib import admin
from .models import Order, Part, Component, PartComponent

def delete_selected(modeladmin, request, queryset):
    queryset.delete()
delete_selected.short_description = "Usuń zaznaczone obiekty"

class OrderAdmin(admin.ModelAdmin):
    list_display = ('part_no', 'serial_number', 'created_by', 'created_at')  # Dodane pole
    actions = [delete_selected]  # Dodaj akcję do listy akcji

admin.site.register(Order, OrderAdmin)
admin.site.register(Part)
admin.site.register(Component)
admin.site.register(PartComponent)