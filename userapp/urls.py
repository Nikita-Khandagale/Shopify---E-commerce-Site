from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'userapp'

urlpatterns = [
    path('profile/', views.view_profile, name='view-profile'),
    path('profile/edit/', views.edit_profile, name='edit-profile'),
    path('profile/delete/', views.delete_profile, name='delete-profile'),

    # 👇 Add these (for login, register, logout)
 path(
    'login/',
    auth_views.LoginView.as_view(template_name='registration/login.html'),
    name='login'
 ),
    path('logout/', auth_views.LogoutView.as_view(next_page='app:home'), name='logout'),
    path('register/<str:role>/', views.register, name='register'),

]
