from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('sub-admin/dashboard/', views.sub_admin_dashboard, name='sub_admin_dashboard'),
    path('sub-admin/complaints/', views.sub_admin_complaints, name='sub_admin_complaints'),
    path('sub-admin/complaint/<int:complaint_id>/', views.sub_admin_complaint_detail, name='sub_admin_complaint_detail'),
    path('main-admin/dashboard/', views.main_admin_dashboard, name='main_admin_dashboard'),
    path('main-admin/complaints/', views.main_admin_complaints, name='main_admin_complaints'),
    path('main-admin/complaint/<int:complaint_id>/', views.main_admin_complaint_detail, name='main_admin_complaint_detail'),
    path('main-admin/users/', views.main_admin_users, name='main_admin_users'),
    path('main-admin/analytics/', views.main_admin_analytics, name='main_admin_analytics'),
]