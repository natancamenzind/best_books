from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import \
    ListView, DetailView, TemplateView, \
    FormView

from books.forms import ContactForm, AuthorContactForm
from books.models import Author, Book, BookComment


class AuthorListView(ListView):
    model = Author
    template_name = 'books/authors_list.html'


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'books/author_detail.html'
    pk_url_kwarg = 'numer_ajdi_autora'

    def get_context_data(self, **kwargs):
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


def book_detail(request, pk):
    book = Book.objects.get(pk=pk)
    return render(
        request,
        'books/book_detail.html',
        {'book': book}
    )


class HomePage(TemplateView):
    template_name = 'books/home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all()[:3]
        context['authors'] = Author.objects.all()[:3]
        return context


def create_book_comment_view(request, book_id):
    book = Book.objects.get(pk=book_id)
    if request.method == 'GET':
        return render(
            request,
            'books/book_comment_form.html',
            {'book': book},
        )
    elif request.method == 'POST':
        BookComment.objects.create(
            book=book,
            author=request.POST.get('kto_to_napisal_w_ogole'),
            content=request.POST.get('content'),
        )
        return HttpResponseRedirect(reverse('book_detail', kwargs={'pk': book_id}))


class ContactView(FormView):
    form_class = ContactForm
    template_name = 'books/contact_form.html'
    success_url = reverse_lazy('authors_list')

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


class AuthorContactView(FormView):
    form_class = AuthorContactForm
    template_name = 'books/author_contact_form.html'
    success_url = reverse_lazy('mail-send')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['author_id'] = self.kwargs.get('pk')
        return kwargs

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


class MailSendView(TemplateView):
    template_name = 'books/mail_send.html'
