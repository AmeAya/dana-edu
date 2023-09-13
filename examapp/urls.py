from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import RedirectView
from .forms import CustomUserLoginForm
from .views import *


urlpatterns = [
    path('', RedirectView.as_view(permanent=True, url='home')),
    path('about_us', aboutUsView, name='about_us_url'),
    path('add_questions_init', addQuestionsInitView, name='add_questions_init_url'),
    path('add_questions', addQuestionsView, name='add_questions_url'),
    path('add_variant', addVariantView, name='add_variant_url'),
    path('cabinet', userCabinetView, name='cabinet_url'),
    path('exam', examView, name='exam_url'),
    path('exam_init', examInitView, name='exam_init_url'),
    path('end_exam', endExamView, name='end_exam_url'),
    path('end_exam_violated', endExamViolatedView, name='end_exam_violated_url'),
    path('exam_result/<int:pk>', examResultView, name='exam_result_url'),
    path('exam_results', examResultsView, name='exam_results_url'),
    path('excel_api', ExcelStatsAPIVIew.as_view(), name='excel_stats_url'),
    path('get_area_by_region', GetAreaByRegion.as_view(), name='get_area_by_region_url'),
    path('get_exam_question', GetExamQuestionApiView.as_view(), name='get_exam_question_url'),
    path('get_questions_by_subject', GetQuestionsBySubjectApiView.as_view(), name='question_by_subject_url'),
    path('get_school_by_area', GetSchoolByArea.as_view(), name='get_school_by_area_url'),
    path('get_stats', getStatsView, name='get_stats_url'),
    path('home/', homeView, name='home_url'),
    path('login', LoginView.as_view(template_name='login_page.html', redirect_authenticated_user=True,
                                    authentication_form=CustomUserLoginForm), name='login_url'),
    path('logout', LogoutView.as_view(), name='logout_url'),
    path('question_preview/<int:question_id>', questionPreviewView, name='question_preview_url'),
    path('question_delete/<int:question_id>', questionDeleteView, name='question_delete_url'),
    path('question_update/<int:question_id>', questionUpdateView, name='question_update_url'),
    path('questions_update', questionsUpdateInitView, name='questions_update_url'),
    path('set_exam_for_groups', setExamForGroup, name='set_exam_for_groups_url'),
    path('set_pupil_answers', SetPupilAnswers.as_view(), name='set_pupil_answers_url'),
    path('subject_select', subjectSelectView, name='get_subjects_url'),
]
