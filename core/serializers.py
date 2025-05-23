from rest_framework import serializers
from .models import Teacher, StudentAchievement, AlumniReview, MediaContent, PartnerCompany

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class StudentAchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAchievement
        fields = '__all__'

class AlumniReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlumniReview
        fields = '__all__'

class MediaContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaContent
        fields = '__all__'

class PartnerCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerCompany
        fields = '__all__'
