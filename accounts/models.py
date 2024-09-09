
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # 추가 필드 (닉네임, 생일 등)
    nickname = models.CharField(max_length=30, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username
    
    # 팔로우 ManyToMany 관계
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers')

    def follow(self, user):
        """특정 사용자를 팔로우하는 메서드"""
        self.following.add(user)

    def unfollow(self, user):
        """특정 사용자를 언팔로우하는 메서드"""
        self.following.remove(user)

    def is_following(self, user):
        """팔로우 여부 확인 메서드"""
        return self.following.filter(pk=user.pk).exists()

    def is_followed_by(self, user):
        """팔로우 당했는지 확인하는 메서드"""
        return self.followers.filter(pk=user.pk).exists()
