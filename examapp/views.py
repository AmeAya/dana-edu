from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required


@login_required(login_url='login_url')
def userCabinetView(request):
    urls = []
    if request.user.type == 'PU':
        urls.append({'text': 'Init Exam', 'url': 'exam_init_url'})
    context = {'urls': urls}
    return render(request, 'cabinet_page.html', context)


@login_required(login_url='login_url')
def examInitView(request):
    pass
