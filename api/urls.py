from django.urls import path, include
from rest_framework.routers import DefaultRouter
from catalog.views import AuthorViewSet, BookViewSet

from operations.views import BorrowRecordViewSet

router = DefaultRouter()
router.register('authors', AuthorViewSet,basename='authors')
router.register('books', BookViewSet,basename='books')
router.register('borrow', BorrowRecordViewSet, basename='borrow')

urlpatterns = [
  
    path('', include(router.urls)),
  
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api-auth/', include('rest_framework.urls')),
]
