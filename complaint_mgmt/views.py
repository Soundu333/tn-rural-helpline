from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Complaint, Category, SubCategory

@login_required
def register_complaint(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        sub_category_id = request.POST.get('sub_category')
        priority = request.POST.get('priority')
        district = request.POST.get('district')
        block = request.POST.get('block')
        panchayat = request.POST.get('panchayat')
        habitation = request.POST.get('habitation')
        name = request.POST.get('name')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        mm_reference = request.POST.get('mm_reference')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        category = Category.objects.get(id=category_id) if category_id else None
        sub_category = SubCategory.objects.get(id=sub_category_id) if sub_category_id else None

        complaint = Complaint.objects.create(
            user=request.user,
            title=title,
            description=description,
            category=category,
            sub_category=sub_category,
            priority=priority,
            district=district,
            block=block,
            panchayat=panchayat,
            habitation=habitation,
            name=name,
            address=address,
            mobile=mobile,
            email=email,
            mm_reference=mm_reference,
            latitude=latitude if latitude else None,
            longitude=longitude if longitude else None,
        )

        if 'document' in request.FILES:
            complaint.document = request.FILES['document']
        if 'photo' in request.FILES:
            complaint.photo = request.FILES['photo']
        complaint.save()

        messages.success(request, f'Complaint registered! Ticket ID: {complaint.ticket_id}')
        return redirect('my_complaints')
    return render(request, 'user/register_complaint.html', {'categories': categories})

@login_required
def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(category_id=category_id).values('id', 'name', 'name_tamil')
    return JsonResponse({'subcategories': list(subcategories)})

@login_required
def my_complaints(request):
    complaints = Complaint.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user/my_complaints.html', {'complaints': complaints})