from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import current_user_info
from .views import like_review
from .views import (
    TeacherViewSet,
    StudentAchievementViewSet,
    AlumniReviewViewSet,
    MediaContentViewSet,
    PartnerCompanyViewSet,
    register_user,
)

router = DefaultRouter()
router.register(r'teachers', TeacherViewSet)
router.register(r'achievements', StudentAchievementViewSet)
router.register(r'reviews', AlumniReviewViewSet)
router.register(r'media', MediaContentViewSet)
router.register(r'partners', PartnerCompanyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register_user),
    path('me/', current_user_info),
    path('reviews/<int:pk>/like/', like_review),
]
