from django import forms
from catalog.models import Product


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'category', 'price')


    def clean_name(self):
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        cleaned_data = self.cleaned_data.get('name')
        for word in forbidden_words:
            if word in cleaned_data.lower():
                raise forms.ValidationError('Запрещенное название')
        return cleaned_data

