from django import forms
from django.core.mail import send_mail

from core.models import SiteConfiguration


class SelectWithDisabled(forms.Select):
    """
    Subclass of Django's select widget that allows disabling options.
    To disable an option, pass a dict instead of a string for its label,
    of the form: {'label': 'option label', 'disabled': True}
    """

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        disabled = False
        if isinstance(label, dict):
            label, disabled = label['label'], label['disabled']
        option_dict = super(SelectWithDisabled, self).create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)
        if disabled:
            option_dict['attrs']['disabled'] = 'disabled'
        return option_dict


class HoneyPotForm(forms.Form):
    h0n3yp0t = forms.CharField(required=False,
                               widget=forms.TextInput(attrs={'autocomplete': 'off', 'tabindex': '-1'}))

    def clean(self):
        cleaned_data = super().clean()
        hp = cleaned_data.get('h0n3yp0t')
        if hp:
            raise forms.ValidationError('You are bot')


class ContactForm(HoneyPotForm):
    TIME_CHOICES = (
        ('', {'label': 'Best Contact Time*', 'disabled': True}),
        ('Morning', 'Morning'),
        ('Afternoon', 'Afternoon'),
        ('Evening', 'Evening'),
    )

    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name*'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email*'}))
    phone = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone*'}))
    best_time = forms.ChoiceField(choices=TIME_CHOICES, widget=SelectWithDisabled(attrs={'class': 'form-control'}))
    project_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Project Address'}), required=False)
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'How we can help you?'}))

    def send_mail(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        phone = self.cleaned_data['phone']
        best_time = self.cleaned_data['best_time']
        project_address = self.cleaned_data['project_address']
        message = self.cleaned_data['message']

        message = f"""
Name: {name}
Email: {email}
Phone: {phone}
Best Time: {best_time}
Project Address: {project_address}
Message: {message}
        """
        email_list = SiteConfiguration.get_solo().email_list.splitlines() or None
        if email_list:
            try:
                send_mail('Emerald Contact Form', message, None, email_list)
            except Exception as e:
                print(str(e))
