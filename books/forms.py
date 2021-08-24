from django import forms
from django.core.mail import send_mail

from books.models import Author


class ContactForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)
    terms_of_use = forms.BooleanField(required=True)
    age = forms.IntegerField()

    def send_email(self):
        name = self.cleaned_data.get('name')
        message = self.cleaned_data.get('message')
        send_mail(
            subject=f'Nowy komenatarz do strony od {name}',
            message=message,
            from_email='no-replay@mojastrona.pl',
            recipient_list=['kamilmarekradomski@gmail.com'],
        )


class AuthorContactForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)
    terms_of_use = forms.BooleanField(required=True)

    def __init__(self, *args, **kwargs):
        self.author_id = kwargs.pop('author_id')
        super().__init__(*args, **kwargs)

    def send_email(self):
        name = self.cleaned_data.get('name')
        message = self.cleaned_data.get('message')
        author = Author.objects.get(pk=self.author_id)
        send_mail(
            subject=f'Nowy komenatarz do strony od {name}',
            message=message,
            from_email='no-replay@mojastrona.pl',
            recipient_list=[f'{author.first_name}_{author.last_name}@bestbooks.pl'],
        )


class LoginForm(forms.Form):
    username = forms.CharField(label='login')
    password = forms.CharField(label='password', widget=forms.PasswordInput)
