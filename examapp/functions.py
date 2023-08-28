from django.utils.translation import gettext_lazy as _


def getExamTypesChoices() -> list:
    exam_types = ['MODO', 'ENT']
    return [(exam_type, exam_type) for exam_type in exam_types]


def getLiteralChoices() -> list:
    russian_alphabet = "А,Б,В,Г,Д,Е,Ё,Ж,З,И,Й,К,Л,М,Н,О,П,Р,С,Т,У,Ф,Х,Ц,Ч,Ш,Щ,Ъ,Ы,Ь,Э,Ю,Я".split(',')
    return [(russian_alphabet[i], russian_alphabet[i]) for i in range(len(russian_alphabet))]


def getNumberChoices() -> list:
    return [(i, i) for i in range(1, 12)]


def getVariantLanguageChoices() -> list:
    exam_types = ['KAZ', 'RUS']
    return [(exam_type, exam_type) for exam_type in exam_types]


def getUserTypeChoices() -> list:
    return [
        ('AH', 'Area Head'),
        ('MH', 'Ministry Head'),
        ('RH', 'Region Head'),
        ('PU', 'Pupil'),
        ('PA', 'Parent'),
        ('SD', 'School Director'),
        ('SS', 'School Staff'),
        ('TE', 'Teacher'),
        ('MO', 'Moderator'),
    ]


def getRandomVariant(all_variants, user):
    from random import choice
    from .models import Result
    user_results = Result.objects.filter(user=user)
    variants = None
    if user_results:
        variants = set(all_variants)
        for result in user_results:
            if result.variant in variants:
                variants.remove(result.variant)
    if variants:
        return choice(list(variants))
    return choice(all_variants)


def getExamSubjects(chosen_subjects_id):
    from .models import Subject, SubjectCombination
    chosen_subjects = SubjectCombination.objects.get(pk=chosen_subjects_id)
    first_subject = Subject.objects.filter(pk=chosen_subjects.first_subject.pk)
    second_subject = Subject.objects.filter(pk=chosen_subjects.second_subject.pk)
    return Subject.objects.filter(is_required=True) | first_subject | second_subject


def changeUserCurrentExamSubjects(user, chosen_subjects_id):
    from .models import CurrentExam
    current_exam = CurrentExam.objects.filter(user=user).latest('pk')
    for subject in getExamSubjects(chosen_subjects_id):
        current_exam.subjects.add(subject)
    current_exam.save()


def getQuestionPoints(question, answers) -> int:
    if not answers:
        return 0
    correct_answers = 0
    for answer in question.answers.all():
        if answer.is_correct:
            correct_answers += 1
    pupil_correct_answers = 0
    pupil_wrong_answers = 0
    for answer in answers:
        if answer.is_correct:
            pupil_correct_answers += 1
        else:
            pupil_wrong_answers += 1
    if pupil_wrong_answers >= 2 or pupil_correct_answers == 0:
        return 0
    if pupil_wrong_answers == 1 and correct_answers == pupil_correct_answers + 1:
        return 1
    if pupil_wrong_answers == 0 and correct_answers == pupil_correct_answers:
        return question.points
    if pupil_wrong_answers == 0 and correct_answers > pupil_correct_answers:
        return 1


def getUserUrls(user) -> []:
    urls = [
        {'text': _('My Cabinet'), 'url': 'cabinet_url'},
        {'text': _('About Us'), 'url': 'about_us_url'}
    ]
    if user.type == 'PU':
        urls.append({'text': _('Init Exam'), 'url': 'exam_init_url'})
        urls.append({'text': _('Exam Results'), 'url': 'exam_results_url'})
    if user.type == 'MO':
        urls.append({'text': _('Get Stats'), 'url': 'get_stats_url'})
        urls.append({'text': _('Add Question'), 'url': 'add_questions_init_url'})
        urls.append({'text': _('Questions Update'), 'url': 'questions_update_url'})
        urls.append({'text': _('Set Exam For Groups'), 'url': 'set_exam_for_groups_url'})
    urls.append({'text': _('Log Out'), 'url': 'logout_url'})
    return urls


def getBaseUrls() -> []:
    urls = [{'text': _('Log In'), 'url': 'login_url'}]
    return urls


def getUserAvg(user):
    from .models import Result
    avg = 0
    results = Result.objects.filter(user=user)
    if results:
        for result in results:
            avg += result.points
        return round(avg / len(results), 2)
    else:
        return 0
