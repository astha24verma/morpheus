from django.urls import path
from django.contrib.auth import views as auth_views
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('', views.form_list, name='form_list'),
    path('api/forms/create/', views.api_form_create, name='api_form_create'),
    path('forms/create/', views.web_form_create, name='web_form_create'),
    path('api/forms/<int:form_id>/edit/', views.api_form_edit, name='api_form_edit'),
    path('forms/<int:form_id>/edit/', views.web_form_edit, name='web_form_edit'),
    path('api/forms/<int:form_id>/submit/', views.api_form_submit, name='api_form_submit'),
    path('forms/<int:form_id>/submit/', views.web_form_submit, name='web_form_submit'),
    path('api/forms/<int:form_id>/analytics/', views.api_form_analytics, name='api_form_analytics'),
    path('forms/<int:form_id>/analytics/', views.web_form_analytics, name='web_form_analytics'),
    path('forms/<int:form_id>/thank-you/', views.form_thank_you, name='form_thank_you'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='form_list'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]


