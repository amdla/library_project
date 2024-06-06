from django import forms
from django.contrib.auth.models import User
from .models import Book, Loan

class BookForm(forms.ModelForm):
    isbn = forms.CharField(max_length=13, required=True, label='ISBN')
    libraryID = forms.CharField(max_length=20, required=True, label='Library ID')

    class Meta:
        model = Book
        fields = ('uniqueID', 'isbn', 'libraryID', 'title', 'authors', 'publisher', 'publication_date')

class LoanForm(forms.ModelForm):
    isbn = forms.CharField(max_length=13, required=True, label='ISBN')
    book = forms.ModelChoiceField(queryset=Book.objects.none(), label='Book (Library ID)')

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
