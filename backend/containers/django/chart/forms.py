from django import forms
from django.core.files.storage import default_storage

# TODO https://blog.narito.ninja/detail/92/
class SingleUploadForm(forms.Form):
    file = forms.ImageField(label='画像ファイル')

    def save(self):
        upload_file = self.cleaned_data['file']
        file_name = default_storage.save(upload_file.name, upload_file)
        return default_storage.url(file_name)

