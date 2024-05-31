from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Book, Loan

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='Imię')
    last_name = forms.CharField(max_length=30, required=True, label='Nazwisko')
    email = forms.EmailField(max_length=254, required=True, label='Email')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

class CustomUserChangeForm(UserChangeForm):
    first_name = forms.CharField(max_length=30, required=True, label='Imię')
    last_name = forms.CharField(max_length=30, required=True, label='Nazwisko')
    email = forms.EmailField(max_length=254, required=True, label='Email')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

class BookForm(forms.ModelForm):
    isbn = forms.CharField(max_length=13, required=True, label='ISBN')

    class Meta:
        model = Book
        fields = ('isbn',)

class LoanForm(forms.ModelForm):
    book_id = forms.CharField(max_length=20, required=True, label='ID książki')
    borrower = forms.ModelChoiceField(queryset=User.objects.all(), label='Wypożyczający')
    return_date = forms.DateField(widget=forms.SelectDateWidget(), label='Data zwrotu')

    class Meta:
        model = Loan
        fields = ('book_id', 'borrower', 'return_date')