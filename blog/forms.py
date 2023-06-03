from .models import Comment, Post
from django import forms


class CommentForm(forms.ModelForm):

    class Meta:

        model = Comment
        fields = ('body', )


class ContactForm(forms.Form):

    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email_address = forms.EmailField(max_length=150)
    message = forms.CharField(widget=forms.Textarea, max_length=2000)


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('__all__')

		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control'}),
			'slug': forms.TextInput(attrs={'class': 'form-control'}),
			'author': forms.Select(attrs={'class': 'form-control'}),
			'category': forms.Select(attrs={'class': 'form-control'}),
			'excerpt': forms.Textarea(attrs={'class': 'form-control'}),			
			'content': forms.Textarea(attrs={'class': 'form-control'}),			
		}


class EditForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('__all__')

		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control'}),
			'slug': forms.TextInput(attrs={'class': 'form-control'}),
			'author': forms.Select(attrs={'class': 'form-control'}),
			'excerpt': forms.Textarea(attrs={'class': 'form-control'}),			
			'content': forms.Textarea(attrs={'class': 'form-control'}),			
		}