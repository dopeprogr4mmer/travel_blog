from django.db import models
from django.contrib.auth import get_user_model
from PIL import Image

# Create your models here.

User = get_user_model()
username = User.username

class  Profile(models.Model):
	"""docstring for  Profiles"""
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default = 'profile_pics/default.png', upload_to = 'profile_pics')
	email = models.EmailField(blank = True, null = True)

	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		img = Image.open(self.image.path)
		if img.height>300 or img.width>300:
			#output_size = (300, 300)
			img.thumbnail(300, 300)
			img.save(self.image.path)

	def get_absolute_url(self):
		return reverse('profiles:get-author', kwargs = { 'pk' : self.user })

	# def get_update_url(self):
	# 	return reverse('myposts:post-update', kwargs = { 'pk' : self.pk })

	# def get_delete_url(self):
	# 	return reverse('myposts:post-delete', kwargs = { 'pk' : self.pk })
