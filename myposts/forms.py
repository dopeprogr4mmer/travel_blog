from django import forms
from tinymce import TinyMCE
from .models import Post, Comment



class TinyMCEWidget(TinyMCE):
	def use_required_atributes(self, *args):
		return False


class PostForm(forms.ModelForm):
	post_content = forms.CharField(
			widget = TinyMCEWidget(
					attrs = {'required':False, 'cols':30, 'rows':10}
				)
		)
	overview = forms.CharField(
			widget = forms.Textarea(
					attrs = {'required':False, 'cols':30, 'rows':2}
				)
		)

	class Meta:
		model = Post
		fields = ('title', 'overview', 'post_content', 'thumbnail', 'categories', 
			'featured', 'previous_post', 'next_post')

class CommentForm(forms.ModelForm):
	comment_content = forms.CharField(label = False,
				widget = forms.Textarea(
					attrs = {
						'required':False,
						'class': 'form-control',
						'placeholder':'Type your Comment',
						'id':'usercomment',
						'rows': 4
						}
					)
				)
								
	class Meta:
		model = Comment
		fields = ('comment_content', )