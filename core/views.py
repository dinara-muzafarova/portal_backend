from django.http import JsonResponse
from django.shortcuts import render
import threading
import asyncio
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from bot import send_gallery_image
from bot import send_new_review
from .serializers import MediaContentSerializer
from rest_framework import status
from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import History, StudentAchievement, AlumniReview, MediaContent, PartnerCompany
from .serializers import (
    HistorySerializer,
    StudentAchievementSerializer,
    AlumniReviewSerializer,
    MediaContentSerializer,
    PartnerCompanySerializer
)
class AlumniReviewViewSet(viewsets.ModelViewSet):
    queryset = AlumniReview.objects.filter(is_approved=True)
    serializer_class = AlumniReviewSerializer
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        review = serializer.save()
        def run_async_task():
            asyncio.run(send_new_review(review))

        threading.Thread(target=run_async_task).start()

class HistoryViewSet(viewsets.ModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer

class StudentAchievementViewSet(viewsets.ModelViewSet):
    queryset = StudentAchievement.objects.all()
    serializer_class = StudentAchievementSerializer

class MediaContentViewSet(viewsets.ModelViewSet):
    queryset = MediaContent.objects.filter(is_approved=True).order_by('-uploaded_at')
    serializer_class = MediaContentSerializer
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        media = serializer.save()

        def run_async_task():
            asyncio.run(send_gallery_image(media))

        threading.Thread(target=run_async_task).start()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(response.data, status=201)

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


def index(request):
    return render(request, 'index.html')