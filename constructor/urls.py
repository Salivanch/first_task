from django.urls import path
from .views import LandingPage,LoginPage,RegistrationPage,LogoutPage,СonfirmationAccount,UserStats,Question

urlpatterns = [
    path('',LandingPage.as_view(),name='landing'),
    path('user/question',Question.as_view(),name='question'),
    path('user/stats',UserStats.as_view(),name="stats"),
    path('user/login',LoginPage.as_view(),name='login'),
    path('user/registration',RegistrationPage.as_view(),name="registration"),
    path('user/logout',LogoutPage.as_view(),name="logout"),
    path('user/confirm/token/<slug>',СonfirmationAccount.as_view(),name="confirm"),
]