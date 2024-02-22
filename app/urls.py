from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import CommentListView, NewCommentView

urlpatterns = [
    path('', CommentListView.as_view(), name='home'),
    path('new_comment/<int:parent_id>', NewCommentView.as_view(), name='new_comment'),
]