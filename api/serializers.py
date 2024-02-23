from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import serializers
from app.models import Comment, User
from app.validators import validate_html_tags, validate_image, validate_text_file_extension, validate_text_file_size


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'user_name', 'email', 'home_page']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user_name', 'text', 'parent_comment', 'file', 'image', 'created_date']

    def validate_text(self, value):
        validate_html_tags(value)
        return value

    def validate_image(self, image):
        if image:
            name = image.name
            img = validate_image(image)
            if img is not None:
                image = SimpleUploadedFile(f'comment_images/upgraded_{name}', img)
        return image

    def validate_file(self, file):
        if file:
            for i in file:
                if i is not None:
                    validate_text_file_extension(i)
                    validate_text_file_size(i)
        return file
