from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_complaint, name='register_complaint'),
    path('my-complaints/', views.my_complaints, name='my_complaints'),
    path('get-subcategories/', views.get_subcategories, name='get_subcategories'),
    path('admin/complaint/<int:id>/', views.admin_complaint_detail, name='admin_complaint_detail'),
]