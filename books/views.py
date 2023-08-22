from django.views import generic
from django.urls import reverse_lazy

from .models import Book


class BookListView(generic.ListView):
    model = Book
    template_name = 'books/books_list.html'
    context_object_name = 'books'

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

class BookCreateView(generic.CreateView):
    model = Book
    fields = ['title', 'author', 'description', 'price',]
    template_name = 'books/book_create.html'

class BookUpdateView(generic.UpdateView):
    model = Book
    fields = ['title', 'author', 'description', 'price',]
    template_name = 'books/book_update.html'

class BookDeleteView(generic.DeleteView):
    model = Book
    template_name = 'books/book_delete.html'
    success_url = reverse_lazy('books_list')
