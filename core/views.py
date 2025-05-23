from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Teacher, StudentAchievement, AlumniReview, MediaContent, PartnerCompany
from .serializers import (
    TeacherSerializer,
    StudentAchievementSerializer,
    AlumniReviewSerializer,
    MediaContentSerializer,
    PartnerCompanySerializer
)
class AlumniReviewViewSet(viewsets.ModelViewSet):
    queryset = AlumniReview.objects.all()
    serializer_class = AlumniReviewSerializer
    permission_classes = [AllowAny]

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class StudentAchievementViewSet(viewsets.ModelViewSet):
    queryset = StudentAchievement.objects.all()
    serializer_class = StudentAchievementSerializer

class MediaContentViewSet(viewsets.ModelViewSet):
    queryset = MediaContent.objects.all()
    serializer_class = MediaContentSerializer

class PartnerCompanyViewSet(viewsets.ModelViewSet):
    queryset = PartnerCompany.objects.all()
    serializer_class = PartnerCompanySerializer

@api_view(['POST'])
def register_user(request):
    print("Вызван register_user")
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Требуется имя пользователя и пароль'}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Пользователь уже существует'}, status=400)

    User.objects.create_user(username=username, password=password)
    return Response({'message': 'Пользователь создан'}, status=201)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_info(request):
    user = request.user
    return Response({
        "username": user.username,
        "email": user.email,
    })

@api_view(['POST'])
def like_review(request, pk):
    try:
        review = AlumniReview.objects.get(pk=pk)
        review.likes += 1
        review.save()
        return Response({'likes': review.likes}, status=200)
    except AlumniReview.DoesNotExist:
        return Response({'error': 'Отзыв не найден'}, status=404)