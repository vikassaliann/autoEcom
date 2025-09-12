from django.contrib import admin
from django.urls import path
from tracker import views as tracker_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('', tracker_views.product_list, name='product_list'),
    path('product/<int:product_id>/delete/', tracker_views.product_delete, name='product_delete'),
]