from django import forms
from webapp.models import Product, Cart, Order


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label='Найти')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = []


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ["qty"]


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["name", "phone", "address"]
