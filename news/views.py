from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse


from .forms import NewsForm, ArticleForm
from .models import Post
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


class NewsCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'create_news.html'
    def form_valid(self, form):
        news = form.save(commit=False)
        news.type = "NW"
        return super().form_valid(form)


class ArticleCreate(CreateView):
    form_class = ArticleForm
    model = Post
    template_name = 'create_article.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.type = "AR"
        return super().form_valid(form)


class NewsUpdate(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'create_news.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        if news.type == "NW":
            return  super().form_valid(form)
        else:
            return redirect("newsediterror")



class ArticleUpdate(UpdateView):
    form_class = ArticleForm
    model = Post
    template_name = 'create_article.html'

    def form_valid(self, form):
        article = form.save(commit=False)
        if article.type == "AR":
            return super().form_valid(form)
        else:
            return redirect("articleediterror")



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