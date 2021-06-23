import django.contrib.auth.models
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class User (AbstractUser):
    avatar = models.ImageField(default="static/img/ava.jpg", upload_to="static/upload/", verbose_name="avatar")

    def __str__(self):
        return self.username


class TagManager(models.Manager):
    def question_by_tag(self, name_tag):
        return self.filter(name=name_tag).first().questions.all().order_by('date').reverse()


class Tag (models.Model):
    name = models.CharField(max_length=255, verbose_name='Tag')

    objects = TagManager()

    def __str__(self):
        return self.name


class Like (models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    content_type = models.ForeignKey(ContentType, default=None, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(default=-1)
    content_object = GenericForeignKey()


class QuestionManager(models.Manager):
    def most_popular(self):
        return self.all().order_by('rating').reverse()

    def newest(self):
        return self.all().order_by('date').reverse()

    def by_id(self, qid):
        return self.all().filter(id=qid)

    def by_tag(self, tag):
        return self.all().filter(tags=tag)


class Question (models.Model):
    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=255)
    text = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='questions', blank=True)
    likes = GenericRelation(Like)
    type = 'question'
    rating = models.IntegerField(default=0, null=False)
    objects = QuestionManager()

    def __str__(self):
        return self.title


class AnswerManager(models.Manager):
    def hot(self):
        return self.all().order_by('rating').reverse()


class Answer (models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    what_question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.TextField()
    correct = models.BooleanField(default=False)
    likes = GenericRelation(Like)
    rating = models.IntegerField(default=0, null=False)
    objects = AnswerManager()
    type = 'answer'

    def __str__(self):
        return self.text

