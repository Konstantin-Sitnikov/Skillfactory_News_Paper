from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import cache


class Author(models.Model):
    rating_autor = models.IntegerField(default = 0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    post_count = models.IntegerField(default = 0)

    def __str__(self):
        return self.user.username.title()

    def get_count(self):
        self.post_count += 1
        self.save()

    def get_count_null(self):
        self.post_count = 0
        self.save()

    def update_rating(self):
        rating_post = 0
        rating_comment = 0
        rating_post_comment = 0
        post = Post.objects.filter(autor_id=self)
        for p in post:
            rating_post += p.rating_post

        comment = Comment.objects.filter(user_id=self.user)
        for c in comment:
            rating_comment += c.rating_comments

        post_comment = Comment.objects.filter(post_id__autor_id=self)
        for p_c in post_comment:
            rating_post_comment += p_c.rating_comments

        self.rating_autor = rating_post * 3 + rating_comment + rating_post_comment
        self.save()


class Post(models.Model):
    news = "NW"
    article = "AR"

    POSITIONS = [(news, "Новость"),
                 (article, "Статья")]

    autor_id = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length = 2, choices=POSITIONS, default=news)
    date_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField("Category", through="PostCategory")
    title_news = models.CharField(max_length = 128)
    text_news = models.TextField()
    rating_post = models.IntegerField(default = 0)

    def like(self):
        self.rating_post += 1
        self.save()

    def dislike(self):
        self.rating_post -= 1
        self.save()

    def preview(self):
        return self.text_news[0:123] + "..."

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')



class Category(models.Model):
    category = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, related_name="categories")

    def __str__(self):
        return self.category



class PostCategory(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.CharField(max_length = 255)
    date_time = models.DateTimeField(auto_now_add=True)
    rating_comments = models.IntegerField(default=0, db_column='rating_comments')

    def like(self):
        self.rating_comments += 1
        self.save()

    def dislike(self):
        self.rating_comments -= 1
        self.save()

class Censorship(models.Model):
    word = models.CharField(max_length = 255, unique=True)

    def __str__(self):
        return f'{self.word}'
