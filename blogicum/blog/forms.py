"""Forms for publications, comments and personal profiles."""
from django import forms
from django.contrib.auth import get_user_model

from .models import Comment, Post


class PostForm(forms.ModelForm):
    """Publication fields editable by its author."""

    class Meta:
        """Keep authorship and moderation under server control."""

        model = Post
        fields = ('title', 'text', 'pub_date', 'category', 'location', 'image')
        widgets = {'pub_date': forms.DateTimeInput(
            format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'},
        )}


class CommentForm(forms.ModelForm):
    """Only a comment's text is editable."""

    class Meta:
        """Bind the comment model."""

        model = Comment
        fields = ('text',)


class ProfileForm(forms.ModelForm):
    """Editable personal information."""

    class Meta:
        """Exclude permissions and authentication secrets."""

        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'email')
