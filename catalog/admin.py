from django.contrib import admin
from .models import Author, Genre, Language, Book, BookInstance


class BookInline(admin.StackedInline):
    model = Book
    classes = ("collapse",)
    fieldsets = [(None, {"fields": ["title", "isbn"]}),]
    extra = 0
    readonly_fields = ["isbn", "title"]
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "date_of_birth", "date_of_death")
    fields = [("first_name", "last_name"), ("date_of_birth", "date_of_death")]
    inlines = [BookInline]

admin.site.register(Author, AuthorAdmin)

##########
class BookInstanceInLine(admin.TabularInline):
    model = BookInstance
    extra = 0
    readonly_fields = ["id"]
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "display_genre", "language", "isbn")
    inlines = [BookInstanceInLine]

#############
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ("book", "status", "borrower", "due_back", "id")
    list_filter = ("status", "due_back")

    fieldsets = (
        ("Book Info", {"fields": ("book", "imprint", "id")}),
        ('Availability', {"fields": ("status", "due_back", "borrower")}),
    )

#admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Language)
# admin.site.register(Book)
# admin.site.register(BookInstance)


# Register your models here.
