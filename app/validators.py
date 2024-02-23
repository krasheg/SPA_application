from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re
import io
import pathlib
from PIL import Image


def validate_text_file_extension(value):
    """Validator for uploaded file extension"""
    if not value.name.endswith('.txt'):
        raise ValidationError(_('You can upload .txt file only'))


def validate_text_file_size(value):
    """Validator for max file size"""
    if value.size > 100 * 1024:
        raise ValidationError(_("File size can't be more than 100 KB."))


def validate_html_tags(value):
    """Validator for comment content, using rules from task"""

    # Regular expression for allowed HTML tags and their attributes
    allowed_tags = ['a', 'code', 'i', 'strong']

    html_tags = re.findall(r"</?(.*?)>", str(value))
    for tag in html_tags:
        if tag not in allowed_tags:
            raise ValidationError(f"HTML tag '{tag}' is not allowed")

    opening_tags = re.findall(r"<\s*([a-zA-Z]+)(?=[^>]*?>)", str(value))
    closing_tags = re.findall(r"<\s*/\s*([a-zA-Z]+)\s*>", str(value))
    if len(opening_tags) != len(closing_tags):
        raise ValidationError("HTML tags are not closed")


def validate_image(image):
    image_content = image.read()

    with Image.open(io.BytesIO(image_content)) as img:
        file_ext = pathlib.Path(image.name).suffix

        if file_ext.lower() in (".jpg", ".png", ".gif"):
            if img.width > 320 or img.height > 240:
                img.thumbnail((320, 240))
                output = io.BytesIO()
                img.save(output,
                         format='PNG')
                return output.getvalue()
            else:
                return None
    raise ValidationError("Image is not valid!")
