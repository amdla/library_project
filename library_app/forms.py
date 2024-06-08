from django import forms
from django.contrib.auth.models import User
from .models import Book, Loan
from django.forms.widgets import DateInput


class BookIDChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return str(obj.unique_id)


class BookForm(forms.ModelForm):
    isbn = forms.CharField(max_length=13, required=True, label='ISBN')

    class Meta:
        model = Book
        fields = ('isbn',)


class LoanForm(forms.ModelForm):
    book = BookIDChoiceField(queryset=Book.objects.all(), label='ID książki')
    borrower = forms.ModelChoiceField(queryset=User.objects.all(), label='Wypożyczający')
    return_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}), label='Data zwrotu')

    class Meta:
        model = Loan
        fields = ('book', 'borrower', 'return_date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book'].queryset = Book.objects.all()
        self.fields['borrower'].queryset = User.objects.all()


class UserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label='Imię')
    last_name = forms.CharField(max_length=30, required=True, label='Nazwisko')
    email = forms.EmailField(max_length=254, required=True, label='Email')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Istnieje już użytkownik z podanym adresem email. Wprowadź inny adres.")
        return email
