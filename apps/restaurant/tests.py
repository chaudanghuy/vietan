from django.test import TestCase
from .models import User
from django.http.response import HttpResponse
from . import helpers

# Create your tests here.
# Test
def create_test_user(request):
    user = User.objects.create_user(username='demo', password='123')
    
    user.first_name = 'Alice'
    user.last_name = 'Firstimer'
    user.save()
    return HttpResponse("Test user created.")