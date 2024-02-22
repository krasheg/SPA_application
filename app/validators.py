from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re


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
