from django.urls import path
from .views import validate_and_process_request

urlpatterns = [
    path('process/', validate_and_process_request, name='process')
]
