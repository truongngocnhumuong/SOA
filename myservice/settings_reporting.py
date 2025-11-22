# myservice/settings_reporting.py
# Cấu hình riêng cho Reporting Service (chạy port 8003)

from .settings import *

# Database riêng cho Reporting Service
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'reporting_db',  # Database riêng
        'USER': 'root',
        'PASSWORD': '1234', 
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Chỉ bật app reports
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'reports',  # CHỈ app reports
]

# URLs của các service khác
PRODUCT_SERVICE_URL = 'http://localhost:8000'
ORDER_SERVICE_URL = 'http://localhost:8000'
AUTH_SERVICE_URL = 'http://localhost:8000'

# REST Framework - Tắt authentication để test
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],
    'UNAUTHENTICATED_USER': None,
}

# Root URLconf riêng
ROOT_URLCONF = 'myservice.urls_reporting'