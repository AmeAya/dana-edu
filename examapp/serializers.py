from rest_framework.serializers import ModelSerializer
from .models import Answer, Question


class AnswerSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
