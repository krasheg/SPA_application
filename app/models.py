from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# Create your models here.
class User(AbstractUser):
    avatar = models.ImageField(upload_to='static/images/', null=True, blank=True,
                               default='static/images/default_avatar.webp')


def validate_text_file_extension(value):
    """Validator for uploaded file extension"""
    if not value.name.endswith('.txt'):
        raise ValidationError(_('You can upload .txt file only'))


def validate_text_file_size(value):
    """Validator for max file size"""
    if value.size > 100 * 1024:
        raise ValidationError(_("File size can't be more than 100 KB."))


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    text_file = models.FileField(upload_to='text_files/', null=True, blank=True,
                                 validators=[validate_text_file_extension, validate_text_file_size])
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Returns first 50 signs in comments"""
        return self.content[:50]

    @property
    def is_top_level(self):
        """Returns True if comment is parental"""
        return self.parent is None

    @property
    def user_name(self):
        """Access to author`s username"""
        return self.user.username

    @property
    def email(self):
        """Access to author`s email"""
        return self.user.email

    @classmethod
    def get_top_level_comments(cls):
        """Method returns all parental comments"""
        return cls.objects.filter(parent=None).order_by('-timestamp')

    class Meta:
        """Here we add ordering LIFO"""
        ordering = ['-timestamp']
