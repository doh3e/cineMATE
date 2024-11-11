from django.urls import path
from . import views


app_name = "accounts"
urlpatterns = [
    path('sign-up/', views.signup, name="sign_up"),
    path('log-in/', views.login, name="log_in"),
    path('log-out/', views.logout, name="log_out"),
]