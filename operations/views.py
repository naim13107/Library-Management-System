# operations/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
# Import IsAdminUser to check for staff/superuser status
from rest_framework.permissions import IsAuthenticated, IsAdminUser 
from django.utils import timezone
from .models import BorrowRecord
from .serializers import BorrowRecordSerializer

class BorrowRecordViewSet(viewsets.ModelViewSet):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer
    
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