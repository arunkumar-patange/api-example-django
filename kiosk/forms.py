from django import forms


# forms go here
class VerifyForm(forms.Form):
    class Meta:
        widgets = {
            'ssn': forms.TextInput(attrs={'placeholder': 'optional'}),
        }

    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    ssn = forms.CharField(label='SSN (optional)', max_length=11, required=False)


class DemoForm(forms.Form):
    '''
    demographics form
    '''
    first_name = forms.CharField(label='First Name', required=False)
    last_name = forms.CharField(label='Last Name', required=False)
    date_of_birth = forms.DateField(required=False)
    gender = forms.ChoiceField(required=True, choices=(
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ))
    social_security_number = forms.CharField(required=False)
    cell_phone = forms.CharField(required=False)
    doctor = forms.CharField(widget=forms.HiddenInput())
