from django.urls import reverse_lazy
from django.views.generic import ListView, FormView

from .models import Comment, User
from .forms import NewComment

menu = [
    {'title': "Home", 'url_name': 'home'},
    {'title': "New comment", 'url_name': 'new_comment'},
]


class CommentListView(ListView):
    model = Comment
    template_name = 'app/home.html'
    context_object_name = 'comments'
    paginate_by = 25

    def get_queryset(self):
        sort_field = self.request.GET.get('sort', '-created_date')
        queryset = Comment.objects.filter(parent_comment=self.request.GET.get('parent'))
        queryset = queryset.order_by(sort_field)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['parent_id'] = self.request.GET.get('parent', 0)
        return context




class NewCommentView(FormView):
    template_name = 'app/new_comment.html'
    form_class = NewComment
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_id'] = self.kwargs['parent_id']
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial['parent_id'] = self.kwargs['parent_id']
        return initial

    def form_valid(self, form):
        try:
            self.save(form.cleaned_data)
            return super().form_valid(form)
        except Exception as ex:
            form.add_error(None, ex)
            return self.render_to_response(self.get_context_data(form=form))

    def save(self, cleaned_data):
        user_model, created = User.objects.get_or_create(
            user_name=cleaned_data['user_name'],
            email=cleaned_data['email'],
            home_page=cleaned_data['home_page']
        )

        if cleaned_data['parent_id'] != 0:
            parent_id = cleaned_data['parent_id']
            parent_comment = Comment.objects.get(id=parent_id)

            Comment.objects.create(
                user_name=user_model,
                text=cleaned_data['text'],
                parent_comment=parent_comment
            )
        else:
            Comment.objects.create(
                user_name=user_model,
                text=cleaned_data['text'],
            )

