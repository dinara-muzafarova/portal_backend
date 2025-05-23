from django.db import models

class Teacher(models.Model):
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

class MediaContent(models.Model):
    title = models.CharField(max_length=255)
    media_type = models.CharField(max_length=10, choices=[('photo', 'Photo'), ('video', 'Video')])
    file = models.FileField(upload_to='media/')
    description = models.TextField(blank=True)

class PartnerCompany(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    logo = models.ImageField(upload_to='partners/')
