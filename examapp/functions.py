def getExamTypesChoices() -> list:
    exam_types = ['ENT', 'MODO', 'VOUD']
    return [(exam_type, exam_type) for exam_type in exam_types]


def getLiteralChoices() -> list:
    russian_alphabet = "А,Б,В,Г,Д,Е,Ё,Ж,З,И,Й,К,Л,М,Н,О,П,Р,С,Т,У,Ф,Х,Ц,Ч,Ш,Щ,Ъ,Ы,Ь,Э,Ю,Я".split(',')
    return [(russian_alphabet[i], russian_alphabet[i]) for i in range(len(russian_alphabet))]


def getNumberChoices() -> list:
    return [(i, i) for i in range(1, 12)]


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
