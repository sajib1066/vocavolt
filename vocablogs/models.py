from django.db import models
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify


class TaggedArticle(TaggedItemBase):
    content_object = models.ForeignKey(
        "Article", on_delete=models.SET_NULL, blank=True, null=True
    )


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Article(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='articles'
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    short_description = models.TextField()
    content = RichTextUploadingField()
    tags = TaggableManager(verbose_name='Tag List', through=TaggedArticle)
    is_active = models.BooleanField(default=True)
    view_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/vocablog/{self.slug}/'
