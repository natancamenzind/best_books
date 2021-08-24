from django.contrib import admin

from books.models import Author, Book, BookComment


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass


@admin.register(BookComment)
class BookCommentAdmin(admin.ModelAdmin):
    pass
