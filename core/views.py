from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
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
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
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

class CustomAuthToken(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Пожалуйста, предоставьте email и пароль'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response({'error': 'Неверный пароль'}, status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


@api_view(['POST'])
def register_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Требуется email и пароль'}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({'error': 'Пользователь с таким email уже существует'}, status=400)

    user = User.objects.create_user(username=email, email=email, password=password)
    return Response({'message': 'Пользователь создан'}, status=201)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_info(request):
    user = request.user
    return Response({
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