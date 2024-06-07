from django import forms
from django.contrib.auth.models import User
from .models import Book, Loan
from django.forms.widgets import DateInput

class BookForm(forms.ModelForm):
    isbn = forms.CharField(max_length=13, required=True, label='ISBN')

    class Meta:
        model = Book
        fields = ('isbn',)

class LoanForm(forms.ModelForm):
    isbn = forms.CharField(max_length=13, required=True, label='ISBN')
    book = forms.ModelChoiceField(queryset=Book.objects.none(), label='Book (Unique ID)')
    return_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Loan
        fields = ('isbn', 'book', 'borrower', 'return_date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'isbn' in self.data:
            try:
                isbn = self.data.get('isbn')
                self.fields['book'].queryset = Book.objects.filter(isbn=isbn)
            except (ValueError, TypeError):
                pass
        else:
            self.fields['book'].queryset = Book.objects.none()

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