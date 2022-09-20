from django import forms

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)    