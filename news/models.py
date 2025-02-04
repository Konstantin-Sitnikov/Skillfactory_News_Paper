from django.db import models
from django.contrib.auth.models import User



class Author(models.Model):
    _rating_autor = models.IntegerField(default = 0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        pass


class Category(models.Model):
    category = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    news = "NW"
    article = "AR"

    POSITIONS = [(news, "Новость"),
                 (article, "Статья")]


    autor_id = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length = 2, choices=POSITIONS, default=news)
    date_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through="PostCategory")
    title_news = models.CharField(max_length = 128)
    text_news = models.TextField()
    _rating_post = models.IntegerField(default = 0, db_column='rating_post')

    def like(self):
        self._rating += 1
        self.save()

    def dislike(self):
        self._rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + "..."


class PostCategory(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.CharField(max_length = 255)
    date_time = models.DateTimeField(auto_now_add=True)
    _rating_comments = models.IntegerField(default=0, db_column='rating_comments')

    def like(self):
        self._rating += 1
        self.save()

    def dislike(self):
        self._rating -= 1
        self.save()

