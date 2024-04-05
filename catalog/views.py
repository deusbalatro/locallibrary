import datetime
from typing import Any
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Book, Author, Language, Genre, BookInstance
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required
from django.urls import reverse, reverse_lazy
from catalog.forms import RenewBookForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView




 
def index(request):
    #View Function for home page of site
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    num_authors = Author.objects.all().count()

    num_genres = Genre.objects.all().count()

    num_contains_ç = Book.objects.filter(title__icontains="ç").count()
    
    num_contains_st = Genre.objects.filter(name__icontains="st").count()
    
    num_visits = request.session.get("num_visits", 0)
    request.session['num_visits'] = num_visits + 1

    if num_visits > 0:
        persistency_message = "Welcome Back!"
    else:
        persistency_message="" 

    

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_contains_ç': num_contains_ç,
        'num_contains_st': num_contains_st,
        'num_visits': num_visits,
        'persistency_message': persistency_message,
    }

    return render(request, 'index.html', context=context)

class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    paginate_by = 2
    #login_url = '/login/'
    #redirect_field_name = ''
    # context_object_name = 'book_list'
    # queryset = Book.objects.all()
    # template_name = 'catalog/book_list.html'
    # def get_context_data(self, **kwargs: Any):
    #     context = super(BookListView, self).get_context_data(**kwargs)
    #     context['all_books'] = 'These are all books in database'
    #     return context

class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book

class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    paginate_by = 2

class AuthorListDetail(LoginRequiredMixin, generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):

    permission_required = 'catalog.can_mark_returned'

    model = BookInstance
    template_name = 'bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return(
            BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
        )

class LoanedBooksListView(PermissionRequiredMixin, generic.ListView):

    permission_required = 'catalog.can_mark_returned'

    model = BookInstance
    template_name = 'bookinstance_list_borrowed_staff.html'

    def get_queryset(self):
        return(BookInstance.objects.filter(status__exact='o').order_by('due_back'))


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == "POST":

        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('borrowed-books'))
        
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, "book_renew_librarian.html", context)


#ModelForm method to create form based on a spesific model:
"""from django.forms import ModelForm

from catalog.models import BookInstance

class RenewBookModelForm(ModelForm):
    def clean_due_back(self):
       data = self.cleaned_data['due_back']

       # Check if a date is not in the past.
       if data < datetime.date.today():
           raise ValidationError(_('Invalid date - renewal in past'))

       # Check if a date is in the allowed range (+4 weeks from today).
       if data > datetime.date.today() + datetime.timedelta(weeks=4):
           raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

       # Remember to always return the cleaned data.
       return data

    class Meta:
        model = BookInstance
        fields = ['due_back']
        labels = {'due_back': _('Renewal date')}
        help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3).')}"""

class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': 'mm/dd/yyyy'}
    permission_required = 'catalog.add_author'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = '__all__'
    permission_required = 'catalog.change_author'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.delete_author'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(reverse("author-delete", kwargs={"pk": self.object.pk}))
    
class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.add_book'

class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.change_book'

class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.delete_book'

    def form_valid(self, form):
        try: 
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(reverse("book-delete", kwargs={"pk": self.object.pk}))
