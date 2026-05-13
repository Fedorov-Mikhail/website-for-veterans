from django import forms

from .models import IssueReport


class IssueReportForm(forms.ModelForm):
    class Meta:
        model = IssueReport
        fields = ['problem_type', 'message', 'contact', 'consent']

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
