from django.contrib import admin
from .models import Category, SubCategory, Complaint

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'name_tamil', 'department', 'sla_days']

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['category', 'name', 'name_tamil']

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['ticket_id', 'title', 'status', 'priority', 'district', 'created_at']
    list_filter = ['status', 'priority', 'district']
    search_fields = ['ticket_id', 'title']