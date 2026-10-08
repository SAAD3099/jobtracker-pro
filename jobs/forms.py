from django import forms
from .models import JobApplication
class ApplicationForm(forms.ModelForm):
    class Meta:
        model=JobApplication
        fields=['company','role','salary','job_link','status','applied_date','interview_at','notes']
        widgets={'applied_date':forms.DateInput(attrs={'type':'date'}),'interview_at':forms.DateTimeInput(format='%Y-%m-%dT%H:%M',attrs={'type':'datetime-local'}),'notes':forms.Textarea(attrs={'rows':4})}
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['interview_at'].input_formats=['%Y-%m-%dT%H:%M']
    def clean_job_link(self):
        value=self.cleaned_data['job_link']
        if value and not value.lower().startswith(('https://','http://')):
            raise forms.ValidationError('Use an http or https link.')
        return value
