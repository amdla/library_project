from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Author, Publisher, Book, BookCopy, Loan, UserProfile

# Inline for UserProfile to be edited within User admin
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'
    fk_name = 'user'

# Extend existing User admin to include UserProfile
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_library_card_number')

    def get_library_card_number(self, instance):
        return instance.userprofile.library_card_number if hasattr(instance, 'userprofile') else None
    get_library_card_number.short_description = 'Library Card Number'

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Admin for Author
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name')

# Admin for Publisher
@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Admin for Book
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publisher', 'publication_year', 'isbn')
    list_filter = ('author', 'publisher')
    search_fields = ('title', 'isbn')

# Admin for BookCopy
@admin.register(BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
    list_display = ('book', 'status')
    list_filter = ('status', 'book')
    actions = ['make_available', 'make_unavailable']

    def make_available(self, request, queryset):
        queryset.update(status='available')
    make_available.short_description = "Mark selected copies as available"

    def make_unavailable(self, request, queryset):
        queryset.update(status='borrowed')
    make_unavailable.short_description = "Mark selected copies as unavailable"

# Admin for Loan
@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('book_copy', 'borrower', 'loan_date', 'return_date')
    list_filter = ('loan_date', 'return_date')
    search_fields = ('borrower__username',)
