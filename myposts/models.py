from tinymce import HTMLField
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from profiles.models import Profile
# Create your models here.


User = get_user_model()
Profile = Profile()

class PostView(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	post = models.ForeignKey('Post', on_delete = models.CASCADE)

	def __str__(self):
		return self.user.username


class Comment(models.Model):
	user = models.ForeignKey(Profile, on_delete = models.CASCADE)
	timestamp = models.DateTimeField(auto_now_add = True)
	comment_content = models.TextField(blank = True, null = True)
	post = models.ForeignKey('Post', related_name = 'comments', on_delete = models.CASCADE)

	def __str__(self):
		return self.user.username


class Author(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE) 
	profile_picture = models.ImageField(default='img/user.png')

	def __str__(self):
		return self.user.username


class Category(models.Model):
	title = models.CharField(max_length = 100)

	class Meta:
		verbose_name_plural = "Categories"

	def __str__(self):
		return self.title


class Post(models.Model):
	title = models.CharField(max_length = 100)
	overview = models.CharField(max_length = 200)
	timestamp = models.DateTimeField(auto_now_add = True)
	post_content = HTMLField()
	#comment_count = models.IntegerField(default = 0)
	#view_count = models.IntegerField(default = 0)
	author = models.ForeignKey(Author, on_delete = models.CASCADE)
	thumbnail = models.ImageField(upload_to='uploads')
	categories = models.ManyToManyField(Category)
	featured = models.BooleanField()
	previous_post = models.ForeignKey('self', related_name = 'previous', on_delete = models.SET_NULL, blank = True, null = True)
	next_post = models.ForeignKey('self', related_name = 'next', on_delete = models.SET_NULL, blank = True, null = True)


	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('myposts:post-detail', kwargs = { 'pk' : self.pk })

	def get_update_url(self):
		return reverse('myposts:post-update', kwargs = { 'pk' : self.pk })

	def get_delete_url(self):
		return reverse('myposts:post-delete', kwargs = { 'pk' : self.pk })

	@property
	def get_comments(self):
		return self.comments.all().order_by('-timestamp')

	@property 
	def view_count(self):
		return PostView.objects.filter(post = self).count()

	@property 
	def comment_count(self):
		return Comment.objects.filter(post = self).count()

