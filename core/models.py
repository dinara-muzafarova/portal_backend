from django.db import models
from django.contrib.auth.models import User

class History(models.Model):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='teachers/')
    achievements = models.TextField()

class StudentAchievement(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    year = models.IntegerField()

class AlumniReview(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField()
    graduation_year = models.IntegerField()
    photo = models.ImageField(upload_to='review_photos/', blank=True, null=True)
    likes = models.PositiveIntegerField(default=0)
    is_approved = models.BooleanField(default=False)

    def get_queryset(self):
        return AlumniReview.objects.filter(is_approved=True)


class MediaContent(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('photo', 'Фото'),
        ('video', 'Видео'),
    ]

    title = models.CharField(max_length=255, blank=True)
    media_type = models.CharField(max_length=5, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(upload_to='media/')
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title or "Без названия"

    class Meta:
        ordering = ['-uploaded_at']  # Сортировка по времени загрузки (по убыванию)

class PartnerCompany(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    logo = models.ImageField(upload_to='partners/')

class GalleryImage(models.Model):
    title = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title or "Фото без названия"