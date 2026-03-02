#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='mainadmin').exists():
    u = User.objects.create_superuser('mainadmin', 'msoundharya40@gmail.com', 'Admin@1234')
    u.role = 'main_admin'
    u.save()
    print('Superuser created!')
"