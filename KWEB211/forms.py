from django import forms
from .models import LecturePost
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class LecturePostForm(forms.ModelForm):
    class Meta:
        model = LecturePost
        fields = ['title', 'content']

        widgets = {
            'title': forms.TextInput(),
            'content': forms.CharField(widget=CKEditorUploadingWidget()),
        }