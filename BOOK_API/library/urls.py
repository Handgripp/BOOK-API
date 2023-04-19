from django.urls import path
from .views import BookList, BookCreateView, BookEditView, BookImportView

urlpatterns = [
    path("books/", BookList.as_view(), name="book_list"),
    path("books/new/", BookCreateView.as_view(), name="book_create"),
    path('edit/<int:pk>/', BookEditView.as_view(), name='book_edit'),
    path('book-import/', BookImportView.as_view(), name='book_import'),
]