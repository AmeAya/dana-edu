from rest_framework.serializers import ModelSerializer
from .models import Answer, Area, Question, School


class AnswerSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


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
