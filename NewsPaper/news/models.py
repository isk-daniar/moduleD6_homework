from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django import forms
from django.contrib.auth.forms import UserCreationForm


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rating = Post.objects.filter(author=self).aggregate(Sum('rating')).get('rating__sum')
        comment_rating  = Comment.objects.filter(user=self.user).aggregate(Sum('rating')).get('rating__sum')
        comment_post_rating = Comment.objects.filter(post__author=self).aggregate(Sum('rating')).get('rating__sum')
        self.rating = post_rating * 3 + comment_rating + comment_post_rating
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)


class Post(models.Model):
    news = 'NW'
    article = 'AR'

    TYPE_POST = [
        (news, 'Новость'),
        (article, 'Статья')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=TYPE_POST, default=article)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=250)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )


class Mailing(models.Model):
    date = models.DateField(
        default=datetime.utcnow,
    )
    client_name = models.CharField(
        max_length=200
    )
    message = models.TextField()

    def __str__(self):
        return f'{self.client_name}: {self.message}'