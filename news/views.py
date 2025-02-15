from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse


from .forms import Publication
from .models import Post, Comment
from .filters import NewsFilter


# Create your views here.

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
        return context


class PublicationCreate(CreateView):
    form_class = Publication
    model = Post
    template_name = 'create_publication.html'

    def form_valid(self, form):
        publication = form.save(commit=False)
        if self.request.path == "/publication/news/create/":
            publication.type = "NW"
            return super().form_valid(form)
        if self.request.path == "/publication/article/create/":
            publication.type = "AR"
            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_news'] = (self.request.path == "/publication/news/create/")
        context['create_article'] = (self.request.path == "/publication/article/create/")
        return context



class PublicationUpdate(UpdateView):
    form_class = Publication
    model = Post
    template_name = 'create_publication.html'

    def form_valid(self, form):
        publication = form.save(commit=False)
        if publication.type == "NW" and self.request.path == f"/publication/news/{publication.pk}/edit/":
            return  super().form_valid(form)
        elif publication.type == "AR" and self.request.path == f"/publication/article/{publication.pk}/edit/":
            return  super().form_valid(form)
        else:
            return redirect("newsediterror")


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('news_list')


def news_update_delete_invalid(request):
    return HttpResponse("Ошибочка! Вы хотите изменить новость а выбрали сатью!")

def article_update_delete_invalid(request):
    return HttpResponse("Ошибочка! Вы хотите изменить Статью а выбрали Новость!")


