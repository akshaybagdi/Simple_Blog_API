from django.urls import path
from .views import PostListView, PostDetailView, PostUpdateView, PostDestroyView, PostCreateView
from rest_framework import routers

app_name = 'posts'  # Namespace for the posts app

# explicitly mapped methods to specific viewset actions using as_view()
simple_router = routers.SimpleRouter()
Delete_Post = PostDestroyView.as_view({'post': 'destroy'})
Update_Post = PostUpdateView.as_view({'post': 'update'})
List_Post_ID = PostDetailView.as_view({'post': 'create'})
Create_post = PostCreateView.as_view({'post': 'create'})


List_Posts = PostListView.as_view({'post': 'list'})

urlpatterns = simple_router.urls

urlpatterns = urlpatterns + [
    path('posts/list/', List_Posts, name='List_Posts'),
    path('posts/postid/', List_Post_ID, name='List_Post_ID'),
    path('posts/create/', Create_post, name='Create_post'),
    path('posts/update/', Update_Post, name='Update_Post'),
    path('posts/delete/', Delete_Post, name='Delete_Post'),
]
