from django import forms

class FileUploadForm(forms.Form):
    file = forms.FileField(label='Select a CSV file')

class LabelEditForm(forms.Form):
    index = forms.IntegerField(label='Index')
    label = forms.CharField(label='Label')
