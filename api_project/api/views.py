# views.py (DRF)
from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]   # ✅ only authenticated users


# New ViewSet with full CRUD
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]   # default
    
    
    
def get_permissions(self):
        if self.action == 'destroy':  # DELETE
            return [IsAdminUser()]    # only admins can delete
        return super().get_permissions()