import requests
from django.views.generic import ListView, CreateView, DeleteView
from django.urls import reverse_lazy
from .models import Books
from .forms import BookForm
from django.views.generic.edit import UpdateView
from django.shortcuts import render, redirect
from django.views import View


class BookList(ListView):
    model = Books
    template_name = 'book_list.html'
    context_object_name = 'books'

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.GET.get('sort_by')
        if sort_by:
            if sort_by == 'title':
                queryset = queryset.order_by('title')
            elif sort_by == 'author':
                queryset = queryset.order_by('author')
            elif sort_by == 'published_date':
                queryset = queryset.order_by('published_date')

        title = self.request.GET.get('title')
        if title:
            queryset = queryset.filter(title__icontains=title)
        author = self.request.GET.get('author')
        if author:
            queryset = queryset.filter(author__icontains=author)
        language = self.request.GET.get('language')
        if language:
            queryset = queryset.filter(language__icontains=language)
        published_date_from = self.request.GET.get('published_date_from')
        if published_date_from:
            queryset = queryset.filter(published_date__gte=published_date_from)
        published_date_to = self.request.GET.get('published_date_to')
        if published_date_to:
            queryset = queryset.filter(published_date__lte=published_date_to)

        return queryset


class BookCreateView(CreateView):
    model = Books
    form_class = BookForm
    template_name = 'book_create.html'
    success_url = reverse_lazy('book_list')

    def form_valid(self, form):
        ISBN_number = form.cleaned_data['ISBN_number']
        title = form.cleaned_data['title']
        if Books.objects.filter(ISBN_number=ISBN_number).exists() or Books.objects.filter(title=title).exists():
            form.add_error('ISBN_number', 'This ISBN number already exists in the database.')
            return self.form_invalid(form)
        if Books.objects.filter(title=title).exists():
            form.add_error('title', 'A book with this title already exists.')
            return self.form_invalid(form)
        return super().form_valid(form)


class BookEditView(UpdateView):
    model = Books
    form_class = BookForm
    template_name = 'book_edit.html'
    success_url = reverse_lazy('book_list')

    def form_valid(self, form):
        ISBN_number = form.cleaned_data['ISBN_number']
        title = form.cleaned_data['title']
        existing_book = Books.objects.filter(ISBN_number=ISBN_number).exclude(id=self.object.id).first()
        if existing_book:
            form.add_error('ISBN_number', 'A book with this ISBN number already exists.')
            return self.form_invalid(form)
        existing_book_with_title = Books.objects.filter(title=title).exclude(id=self.object.id).first()
        if existing_book_with_title:
            form.add_error('title', 'A book with this title already exists.')
            return self.form_invalid(form)
        return super().form_valid(form)


class BookDeleteView(DeleteView):
    model = Books
    template_name = 'book_delete.html'
    success_url = reverse_lazy('book_list')


class BookImportView(View):

    def post(self, request):
        book_name = request.POST.get('book_name')
        if not book_name:
            return render(request, 'book_import.html', {'error_message': 'Please enter a book name'})

        response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={book_name}')
        if response.status_code != 200:
            return render(request, 'book_import.html', {'error_message': 'Unable to fetch data from Google Books API'})

        data = response.json()
        if 'items' not in data:
            return render(request, 'book_import.html', {'error_message': 'No books found with that name'})

        for item in data['items']:
            volume_info = item.get('volumeInfo', {})
            title = volume_info.get('title', '')
            author = volume_info.get('authors', [''])[0]
            published_date = volume_info.get('publishedDate', '')
            ISBN_number = volume_info.get('industryIdentifiers', [{'identifier': ''}])[0]['identifier']
            pages_numbers = volume_info.get('pageCount', 0)
            image_link = volume_info.get('imageLinks', {}).get('thumbnail', '')
            language = volume_info.get('language', '')

            if title and author and ISBN_number and published_date and language and pages_numbers:

                if Books.objects.filter(ISBN_number=ISBN_number).exists():
                    context = {'error_message': 'The book with this ISBN number already exists'}
                    return render(request, 'book_import.html', context=context)


                if book_name in title:
                    Books.objects.create(
                        title=title,
                        author=author,
                        published_date=published_date,
                        ISBN_number=ISBN_number,
                        pages_numbers=pages_numbers,
                        image_link=image_link,
                        language=language
                    )

        return redirect('book_list')

    def get(self, request):
        return render(request, 'book_import.html')
