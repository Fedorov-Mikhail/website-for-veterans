from django import forms


class IssueReportForm(forms.Form):
    PROBLEM_TYPES = (
        ('fact', 'Фактическая ошибка'),
        ('typo', 'Опечатка'),
        ('other', 'Другое'),
    )

    problem_type = forms.ChoiceField(choices=PROBLEM_TYPES)
    message = forms.CharField(min_length=20)
    contact = forms.CharField(max_length=200, required=False)
    consent = forms.BooleanField()

    def clean_message(self):
        message = self.cleaned_data['message'].strip()
        if len(message) < 20:
            raise forms.ValidationError('Опишите проблему чуть подробнее.')
        return message

    def clean_consent(self):
        consent = self.cleaned_data['consent']
        if not consent:
            raise forms.ValidationError('Нужно согласие на обработку персональных данных.')
        return consent
