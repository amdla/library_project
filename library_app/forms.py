from django import forms
from django.contrib.auth.models import User
from .models import Book, Loan

class BookForm(forms.ModelForm):
    isbn = forms.CharField(max_length=13, required=True, label='ISBN')

    class Meta:
        model = Book
        fields = ('isbn',)

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ('book', 'borrower', 'return_date')

class UserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, label='Imię')
    last_name = forms.CharField(max_length=30, required=True, label='Nazwisko')
    email = forms.EmailField(max_length=254, required=True, label='Email')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
