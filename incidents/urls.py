from django.urls import path
from .views import *
urlpatterns = [
    path('api/register/', RegisterUserView.as_view(), name='register-user'),
    path('api/login/', LoginView.as_view(), name='login-user'),
    path('api/incidents/', IncidentListCreateView.as_view(), name='incident-list-create'),
    path('api/incidents/<int:pk>/', IncidentDetailView.as_view(), name='incident-detail'),
    path('api/incidents/search/<str:incident_id>/', IncidentSearchView.as_view(), name='incident-search'),

    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('incident/', incident_page, name='incident-page'),

    path('forgot-password/', forgot_password, name='forgot_password'),
    path('get-location/', get_location, name='get_location'),

]



