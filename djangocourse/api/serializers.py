from rest_framework import serializers

from projects.models import Project, Tag, Review
from users.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['name', 'email']


class ReviewSerializer(serializers.ModelSerializer):
    owner = UserProfileSerializer(many=False)

    class Meta:
        model = Review
        fields = ['value', 'body', 'owner', 'created']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


class ProjectSerializer(serializers.ModelSerializer):
    owner = UserProfileSerializer(many=False)
    tags = TagSerializer(many=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    def get_reviews(self, object):
        reviews = object.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)

        return serializer.data
