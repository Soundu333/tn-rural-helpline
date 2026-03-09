#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py shell -c "
from django.contrib.auth import get_user_model
from complaint_mgmt.models import Category, SubCategory

User = get_user_model()
if not User.objects.filter(username='mainadmin').exists():
    u = User(username='mainadmin', email='msoundharya40@gmail.com', role='main_admin', phone_number='7845488475')
    u.set_password('Admin@1234')
    u.is_superuser = True
    u.is_staff = True
    u.save()
    print('Superuser created!')

categories = [
    ('Road', 'சாலை', [('Pothole', 'குழி'), ('Bridge Damage', 'பாலம் சேதம்'), ('Road Widening', 'சாலை விரிவாக்கம்'), ('Street Light', 'தெரு விளக்கு'), ('Drainage', 'வடிகால்')]),
    ('Health', 'சுகாதாரம்', [('Hospital Facility', 'மருத்துவமனை வசதி'), ('Medicine Shortage', 'மருந்து பற்றாக்குறை'), ('Ambulance', 'ஆம்புலன்ஸ்'), ('Doctor Absence', 'மருத்துவர் வருகை இல்லை')]),
    ('Water Supply', 'குடிநீர்', [('No Water Supply', 'தண்ணீர் வரவில்லை'), ('Pipe Leakage', 'குழாய் கசிவு'), ('Water Quality', 'தண்ணீர் தரம்'), ('New Connection', 'புதிய இணைப்பு')]),
    ('Electricity', 'மின்சாரம்', [('Power Cut', 'மின்தடை'), ('Transformer Issue', 'மின்மாற்றி பிரச்சனை'), ('New Connection', 'புதிய இணைப்பு'), ('Street Light', 'தெரு விளக்கு')]),
    ('Agriculture', 'விவசாயம்', [('Crop Damage', 'பயிர் சேதம்'), ('Fertilizer', 'உரம்'), ('Irrigation', 'நீர்ப்பாசனம்'), ('Loan', 'கடன்')]),
    ('Police', 'காவல்துறை', [('Theft', 'திருட்டு'), ('Assault', 'தாக்குதல்'), ('Missing Person', 'காணாமல் போனவர்'), ('Harassment', 'தொல்லை')]),
    ('Revenue', 'வருவாய்', [('Land Issue', 'நில பிரச்சனை'), ('Patta', 'பட்டா'), ('Encroachment', 'ஆக்கிரமிப்பு'), ('Certificate', 'சான்றிதழ்')]),
    ('Education', 'கல்வி', [('School Facility', 'பள்ளி வசதி'), ('Teacher Absence', 'ஆசிரியர் வருகை இல்லை'), ('Scholarship', 'உதவித்தொகை'), ('Mid Day Meal', 'மதிய உணவு')]),
    ('Ration Shop', 'ரேஷன் கடை', [('Stock Shortage', 'பொருட்கள் இல்லை'), ('Quality Issue', 'தரக்குறைபாடு'), ('New Card', 'புதிய அட்டை'), ('Wrong Entry', 'தவறான பதிவு')]),
    ('Panchayat', 'பஞ்சாயத்து', [('Road', 'சாலை'), ('Drainage', 'வடிகால்'), ('Drinking Water', 'குடிநீர்'), ('Building', 'கட்டிடம்')]),
]

for cat_name, cat_tamil, subcats in categories:
    cat, created = Category.objects.get_or_create(name=cat_name, defaults={'name_tamil': cat_tamil})
    for sub_name, sub_tamil in subcats:
        SubCategory.objects.get_or_create(category=cat, name=sub_name, defaults={'name_tamil': sub_tamil})

print('Categories and subcategories created!')
"