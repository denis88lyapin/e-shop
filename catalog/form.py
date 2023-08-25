from django import forms
from catalog.models import Product, Version


class VisualMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class ProductForm(VisualMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'category', 'price')

    def clean_name(self):
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        cleaned_data = self.cleaned_data.get('name')
        for word in forbidden_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError('Запрещенное название')
        return cleaned_data


class VersionForm(VisualMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = ('version_num', 'version_name', 'version_activ')
