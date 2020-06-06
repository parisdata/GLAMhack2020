from django import forms

class UploadFileForm(forms.Form):
    column = forms.CharField(label='column', max_length=100)
    testCSV = forms.FileField()