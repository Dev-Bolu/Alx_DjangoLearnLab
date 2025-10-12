# posts/views.py
from rest_framework import viewsets, permissions, filters, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

User = get_user_model()


# ---------------------------------------------------------------------
# 🔹 STANDARD PAGINATION
# ---------------------------------------------------------------------
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# ---------------------------------------------------------------------
# 🔹 POST VIEWSET
# ---------------------------------------------------------------------
class PostViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for posts.

    - List/Retrieve: Open to all users (IsAuthenticatedOrReadOnly)
    - Create: Authenticated users only (author is auto-assigned)
    - Update/Delete: Only post author (IsOwnerOrReadOnly)
    """
    queryset = Post.objects.all().select_related('author')
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = []  # You can add more filters later
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# ---------------------------------------------------------------------
# 🔹 COMMENT VIEWSET
# ---------------------------------------------------------------------
class CommentViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for comments.

    - Create: Authenticated users only.
    - Update/Delete: Only comment author.
    """
    queryset = Comment.objects.all().select_related('author', 'post')
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['post']
    search_fields = ['content']
    ordering_fields = ['created_at', 'updated_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# ---------------------------------------------------------------------
# 🔹 FEED VIEW
# ---------------------------------------------------------------------
class FeedView(generics.ListAPIView):
    """
    Returns posts from users that the current user follows.

    Endpoint:
        GET /api/feed/

    Requires token authentication.
    """
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all() if hasattr(user, 'following') else User.objects.none()
        return Post.objects.filter(author__in=following_users).order_by('-created_at')
