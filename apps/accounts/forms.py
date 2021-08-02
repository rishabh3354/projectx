from django import forms


class ContactForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Your Email'}))
    subject = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Subject'}))
    message = forms.CharField(widget=forms.Textarea, required=True)


class SetPassword(forms.Form):
    password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput())

