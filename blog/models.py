from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Post(models.Model):
    categories = models.ManyToManyField(Category, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250, unique_for_date='date')
    title = models.CharField(max_length=255)
    body = models.TextField()
    likes = models.ManyToManyField(User, related_name='blog_post')
    date = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} by {self.author.username} ({self.categories.name})'

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[str(self.id)])

    @property
    def number_of_comments(self):
        return Comment.objects.filter(post=self).count()


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse('blog:post_list')