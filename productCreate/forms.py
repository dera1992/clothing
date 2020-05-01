from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Products,ProductsImages,Category,SubCategory



class AdsForm(forms.ModelForm):
    price = forms.DecimalField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'NGN'}
        )
    )
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}))
    available = forms.BooleanField()

    class Meta:
        model = Products
        fields = ('title', 'category','subcategory','price','discount_price','description','label','status','available')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subcategory'].queryset = SubCategory.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategory.order_by('name')


class AdsImageForm(forms.ModelForm):
    product_image = forms.ImageField(label='Image')
    class Meta:
        model = ProductsImages
        fields = ('product_image', )



class AdsEditForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), to_field_name='id', required=True,label='Type')
    price = forms.DecimalField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'NGN'}
        )
    )
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}))
    available = forms.BooleanField()

    class Meta:
        model = Products
        fields = ('title', 'category','subcategory','price','discount_price','description','label','status','available')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subcategory'].queryset = SubCategory.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategory_set.order_by('name')


class AdsEditImageForm(forms.ModelForm):
    product_image = forms.ImageField(label='Image')
    class Meta:
        model = ProductsImages
        fields = ('product_image', )



