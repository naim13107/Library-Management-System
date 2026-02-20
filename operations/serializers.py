# operations/serializers.py
from rest_framework import serializers
from .models import BorrowRecord

class BorrowRecordSerializer(serializers.ModelSerializer):
    book_name = serializers.CharField(source='book.title', read_only=True)
    member_name = serializers.CharField(source='member.email', read_only=True)
    class Meta:
        model = BorrowRecord
        fields = ['id', 'book', 'book_name', 'member', 'member_name', 'borrow_date', 'return_date']
        read_only_fields = ['member', 'borrow_date', 'return_date']