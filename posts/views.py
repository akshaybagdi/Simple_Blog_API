from django.utils.decorators import method_decorator
from rest_framework import filters, mixins, viewsets, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models.models import Post
from .serializers.serializers import PostSerializer
from .pagniations.pagniations import CustomPagination
from .utlis import PostID
from core.permission import UserPermission
from core.decorators import validate_payload

"""
Using mixins allows us to add specific functionality (e.g., list, delete,retrieve) to views.
viewsets.GenericViewSet provides the base functionality for creating custom views with mixins.
"""


class PostListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Post.objects.all()  # Fetch all Post objects
    serializer_class = PostSerializer  # Serialize Post model data
    pagination_class = CustomPagination  # Paginate the results
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]  # Enable search and ordering
    search_fields = ['title', 'content']  # Searchable fields
    ordering_fields = ['publication_date']  # Fields to order by
    ordering = ['-publication_date']  # Default ordering (newest first)
    authentication_classes = [JWTAuthentication]  # Use JWT for authentication
    permission_classes = [IsAuthenticated]  # Authenticated users can write; others can only read


class PostDetailView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):  # Handles retrieving a single post
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        post_id = request.data.get('id')  # Get the ID from the request payload
        post = PostID.get_post_by_id(post_id)  # Directly call the static method of PostH
        if isinstance(post, Response):  # If the helper(PostID) function returns a Response (error), return it directly
            return post
        serializer = self.get_serializer(post)  # Otherwise, process the post instance and return the response
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostUpdateView(mixins.UpdateModelMixin, viewsets.GenericViewSet):  # Handles updating a post
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    permission_classes = [permissions.IsAuthenticated, UserPermission]

    def update(self, request, *args, **kwargs):
        print(f"Authenticated user: {request.user}")
        # post_id = self.get_object()
        post_id = request.data.get('id')  # Extract post ID from payload
        data = request.data  # Full payload
        print("Received payload:", data)

        try:
            updated_post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"Error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, updated_post)

        updated_post = PostID.update_post(post_id, data)  # Call the `update_post` method
        if isinstance(updated_post, Response):  # If the helper method returns a Response, return it directly
            return updated_post
        serializer = self.get_serializer(updated_post)  # Serialize the updated post and return a success response
        return Response({"message": "Post updated successfully.", "post": serializer.data}, status=status.HTTP_200_OK)


class PostDestroyView(mixins.DestroyModelMixin, viewsets.GenericViewSet):  # Handles deleting a post
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, UserPermission]

    def destroy(self, request, *args, **kwargs):
        post_id = request.data.get('id')  # Get the ID from the request payload
        try:
            delete_post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"Error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, delete_post)
        response = PostID.delete_post_by_id(post_id)  # Call the helper method to delete the post
        return response  # Return the response from the helper method


class PostCreateView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    # queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]

    @validate_payload(['title', 'content', 'volume'])  # Apply the custom decorator
    def create(self, request, *args, **kwargs):
        # Manually handle the creation logic
        payload = request.data
        serializer = self.get_serializer(data=payload)

        if serializer.is_valid():
            serializer.save(author=request.user)  # Assign the authenticated user as the author before saving
            return Response(
                {"Message": "Post created successfully!", "post": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
