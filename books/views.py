from typing import Optional
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Book
from .forms import CommentForm


class BookListView(generic.ListView):
    model = Book
    paginate_by = 4
    template_name = 'books/books_list.html'
    context_object_name = 'books'

class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book
    form_class = CommentForm
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        book_comments = book.comments.all()
        comment_form = self.form_class()

        return render(request, self.template_name, context={'book': book, 'comments': book_comments, 'comment_form': comment_form,})
    
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        book_comments = book.comments.all()
        comment_form = self.form_class(request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.book = book
            new_comment.user = request.user
            new_comment.save()
            comment_form = self.form_class()

        return render(request, self.template_name, context={'book': book, 'comments': book_comments, 'comment_form': comment_form})


class BookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Book
    fields = ['title', 'author', 'description', 'price', 'cover']
    template_name = 'books/book_create.html'

class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Book
    fields = ['title', 'author', 'description', 'price', 'cover']
    template_name = 'books/book_update.html'

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user
    
class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Book
    template_name = 'books/book_delete.html'
    success_url = reverse_lazy('books_list')

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


def book_search_view(request):
    if request.method == "GET":
        query = request.GET.get('query')

        if query:
            results = Book.objects.filter(title__icontains=query)
        else:
            results = []
    
    context = {'results': results, 'query': query}
    return render(request, 'books/book_search.html', context)
