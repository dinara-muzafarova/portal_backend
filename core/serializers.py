from rest_framework import serializers
from .models import History, StudentAchievement, AlumniReview, MediaContent, PartnerCompany

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'

class StudentAchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAchievement
        fields = '__all__'

class AlumniReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlumniReview
        fields = '__all__'
        read_only_fields = ('is_approved', 'likes')

class MediaContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaContent
        fields = ['id', 'title', 'media_type', 'file', 'description', 'uploaded_at', 'user']
        read_only_fields = ['uploaded_at', 'user']

class PartnerCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerCompany
        fields = '__all__'
