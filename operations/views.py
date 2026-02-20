from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser 
from django.utils import timezone
from .models import BorrowRecord
from .serializers import BorrowRecordSerializer
from catalog.pagination import DefaultPagination

class BorrowRecordViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing book borrowing records.
    
    * Authenticated users can create a borrow record (checkout a book).
    * Normal users can only view their own borrow history.
    * Admin users can view all borrow records and delete records.
    """
    
    serializer_class = BorrowRecordSerializer
    pagination_class = DefaultPagination
    
    def get_permissions(self):
        
        if self.action == 'destroy':
            return [IsAdminUser()] 
        return [IsAuthenticated()] 

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return BorrowRecord.objects.all()
        return BorrowRecord.objects.filter(member=user)
    
    def perform_create(self, serializer):
        record = serializer.save(member=self.request.user) 
        record.book.is_available = False
        record.book.save()

    def perform_destroy(self, instance):
        if not instance.return_date:
            instance.book.is_available = True
            instance.book.save()
        instance.delete()

    @action(detail=True, methods=['post','get'])
    def return_book(self, request, pk=None):
        """
        Custom endpoint to mark a borrowed book as returned.
        
        Sets the return_date to the current timestamp and updates 
        the associated book's availability status to True.
        """
        record = self.get_object()
        
        if record.member != request.user and not request.user.is_staff:
            return Response({"detail": "You can only return your own books."}, status=status.HTTP_403_FORBIDDEN)

        if record.return_date:
            return Response({"detail": "Book is already returned."}, status=status.HTTP_400_BAD_REQUEST)
        
        record.return_date = timezone.now()
        record.save()
        
        record.book.is_available = True
        record.book.save()
        
        return Response({
            "status": "Success",
            "message": f"'{record.book.title}' was successfully returned by {record.member.email}!"
        })