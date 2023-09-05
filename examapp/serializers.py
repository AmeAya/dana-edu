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

    def to_representation(self, instance):
        obj = super().to_representation(instance)
        obj['text'] = obj['text'].replace('\n', '<br>')
        obj['text'] = obj['text'].replace('\r\x85', '<br>')
        obj['text'] = obj['text'].replace('\t', '&nbsp&nbsp&nbsp&nbsp')
        return obj


class SchoolSerializer(ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'


class PupilAnswerSerializer(ModelSerializer):
    class Meta:
        model = PupilAnswer
        fields = ('answers', 'question')
