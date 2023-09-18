from rest_framework.serializers import ModelSerializer
from .models import *


class AnswerSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'text', 'image')


class AreaSerializer(ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class SchoolSerializer(ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'


class PupilAnswerSerializer(ModelSerializer):
    class Meta:
        model = PupilAnswer
        fields = ('answers', 'question')


class VariantSerializer(ModelSerializer):
    class Meta:
        model = Variant
        fields = '__all__'
