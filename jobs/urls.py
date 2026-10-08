from django.urls import path
from django.contrib.auth import views as auth
from . import views
urlpatterns=[path('',views.dashboard,name='dashboard'),path('signup/',views.signup,name='signup'),path('login/',auth.LoginView.as_view(),name='login'),path('logout/',auth.LogoutView.as_view(),name='logout'),path('applications/new/',views.application_form,name='add'),path('applications/<int:pk>/edit/',views.application_form,name='edit'),path('applications/<int:pk>/delete/',views.delete_application,name='delete'),path('export/',views.export_csv,name='export')]
