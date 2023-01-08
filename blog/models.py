from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import get_object_or_404


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # post_image = models.ImageField(blank=True, upload_to='post_pics')

    def __repr__(self):
        return self.title

    # Django默认修改post之后理论上之后会进入datail页面，但是Django不知道怎么找到detail页面。P10 29:10
    # 为了告诉Django如何找到任何一个instalce
    # 为了在发送post后重定向到post-datail
    # view中的PostUpdateView
    def get_absolute_url(self):
        # reverse 返回一个字符串形式的url
        return reverse('post-detail', kwargs={'pk': self.pk})


class PostImages(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to='post_pics')

    def __repr__(self):
        return str(self.post_id)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commet = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __repr__(self):
        return self.commet[0:50]

    def get_absolute_url(self):
        comment = get_object_or_404(Comment, id=self.pk)
        post_id = comment.post.id
        return reverse('post-detail', kwargs={'pk': post_id})
