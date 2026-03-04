from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
import random


def register_view(request):
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.district = form.cleaned_data.get('district')
            user.taluk = form.cleaned_data.get('taluk')
            user.village = form.cleaned_data.get('village')
            user.phone_number = form.cleaned_data.get('phone_number')
            user.save()
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form, 'num1': num1, 'num2': num2})


def login_view(request):
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.role == 'main_admin':
                    return redirect('main_admin_dashboard')
                elif user.role == 'sub_admin':
                    return redirect('sub_admin_dashboard')
                else:
                    return redirect('user_dashboard')
            else:
                messages.error(request, 'Invalid credentials!')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form, 'num1': num1, 'num2': num2})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def user_dashboard(request):
    from complaint_mgmt.models import Complaint
    total_complaints = Complaint.objects.filter(user=request.user).count()
    pending_complaints = Complaint.objects.filter(user=request.user, status='pending').count()
    resolved_complaints = Complaint.objects.filter(user=request.user, status='resolved').count()
    emergency_complaints = Complaint.objects.filter(user=request.user, priority='emergency').count()
    recent_complaints = Complaint.objects.filter(user=request.user).order_by('-created_at')[:5]
    return render(request, 'user/dashboard.html', {
        'total_complaints': total_complaints,
        'pending_complaints': pending_complaints,
        'resolved_complaints': resolved_complaints,
        'emergency_complaints': emergency_complaints,
        'recent_complaints': recent_complaints,
    })


@login_required
def sub_admin_dashboard(request):
    if request.user.role != 'sub_admin':
        return redirect('user_dashboard')
    from complaint_mgmt.models import Complaint
    total = Complaint.objects.all().count()
    pending = Complaint.objects.filter(status='pending').count()
    resolved = Complaint.objects.filter(status='resolved').count()
    emergency = Complaint.objects.filter(priority='emergency').count()
    recent = Complaint.objects.all().order_by('-created_at')[:10]
    return render(request, 'sub_admin/dashboard.html', {
        'total': total,
        'pending': pending,
        'resolved': resolved,
        'emergency': emergency,
        'recent': recent,
    })


@login_required
def sub_admin_complaints(request):
    if request.user.role != 'sub_admin':
        return redirect('user_dashboard')
    from complaint_mgmt.models import Complaint
    status_filter = request.GET.get('status', '')
    complaints = Complaint.objects.all().order_by('-created_at')
    if status_filter:
        complaints = complaints.filter(status=status_filter)
    return render(request, 'sub_admin/complaints.html', {
        'complaints': complaints,
        'status_filter': status_filter,
    })


@login_required
def sub_admin_complaint_detail(request, complaint_id):
    if request.user.role != 'sub_admin':
        return redirect('user_dashboard')
    from complaint_mgmt.models import Complaint
    from django.utils import timezone
    complaint = Complaint.objects.get(id=complaint_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        complaint.status = status
        if status == 'resolved':
            complaint.resolved_at = timezone.now()
        complaint.save()
        messages.success(request, 'Complaint status updated!')
        return redirect('sub_admin_complaints')
    return render(request, 'sub_admin/complaint_detail.html', {'complaint': complaint})


@login_required
def main_admin_dashboard(request):
    if request.user.role != 'main_admin':
        return redirect('user_dashboard')
    from complaint_mgmt.models import Complaint, Category
    from django.db.models import Count
    from django.db.models.functions import TruncMonth

    total = Complaint.objects.count()
    closed = Complaint.objects.filter(status='closed').count()
    open_complaints = Complaint.objects.exclude(status__in=['closed', 'resolved']).count()
    resolved = Complaint.objects.filter(status='resolved').count()
    emergency = Complaint.objects.filter(priority='emergency').count()
    pending = Complaint.objects.filter(status='pending').count()
    in_progress = Complaint.objects.filter(status='in_progress').count()

    category_data = list(Complaint.objects.values('category__name').annotate(count=Count('id')))
    district_data = list(Complaint.objects.values('district').annotate(count=Count('id')))
    monthly_data = list(Complaint.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month'))

    return render(request, 'main_admin/dashboard.html', {
        'total': total,
        'closed': closed,
        'open_complaints': open_complaints,
        'resolved': resolved,
        'emergency': emergency,
        'pending': pending,
        'in_progress': in_progress,
        'category_data': category_data,
        'district_data': district_data,
        'monthly_data': monthly_data,
    })


@login_required
def main_admin_complaints(request):
    if request.user.role != 'main_admin':
        return redirect('user_dashboard')
    from complaint_mgmt.models import Complaint
    status_filter = request.GET.get('status', '')
    district_filter = request.GET.get('district', '')
    complaints = Complaint.objects.all().order_by('-created_at')
    if status_filter:
        complaints = complaints.filter(status=status_filter)
    if district_filter:
        complaints = complaints.filter(district=district_filter)
    return render(request, 'main_admin/complaints.html', {
        'complaints': complaints,
        'status_filter': status_filter,
        'district_filter': district_filter,
    })


@login_required
def main_admin_users(request):
    if request.user.role != 'main_admin':
        return redirect('user_dashboard')
    from accounts.models import CustomUser
    users = CustomUser.objects.all().order_by('-date_joined')
    return render(request, 'main_admin/users.html', {'users': users})


@login_required
def main_admin_analytics(request):
    if request.user.role != 'main_admin':
        return redirect('user_dashboard')
    from complaint_mgmt.models import Complaint
    from django.db.models import Count, Q
    from django.db.models.functions import TruncMonth

    category_data = list(Complaint.objects.values('category__name').annotate(
        total=Count('id'),
        resolved=Count('id', filter=Q(status='resolved'))
    ))
    district_data = list(Complaint.objects.values('district').annotate(count=Count('id')).order_by('-count')[:10])
    monthly_data = list(Complaint.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month'))

    return render(request, 'main_admin/analytics.html', {
        'category_data': category_data,
        'district_data': district_data,
        'monthly_data': monthly_data,
    })


@login_required
def main_admin_complaint_detail(request, complaint_id):
    if request.user.role != 'main_admin':
        return redirect('user_dashboard')
    from complaint_mgmt.models import Complaint
    from django.utils import timezone
    complaint = Complaint.objects.get(id=complaint_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        complaint.status = status
        if status == 'resolved':
            complaint.resolved_at = timezone.now()
        complaint.save()
        messages.success(request, 'Complaint status updated!')
        return redirect('main_admin_complaints')
    return render(request, 'main_admin/complaint_detail.html', {'complaint': complaint})