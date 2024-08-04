from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Incident
from .serializers import *
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny


class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        print(f"Request data: {request.data}")
        return super().post(request, *args, **kwargs)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })

class IncidentListCreateView(generics.ListCreateAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(reporter=self.request.user)

class IncidentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        incident = get_object_or_404(self.queryset, pk=self.kwargs['pk'], reporter=self.request.user)
        if incident.status == 'Closed':
            self.permission_denied(self.request, message="Closed incidents cannot be edited.")
        return incident

class IncidentSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, incident_id):
        incident = get_object_or_404(Incident, incident_id=incident_id, reporter=request.user)
        serializer = IncidentSerializer(incident)
        return Response(serializer.data)
    
    
    
from django.shortcuts import render

def register(request):
    return render(request, 'register.html.j2')

def login(request):
    return render(request, 'login.html.j2')

def forgot_password(request):
    return render(request, 'forgot-password.html.j2')

from django.views.decorators.http import require_GET
from django.http import JsonResponse
import requests
from django.contrib.auth.decorators import login_required


@require_GET
def get_location(request):
    pincode = request.GET.get('pincode')
    if pincode:
        # Using a placeholder API for demonstration purposes
        response = requests.get(f'http://api.zippopotam.us/in/{pincode}')
        if response.status_code == 200:
            data = response.json()
            city = data['places'][0]['place name']
            country = data['country']
            return JsonResponse({'city': city, 'country': country})
    return JsonResponse({'error': 'Invalid pin code'}, status=400)    


@login_required
def incident_page(request):
    return render(request, 'incident_page.html.j2')