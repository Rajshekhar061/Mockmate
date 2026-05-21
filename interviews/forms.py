from django import forms
from .models import Interview


class InterviewStartForm(forms.ModelForm):
    """Form used to start a new mock interview session."""

    class Meta:
        model = Interview
        fields = ['role', 'difficulty', 'interview_type']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-select'}),
            'difficulty': forms.Select(attrs={'class': 'form-select'}),
            'interview_type': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        difficulty = cleaned_data.get('difficulty')
        interview_type = cleaned_data.get('interview_type')

        if not role or not difficulty or not interview_type:
            raise forms.ValidationError('Please select a role, difficulty, and interview type.')

        return cleaned_data


class InterviewAnswerForm(forms.Form):
    """Form for answering a single interview question."""

    user_answer = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Write your answer here...'
            }
        ),
        label='Your Answer',
        required=True,
    )

    def clean_user_answer(self):
        answer = self.cleaned_data.get('user_answer', '').strip()
        if not answer:
            raise forms.ValidationError('Please enter an answer before continuing.')
        return answer
