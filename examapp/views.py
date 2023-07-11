from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import *
from django.utils import timezone, dateformat
from .functions import getRandomVariant, changeUserCurrentExamSubjects
from .serializers import QuestionSerializer, AnswerSerializer


@login_required(login_url='login_url')
def userCabinetView(request):
    urls = []
    if request.user.type == 'PU':
        urls.append({'text': 'Init Exam', 'url': 'exam_init_url'})
    context = {'urls': urls}
    return render(request, 'cabinet_page.html', context)


@login_required(login_url='login_url')
def examInitView(request):
    if request.user.type != 'PU':
        return redirect('home_url')
    group_exam = ExamForGroup.objects.filter(group=request.user.group).latest('pk')
    if group_exam:
        if group_exam.ends_at < timezone.now():
            context = {'message': 'Your exam already ends at ' + dateformat.format(group_exam.ends_at, 'Y-m-d H:i:s')}
            return render(request, 'exam_init_page.html', context)
    else:
        context = {'message': 'You don`t have Exams!'}
        return render(request, 'exam_init_page.html', context)
    current_exam = CurrentExam.objects.filter(user=request.user)
    if current_exam:
        context = {'message': 'Your variant is ',
                   'variant': current_exam.latest('pk').variant,
                   'subjects': SubjectCombination.objects.all()}
        return render(request, 'exam_init_page.html', context)
    current_variant = getRandomVariant(group_exam.variants.all(), request.user)
    CurrentExam(user=request.user, variant=current_variant).save()
    context = {'message': 'Your variant is ',
               'variant': current_variant,
               'subjects': SubjectCombination.objects.all()}
    return render(request, 'exam_init_page.html', context)


@login_required(login_url='login_url')
def subjectSelectView(request):
    if request.method == 'POST':
        changeUserCurrentExamSubjects(request.user, request.POST.get('subjects'))
        return redirect('exam_url')
    else:
        return redirect('home_url')


@login_required(login_url='login_url')
def examView(request):
    subjects = CurrentExam.objects.filter(user=request.user).latest('pk').subjects
    context = {'subjects': subjects.all()}
    return render(request, 'exam_page.html', context)


class GetExamQuestionApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        question = Question.objects.get(pk=request.GET.get('pk'))
        answers = question.answers.all()
        data = {'question': QuestionSerializer(question).data,
                'answers': AnswerSerializer(answers, many=True).data}
        return Response(data, status=status.HTTP_200_OK)


class GetQuestionsBySubjectApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        subject = Subject.objects.get(pk=request.query_params['subject_id'])
        variant = CurrentExam.objects.filter(user=request.user).latest('pk').variant
        questions = Question.objects.filter(subject=subject).filter(variant=variant).order_by('number')
        is_solved = []
        for question in questions:
            if PupilAnswer.objects.filter(user=request.user).filter(question=question):
                is_solved.append(True)
            else:
                is_solved.append(False)
        data = {'questions': QuestionSerializer(questions, many=True).data,
                'is_solved': is_solved}
        return Response(data, status=status.HTTP_200_OK)


class SetPupilAnswers(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        question = Question.objects.get(pk=request.POST.get('question'))
        pupil_answer = PupilAnswer.objects.filter(user=request.user).filter(question=question)
        answers = Answer.objects.filter(pk__in=request.POST.get('answers').split(','))
        if not pupil_answer:
            pupil_answer = PupilAnswer(user=request.user, question=question)
            pupil_answer.save()
        else:
            pupil_answer = pupil_answer.latest('pk')
            pupil_answer.answers.clear()
        pupil_answer.answers.add(*answers)
        pupil_answer.save()
        return Response(status=status.HTTP_200_OK)


@login_required(login_url='login_url')
def endExamView(request):
    for answer in PupilAnswer.objects.filter(user=request.user):
        answer.delete()
    return render(request, '', )
