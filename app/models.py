from django.contrib.auth.models import AbstractUser
from django.db import models
from app.validators import validate_html_tags, validate_text_file_size, validate_text_file_extension


# Create your models here.


class Comment(models.Model):
    user_name = models.ForeignKey('User', to_field='id', on_delete=models.CASCADE)
    text = models.TextField(validators=[validate_html_tags])
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to='comment_files/', null=True, blank=True,
                            validators=[validate_text_file_size, validate_text_file_extension])
    image = models.ImageField(upload_to='comment_images/', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f'{self.user_name} - {self.text[:50]}'

    def save(self, *args, **kwargs):
        validate_html_tags(self.text)
        super().save(*args, **kwargs)


class User(models.Model):
    user_name = models.CharField(max_length=50)
    email = models.EmailField()
    home_page = models.URLField(blank=True)

    def __str__(self):
        return self.user_name
