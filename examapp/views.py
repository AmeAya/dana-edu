from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import *
from django.utils import timezone, dateformat
from .functions import getRandomVariant
from .functions import changeUserCurrentExamSubjects
from .functions import getQuestionPoints
from .functions import getUserUrls
from .functions import getBaseUrls
from .serializers import *


@login_required(login_url='login_url')
def userCabinetView(request):
    context = {'urls': getUserUrls(request.user)}

    return render(request, 'cabinet_page.html', context)


@login_required(login_url='login_url')
def examInitView(request):
    if request.user.type != 'PU':
        return redirect('home_url')
    group_exam = ExamForGroup.objects.filter(group=request.user.group).latest('pk')
    if group_exam:
        if group_exam.ends_at < timezone.now():
            context = {
                'message': 'Your exam already ends at ' + dateformat.format(group_exam.ends_at, 'Y-m-d H:i:s'),
                'urls': getUserUrls(request.user)
            }
            return render(request, 'exam_init_page.html', context)
        if request.user in group_exam.ended_users.all():
            context = {
                'message': 'You already done your exam!',
                'urls': getUserUrls(request.user)
            }
            return render(request, 'exam_init_page.html', context)
    else:
        context = {
            'message': 'You don`t have Exams!',
            'urls': getUserUrls(request.user)
        }
        return render(request, 'exam_init_page.html', context)
    current_exam = CurrentExam.objects.filter(user=request.user)
    if current_exam:
        context = {
            'message': 'Your variant is ',
            'variant': current_exam.latest('pk').variant,
            'subjects': SubjectCombination.objects.all(),
            'urls': getUserUrls(request.user)
        }
        return render(request, 'exam_init_page.html', context)
    current_variant = getRandomVariant(group_exam.variants.all(), request.user)
    CurrentExam(user=request.user, variant=current_variant).save()
    context = {
        'message': 'Your variant is ',
        'variant': current_variant,
        'subjects': SubjectCombination.objects.all(),
        'urls': getUserUrls(request.user)
    }
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
    ends_at = ExamForGroup.objects.filter(group=request.user.group).latest('pk').ends_at
    context = {
        'subjects': subjects.all(),
        'ends_at': ends_at
    }
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
            if PupilAnswer.objects.filter(user=request.user).filter(question=question).filter(is_in_action=True):
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
        pupil_answer = PupilAnswer.objects.filter(user=request.user).filter(question=question).filter(is_in_action=True)
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
    current_exam = CurrentExam.objects.get(user=request.user)
    starts_at = ExamForGroup.objects.filter(group=request.user.group).latest('pk').starts_at
    result = Result(user=request.user, variant=current_exam.variant, starts_at=starts_at, ends_at=timezone.now())
    pupil_answers = PupilAnswer.objects.filter(user=request.user).filter(is_in_action=True)
    result.points = 0
    result.save()
    for question in Question.objects.filter(variant=current_exam.variant):
        result.questions.add(question)
    for subject in current_exam.subjects.all():
        result.subjects.add(subject)
    result.save()

    for pupil_answer in pupil_answers:
        result.subjects.add(pupil_answer.question.subject)
        pupil_answer.points = getQuestionPoints(pupil_answer.question, pupil_answer.answers.all())
        result.answers.add(pupil_answer)
        result.points += pupil_answer.points
        result.save()
        pupil_answer.is_in_action = False
        pupil_answer.save()

    current_exam.delete()

    exam_group = ExamForGroup.objects.filter(group=request.user.group).latest('pk')
    exam_group.ended_users.add(request.user)
    exam_group.save()

    return redirect('exam_results_url')


@login_required(login_url='login_url')
def examResultsView(request):
    results = Result.objects.filter(user=request.user).order_by('-starts_at')

    context = {'results': results,
               'urls': getUserUrls(request.user)}
    return render(request, 'exam_results_page.html', context)


@login_required(login_url='login_url')
def examResultView(request, pk):
    result = Result.objects.get(pk=pk)
    pupil_answers = result.answers.all()
    if result.user != request.user:
        return redirect('exam_results_url')
    results = []
    for subject in result.subjects.all():
        results.append({'subject': subject, 'questions': []})
    for question in result.questions.all():
        correct_answers = []
        for answer in question.answers.all():
            if answer.is_correct:
                correct_answers.append(answer)
        this_question = {'question': question, 'answers': correct_answers, 'pupil_answers': [], 'points': 0}
        for pupil_answer in pupil_answers:
            if pupil_answer.question == question:
                this_question['pupil_answers'] = pupil_answer.answers.all()
                this_question['points'] = pupil_answer.points
                break
        if this_question['points'] == 1:
            this_question['points'] = '1 point'
        else:
            this_question['points'] = str(this_question['points']) + ' points'
        for subject in results:
            if subject['subject'] == question.subject:
                subject['questions'].append(this_question)
    context = {
        'results': results,
        'variant': result.variant,
        'points': result.points,
        'starts_at': result.starts_at.strftime('%Y-%m-%d %H:%M'),
        'urls': getUserUrls(request.user)
    }
    return render(request, 'exam_result_page.html', context)


@login_required(login_url='login_url')
def addQuestionsView(request, question_number):
    if request.user.type != 'MO':
        return redirect('home_url')
    if request.method == 'GET':
        if 'variant' in request.session:
            context = {
                'variant': Variant.objects.get(pk=request.session['variant']),
                'subjects': Subject.objects.all(),
                'points': [1, 2],
                'question_number': question_number,
                'urls': getUserUrls(request.user)
            }
            return render(request, 'add_questions_page.html', context)
        else:
            return redirect('add_questions_init_url')
    else:
        variant = Variant.objects.get(pk=request.POST.get('variant'))
        question_number = int(request.POST.get('question_number'))
        question_points = request.POST.get('question_points')
        subject = Subject.objects.get(pk=request.POST.get('subject'))
        question = Question(number=question_number, points=question_points, subject=subject, variant=variant)
        question_text = request.POST.get('question_text')
        if question_text:
            question.text = question_text
        if 'question_image' in request.FILES:
            question_image = request.FILES['question_image']
            question.image = question_image
        question.save()
        for i in range(1, int(request.POST.get('answers_count'))):
            is_correct = False
            is_empty = True
            if request.POST.get('is_correct_answer_' + str(i)):
                is_correct = True
            answer = Answer(is_correct=is_correct)
            answer_text = request.POST.get('answer_text_' + str(i))
            if 'answer_image_' + str(i) in request.FILES:
                answer_image = request.FILES['answer_image_' + str(i)]
                answer.image = answer_image
                is_empty = False
            if answer_text:
                answer.text = answer_text
                is_empty = False
            if not is_empty:
                answer.save()
                question.answers.add(answer)
        return redirect('add_questions_url', question_number=question_number+1)


@login_required(login_url='login_url')
def createVariantView(request):
    if request.user.type != 'MO':
        return redirect('home_url')
    if request.method == 'GET':
        from .functions import getExamTypesChoices
        choices = []
        for choice in getExamTypesChoices():
            choices.append(choice[0])
        context = {'choices': choices, 'urls': getUserUrls(request.user)}
        return render(request, 'add_variant_page.html', context)
    else:
        Variant(name=request.POST.get('variant_name'), exam_type=request.POST.get('choice')).save()
        return redirect('add_questions_init_url')


@login_required(login_url='login_url')
def addQuestionsInitView(request):
    if request.user.type != 'MO':
        return redirect('home_url')
    if request.method == 'GET':
        context = {'variants': Variant.objects.all(), 'urls': getUserUrls(request.user)}
        return render(request, 'add_questions_init_page.html', context)
    else:
        request.session['variant'] = request.POST.get('variant')
        return redirect('add_questions_url', question_number=1)


@login_required(login_url='login_url')
def setExamForGroup(request):
    if request.user.type != 'MO':
        return redirect('home_url')
    if request.method == 'GET':
        context = {'groups': Group.objects.all(),
                   'variants': Variant.objects.all(),
                   'exam_for_groups': ExamForGroup.objects.all().order_by('-pk'),
                   'urls': getUserUrls(request.user)}
        return render(request, 'set_exam_for_groups_page.html', context)
    else:
        group = Group.objects.get(pk=int(request.POST.get('group')))
        start_time = request.POST.get('start_time')
        start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M')
        duration = int(request.POST.get('duration'))
        exam_for_groups = ExamForGroup(group=group, duration=duration, starts_at=start_time)
        exam_for_groups.save()
        variants = request.POST.getlist('variants')
        for variant in variants:
            exam_for_groups.variants.add(Variant.objects.get(pk=int(variant)))
        exam_for_groups.save()
        return redirect('set_exam_for_groups_url')


def homeView(request):
    if request.user.is_authenticated:
        urls = getUserUrls(request.user)
        context = {'urls': getUserUrls(request.user)}
    else:
        context = {'urls': getBaseUrls()}
    return render(request, 'home_page.html', context)


@login_required(login_url='login_url')
def getStatsView(request):
    if request.user.type != 'MO':
        return redirect('home_url')
    if request.method == 'GET':
        context = {
            'regions': Region.objects.all(),
            'urls': getUserUrls(request.user)
        }
        return render(request, 'get_stats_init_page.html', context)
    else:
        school = School.objects.get(id=request.POST.get('school'))
        groups = Group.objects.filter(school=school)
        results_by_groups = []
        for group in groups:
            results = []
            for user in CustomUser.objects.filter(group=group):
                results.append(Result.objects.filter(user=user))
            results_by_groups.append({group: results})
        context = {
            'results_by_groups': results_by_groups,
            'urls': getUserUrls(request.user)
        }
        return render(request, 'get_stats_page.html', context)


class GetAreaByRegion(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        region = Region.objects.get(id=request.POST.get('region_id'))
        area = Area.objects.filter(region=region)
        data = {'areas': AreaSerializer(area, many=True).data}
        return Response(data, status=status.HTTP_200_OK)


class GetSchoolByArea(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        area = Area.objects.get(id=request.POST.get('area_id'))
        school = School.objects.filter(area=area)
        data = {'schools': SchoolSerializer(school, many=True).data}
        return Response(data, status=status.HTTP_200_OK)
