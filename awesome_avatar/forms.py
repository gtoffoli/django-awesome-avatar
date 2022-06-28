from django import forms

from awesome_avatar.settings import config
from awesome_avatar.widgets import AvatarWidget

# 181206 GT - redefined  run_validators: see https://code.djangoproject.com/ticket/28148
# (addition of validate_image_file_extension() as a backwards incompatible change for ImageField)
from django.core.validators import FileExtensionValidator, get_available_image_extensions
def validate_image_file_extension(value):
    return FileExtensionValidator(allowed_extensions=get_available_image_extensions())(value['file'])

class AvatarField(forms.ImageField):
    widget = AvatarWidget

    def __init__(self, **defaults):
        self.width = defaults.pop('width', config.width)
        self.height = defaults.pop('height', config.height)
        self.disable_preview = defaults.pop('disable_preview', False)
        super(AvatarField, self).__init__(**defaults)

    def to_python(self, data):
        super(AvatarField, self).to_python(getattr(data, 'file', None))
        return data

    def widget_attrs(self, widget):
        return {'width': self.width, 'height': self.height, 'disable_preview': self.disable_preview}

    def run_validators(self, value):
        self.validators = [validate_image_file_extension]
        super(AvatarField, self).run_validators(value)
