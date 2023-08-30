from django import forms
from catalog.models import Product, Version


class VisualMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class ProhibitedWordsMixin:
    def clean(self):
        cleaned_data = super().clean()
        name = self.cleaned_data['name'].lower()
        description = self.cleaned_data['description'].lower()

        prohibited_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

        for word in prohibited_words:
            if word in name.lower():
                raise forms.ValidationError('Название содержит запрещенное слово!')
            if word in description.lower():
                raise forms.ValidationError('Описание содержит запрещенное слово!')

        return cleaned_data

class ProductForm(VisualMixin, ProhibitedWordsMixin, forms.ModelForm):
    class Meta:
        model = Product
        # fields = ('name', 'description', 'image', 'category', 'price',)
        exclude = ('status', 'owner')

class ProductCuttedForm(VisualMixin, forms.ModelForm):
    # name = forms.CharField(disabled=True)
    # image = forms.ImageField(disabled=True)
    # price = forms.IntegerField(disabled=True)

    class Meta:
        model = Product
        fields = ('description', 'category', 'status')


class VersionForm(VisualMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = ('version_num', 'version_name', 'version_activ')
