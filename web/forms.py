from django import forms

from web.models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('title', 'text')

