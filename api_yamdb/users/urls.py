from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users import views

v1_router = DefaultRouter()
v1_router.register('users', views.UserViewSet, 'users')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', views.get_confirmation_code),
    path('v1/auth/token/', views.get_token),
]
