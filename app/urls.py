
from django.urls import path

from .views import CommentListView, NewCommentView, CommentDetailView, CommentDeleteView

urlpatterns = [
    path('', CommentListView.as_view(), name='home'),
    path('new_comment/<int:parent_id>', NewCommentView.as_view(), name='new_comment'),
    path('comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment_delete'),
    path('comment/<int:pk>/', CommentDetailView.as_view(), name='comment_detail'),
]
