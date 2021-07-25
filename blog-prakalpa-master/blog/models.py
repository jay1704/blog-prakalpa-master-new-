from django.db import models
from django.utils import timezone
from django.urls import reverse_lazy
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.shortcuts import redirect
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class Post(models.Model):
    slug = models.SlugField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    image = models.ImageField(upload_to='media', blank=True, null=True)
    publish_date = models.DateTimeField(default=timezone.now())
    
    class Meta:
        ordering = ["-publish_date"]
    
    def get_api_url(self):
        try:
            return reverse_lazy("post_detail", kwargs={"slug":self.slug})
        except:
            None

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def __str__(self):
        return self.title

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter(post=instance)
        return qs

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Post)
    
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now())
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()
    
    def get_absolute_url(self):
        return reverse_lazy('list_post')
    
    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return self.text