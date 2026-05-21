from django import forms
from .models import Resume


class ResumeUploadForm(forms.ModelForm):
    """
    Form for uploading resumes.
    """
    class Meta:
        model = Resume
        fields = ['uploaded_file']
        widgets = {
            'uploaded_file': forms.FileInput(attrs={
                'class': 'd-none',
                'accept': 'pdf',
                'required': True,
                'id': 'id_uploaded_file',
            })
        }

    def clean_uploaded_file(self):
        """
        Validate the uploaded file.
        """
        file = self.cleaned_data.get('uploaded_file')
        
        if file:
            # Check file size (5MB max)
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError('File size must not exceed 5MB.')
            
            # Check file type
            if not file.name.lower().endswith('.pdf'):
                raise forms.ValidationError('Only PDF files are allowed.')
            
        return file
