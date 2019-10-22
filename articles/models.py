from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.contrib.auth import get_user_model
from django.conf import settings
# Reporter(1) - Article(N)
# reporter - name


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Reporter(models.Model):
    name = models.CharField(max_length=10)


class Article(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    image = models.ImageField(blank=True)
    # ImageSpecField: 인풋 하나만 받고 잘라서 저장
    # ProcessedImageField : 인풋 받은 것을 잘라서 저장
    # resize to fill : 300 * 300
    # resize to fit : 긴쪽을 300에 맞추고 비율에 맞게 자름
    image_thumbnail = ProcessedImageField(
        blank=True,
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 80},
    )

    def __str__(self):
        return f'{self.pk} - {self.title}'

class Comment(models.Model):
    content = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # on_delete
    # 1. CASCADE: 글이 삭제되었을 때 모든 댓글을 삭제
    # 2. PROTECT: 댓글이 존재하면 글 삭제 안됨.
    # 3. SET_NULL : 글이 삭제되면 NULL로 치환(NOT NULL일 경우 사용 불가)
    # 4. SET_DEFAULT : 디폴트 값으로 치환.
