from django import forms


class PDF(forms.Form):
    file1 = forms.FileField()  # for creating file input
    file2 = forms.FileField()  # for creating file input

