from rest_framework.response import Response
from rest_framework import status
from .models.models import Post


class PostID:
    @staticmethod
    def get_post_by_id(post_id):
        """
        Retrieve a post by its ID.
        :param post_id: The ID of the post to retrieve
        :return: Post instance or Response with error message
        """
        if not post_id:
            return Response({"Error": "Post ID is required in the payload."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            post = Post.objects.get(id=post_id)
            return post  # Return the post instance for further processing
        except Post.DoesNotExist:
            return Response({"Error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def delete_post_by_id(post_id):
        """Delete a post by its ID.
        :param post_id: The ID of the post to deletereturn
        :Response object with success or error message"""
        post = PostID.get_post_by_id(post_id)
        if isinstance(post, Response):
            return post  # Return error Response directly
        post.delete()
        return Response({"message": "Post successfully deleted."}, status=status.HTTP_200_OK)

    @staticmethod
    def update_post(post_id, data):
        # Retrieve the post
        post = PostID.get_post_by_id(post_id)
        if isinstance(post, Response):  # If the retrieval returns a Response (error), return it
            return post
        for field, value in data.items():  # Update fields dynamically
            try:
                setattr(post, field, value)  # Dynamically update attributes
            except AttributeError:
                return Response({"Error": f"Invalid field '{field}' provided for update."},
                                status=status.HTTP_400_BAD_REQUEST)
        # Save the updated post
        post.save()
        return post
