# posts/views.py
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Status, Priority
from django.http import HttpResponseRedirect

class PostListView(ListView):
    template_name = "posts/list.html"
    model = Post

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('signup'))  # Redirect to signup page if user is not authenticated

        if not request.user.role:
            return HttpResponseRedirect(reverse_lazy('signup'))  # Redirect to signup page if user has no role

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role == 'product_owner':
            return queryset
        else:
            return queryset.filter(assignee__team=self.request.user.team)


class DraftPostListView(LoginRequiredMixin, ListView):
    template_name = "posts/list.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        draft_status = Status.objects.get(name="draft")
        context["post_list"] = Post.objects.filter(status=draft_status).filter(author=self.request.user).order_by("created_on").reverse()
        return context

class PostDetailView(DetailView):
    template_name = "posts/detail.html"
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = "posts/new.html"
    model = Post
    fields = ["title", "subtitle", "body", "status", "priority", "assignee"]

    def test_func(self):
        return self.request.user.role == 'product_owner'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

                      
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "posts/edit.html"
    model = Post
    fields = ["title", "subtitle", "body", "status", "priority", "assignee"]

    def test_func(self):
        post = self.get_object()
        return self.request.user.role == 'product_owner' or post.author == self.request.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "posts/delete.html"
    model = Post
    success_url = reverse_lazy("list")

    def test_func(self):
        post = self.get_object()
        return self.request.user.role == 'product_owner' or post.author == self.request.user