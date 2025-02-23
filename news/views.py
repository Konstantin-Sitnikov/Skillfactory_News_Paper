from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required


from .forms import Publication
from .models import Post, Comment, Author, PostCategory
from .filters import NewsFilter



class PostList(ListView):
    model = Post
    ordering = '-date_time'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

class PostSearch(ListView):
    model = Post
    ordering = '-date_time'
    template_name = 'post_search.html'
    context_object_name = 'post_search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        publication = self.get_object()
        context = super().get_context_data(**kwargs)
        context['update_news'] = (publication.type == "NW")
        context['update_article'] = (publication.type == "AR")
        context['comments'] = Comment.objects.filter(post_id=publication.pk)

        print(publication.category)
        context['category'] = publication
        return context


class PublicationCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post', )
    form_class = Publication
    model = Post
    template_name = 'create_publication.html'

    def form_valid(self, form):

        publication = form.save(commit=False)
        author = Author.objects.get(user=self.request.user)
        if self.request.path == "/news/create/":

            publication.autor_id = author
            publication.type = "NW"

            return super().form_valid(form)
        if self.request.path == "/article/create/":
            publication.autor_id = author
            publication.type = "AR"
            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_news'] = (self.request.path == "/news/create/")
        context['create_article'] = (self.request.path == "/article/create/")
        return context



class PublicationUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = Publication
    model = Post
    template_name = 'create_publication.html'

    def form_valid(self, form):
        publication = form.save(commit=False)
        if publication.type == "NW" and self.request.path == f"/news/{publication.pk}/edit/":
            return  super().form_valid(form)
        elif publication.type == "AR" and self.request.path == f"/article/{publication.pk}/edit/":
            return  super().form_valid(form)
        else:
            return redirect("edit_delete_error")



class PublicationDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'publication_delete.html'
    success_url = reverse_lazy('news_list')


def edit_delete_invalid(request):
    return HttpResponse("Ошибочка! Неверный путь!")


def like_dislike(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == "POST":
        if request.POST.get("like") == "like":
            post.like()
            post.save()
            return redirect("news_detail", pk)
        elif request.POST.get("dislike") == "dislike":
            post.dislike()
            post.save()
            return redirect("news_detail", pk)





# @login_required
# def subscribe(request):
#     user = request.user
#     authors_group = Group.objects.get(name='authors')
#     if not request.user.groups.filter(name='authors').exists():
#         authors_group.user_set.add(user)
#         Author.objects.create(user=user)
#     return redirect('/protect/login/')