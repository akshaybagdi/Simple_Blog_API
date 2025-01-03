from rest_framework import generics, permissions, status, viewsets
from rest_framework.exceptions import NotFound
from core.permission import UserPermission
from .models.models import Comment
from .serializers.serializers import CommentSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .utlis import CommentID
from rest_framework.response import Response


class CommentListView(generics.ListAPIView, viewsets.GenericViewSet):
    # queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, UserPermission]

    def get_queryset(self):
        comment_id = self.request.data.get("id")  # Fetch the 'id' from the request payload
        print(f"Received comment ID: {comment_id}")
        if comment_id:
            queryset = Comment.objects.filter(id=comment_id)
            if not queryset.exists():
                raise NotFound(
                    detail="No comment found with the given ID.")  # Raise NotFound exception if no comments are found
            return queryset
        return Comment.objects.all()  # Return all comments if no ID is provided


class CommentCreateView(generics.CreateAPIView, viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)


class CommentUpdateView(generics.UpdateAPIView, viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, UserPermission]

    def update(self, request, *args, **kwargs):
        print(f"Authenticated user: {request.user}")
        comment_id = request.data.get('id')
        data = request.data
        try:
            updated_comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"Error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, updated_comment)
        updated_comment = CommentID.update_comment(comment_id, data)  # Use the CommentID to update the comment
        if isinstance(updated_comment, Response):
            return updated_comment  # Return error if the comment is not found
        # Return the updated comment
        serializer = self.get_serializer(updated_comment)
        return Response({"Message": "Comment updated successfully.", "comment": serializer.data},
                        status=status.HTTP_200_OK)


class CommentDeleteView(generics.DestroyAPIView, viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, UserPermission]

    def destroy(self, request, *args, **kwargs):
        comment_id = request.data.get('id')
        try:
            delete_post = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"Error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, delete_post)
        # Use the CommentID to delete the comment
        deletion_response = CommentID.delete_comment_by_id(comment_id)

        if isinstance(deletion_response, Response):
            return deletion_response  # Return error if the comment is not found

        return Response({"message": "Comment successfully deleted."}, status=status.HTTP_200_OK)

# class CommentListCreateView(generics.ListCreateAPIView, viewsets.GenericViewSet):
#     serializer_class = CommentSerializer
#
#     def get_queryset(self):
#         post_id = self.kwargs['post_id']
#         return Comment.objects.filter(post_id=post_id)
