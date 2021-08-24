from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Role(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    username = models.CharField(max_length=150,
                                unique=True,
                                null=True,
                                blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30,  blank=True)
    bio = models.TextField(blank=True)
    email = models.EmailField(unique=True,
                              null=False,
                              blank=False)
    role = models.CharField(max_length=30, choices=Role.choices, default=Role.USER)

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f'{self.slug}'


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f'{self.slug}'


class Title(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    category = models.ForeignKey(Category,
                                 related_name='titles',
                                 on_delete=models.SET_NULL,
                                 null=True)
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return f'{self.title}'


class Review(models.Model):
    title_id = models.ForeignKey(Title,
                                 related_name='reviews',
                                 on_delete=models.CASCADE,
                                 null=False)
    text = models.TextField()
    author = models.ForeignKey(User,
                               related_name='reviews',
                               on_delete=models.CASCADE,
                               null=False)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    pub_date = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    review_id = models.ForeignKey(Review,
                                  related_name='comments',
                                  on_delete=models.CASCADE,
                                  null=False)
    text = models.TextField()
    author = models.ForeignKey(User,
                               related_name='comments',
                               on_delete=models.CASCADE,
                               null=False)
    pub_date = models.DateTimeField(auto_now=True)











