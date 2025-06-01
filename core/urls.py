from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from .views import current_user_info
from .views import like_review
from .views import (
    HistoryViewSet,
    StudentAchievementViewSet,
    AlumniReviewViewSet,
    MediaContentViewSet,
    PartnerCompanyViewSet,
    register_user,
)

router = DefaultRouter()
router.register(r'history', HistoryViewSet)
router.register(r'achievements', StudentAchievementViewSet)
router.register(r'reviews', AlumniReviewViewSet)
router.register(r'media', MediaContentViewSet, basename='media')
router.register(r'partners', PartnerCompanyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register_user),
    path('me/', current_user_info),
    path('reviews/<int:pk>/like/', like_review),
    path('api/', include(router.urls)),
    path('', views.index, name='index'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

