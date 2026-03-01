from django.db import models
from accounts.models import CustomUser
import uuid

class Category(models.Model):
    name = models.CharField(max_length=100)
    name_tamil = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    sla_days = models.IntegerField(default=7)
    keywords = models.TextField(blank=True)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    name_tamil = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class Complaint(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
        ('escalated', 'Escalated'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('emergency', 'Emergency'),
    ]
    ticket_id = models.CharField(max_length=20, unique=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='complaints')
    
    # Personal Info
    name = models.CharField(max_length=200, blank=True)
    address = models.TextField(blank=True)
    mobile = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    
    # Location
    district = models.CharField(max_length=100, blank=True)
    block = models.CharField(max_length=100, blank=True)
    panchayat = models.CharField(max_length=100, blank=True)
    habitation = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Complaint Info
    mm_reference = models.CharField(max_length=50, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # File uploads
    document = models.FileField(upload_to='complaint_docs/', null=True, blank=True)
    photo = models.ImageField(upload_to='complaint_photos/', null=True, blank=True)
    voice_file = models.FileField(upload_to='voice_complaints/', null=True, blank=True)
    
    # Status & Priority
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    # AI Fields
    ai_category = models.CharField(max_length=100, null=True, blank=True)
    is_duplicate = models.BooleanField(default=False)
    duplicate_of = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    
    # Assignment
    assigned_to = models.ForeignKey(CustomUser, null=True, blank=True, related_name='assigned_complaints', on_delete=models.SET_NULL)
    sla_deadline = models.DateTimeField(null=True, blank=True)
    sla_breached = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.ticket_id:
            self.ticket_id = 'TN' + str(uuid.uuid4()).upper()[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ticket_id} - {self.title}"