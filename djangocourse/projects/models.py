from django.db import models

import uuid

from users.models import UserProfile

# Create your models here.


class Project(models.Model):
    owner = models.ForeignKey(
        UserProfile, null=True, blank=True, on_delete=models.SET_NULL,
    )

    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)

    featured_image = models.ImageField(
        null=True, blank=True, default='default.jpg',
    )

    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False,
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = ['-vote_ratio', '-vote_total', '-created']

    @property
    def get_vote_ratio(self):
        all_reviews = self.review_set.all()

        upvotes = all_reviews.filter(value='up').count()
        total_votes = all_reviews.count()

        self.vote_total = total_votes

        if total_votes == 0:
            self.vote_ratio = 0.0
        else:
            self.vote_ratio = upvotes / total_votes * 100

        self.save()


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )

    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False,
    )

    def __str__(self):
        return self.value

    class Meta:
        unique_together = [['owner', 'project']]


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False,
    )

    def __str__(self):
        return self.name
