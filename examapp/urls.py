from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from .forms import CustomUserLoginForm
from .views import *


urlpatterns = [
    path('cabinet', userCabinetView, name='cabinet_url'),
    path('exam_init', examInitView, name='exam_init_url'),
    path('subject_select', subjectSelectView, name='get_subjects_url'),
    path('exam', examView, name='exam_url'),
    path('get_questions_by_subject', GetQuestionsBySubjectApiView.as_view(), name='question_by_subject_url'),
    path('get_exam_question', GetExamQuestionApiView.as_view(), name='get_exam_question_url'),
    path('set_pupil_answers', SetPupilAnswers.as_view(), name='set_pupil_answers_url'),
    path('end_exam', endExamView, name='end_exam_url'),
    path('home', TemplateView.as_view(template_name='home_page.html'), name='home_url'),
    path('login', LoginView.as_view(template_name='login_page.html', redirect_authenticated_user=True,
                                    authentication_form=CustomUserLoginForm), name='login_url'),
    path('logout', LogoutView.as_view(), name='logout_url'),
]
