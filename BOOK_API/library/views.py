from django.views.generic import ListView
from .models import Books


class BookList(ListView):
    model = Books
    template_name = 'book_list.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
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