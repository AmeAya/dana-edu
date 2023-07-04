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
    ]
