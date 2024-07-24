from django.urls import path, include
from . import views
from .views import LoginView

urlpatterns = [
    path('add_order/', views.add_order, name='add_order'),
    path('part/<str:part_no>/scan/<str:serial_number>/', views.scan_components, name='scan_components'),
    path('part/<str:part_no>/scan/<str:serial_number>/remove/<int:component_id>/', views.remove_component, name='remove_component'),
    path('part/<str:part_no>/scan/<str:serial_number>/complete/', views.complete_order, name='complete_order'),
    path('generate_pdf/<str:part_no>/<str:serial_number>/', views.generate_pdf, name='generate_pdf'),
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('', views.home, name='home'),  # Dodanie URL-a do strony głównej aplikacji prodapp
    path('login/', LoginView.as_view(), name='login'),

]