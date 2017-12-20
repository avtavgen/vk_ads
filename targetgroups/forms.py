from django import forms


class NewTargetGroupForm(forms.Form):
    account_id = forms.IntegerField()
    name = forms.CharField(max_length=100)
    file = forms.FileField()


