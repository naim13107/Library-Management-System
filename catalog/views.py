from rest_framework import viewsets
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAdminUser
from rest_framework import viewsets, filters  
from catalog.pagination import DefaultPagination
class AuthorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows authors to be viewed or edited.
    
    * Any user can view the list of authors or specific author details.
    * Only Admin users can create, update, or delete authors.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = DefaultPagination

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()] 
        return [IsAdminUser()]

class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed or edited.
    
    * Any user can view the list of books or specific book details.
    * Supports searching by 'title' or the author's 'name' (?search=...).
    * Only Admin users can create, update, or delete books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author__name']
    pagination_class = DefaultPagination

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAdminUser()]