from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import *
from .forms import CustomUserChangeForm, CustomUserCreationForm


class CustomUserAdmin(UserAdmin):
    readonly_fields = ('date_joined', 'last_login', 'is_staff', 'is_superuser', 'is_active')
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('surname', 'name', 'patronymic', 'iin')
    add_fieldsets = (
        (None, {
            'fields': (
                'iin', 'password', 'type', 'surname', 'name', 'patronymic',
                'photo', 'phone', 'birth_date',  'group',
            )
        }),
    )
    fieldsets = (
        (None, {
            "fields": (
                'iin', 'password', 'type', 'surname', 'name', 'patronymic', 'photo', 'phone', 'birth_date',
                'group', 'is_staff', 'is_superuser', 'is_active', 'date_joined', 'last_login',
            ),
        }),
    )
    # list_filter = ('iin', 'surname', 'name', 'patronymic')
    search_fields = ('iin',)
    ordering = ('surname', 'name', 'patronymic')


admin.site.register(Answer)
admin.site.register(Area)
admin.site.register(CurrentExam)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ExamForGroup)
admin.site.register(Group)
admin.site.register(Ministry)
admin.site.register(PupilAnswer)
admin.site.register(Question)
admin.site.register(Region)
admin.site.register(Result)
admin.site.register(School)
admin.site.register(Subject)
admin.site.register(SubjectCombination)
admin.site.register(Variant)
