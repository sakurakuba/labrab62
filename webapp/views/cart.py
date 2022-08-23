from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView

from webapp.forms import CartForm, OrderForm, ProductForm
from webapp.models import Cart, Product, Order, OrderProduct


class CartAddView(CreateView):
    form_class = ProductForm

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs.get("pk"))
        qty = form.cleaned_data.get("qty")

        if qty > product.amount:
            return HttpResponseBadRequest(
                f"Количество товара {product.name} всего {product.amount}. Добавить {qty} штук не получится")

        if product.pk not in self.request.session:
            self.request.session[product.pk] = qty

        else:
            self.request.session[product.pk] += qty
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        next = self.request.GET.get("next")
        if next:
            return next
        return reverse("webapp:index")


class CartView(ListView):
    model = Product
    template_name = "cart/cart_view.html"
    context_object_name = "cart"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['total'] = self.get_total()
        context['form'] = OrderForm()
        return context

    def product_total(self, key):
        #product = get_object_or_404(Product, pk=self.kwargs.get("pk"))
        return self.request.session.get(key) * product.price

    def get_total(self):
        total = 0
        for key, val in self.request.session.items():
            if key == Product.objects.all():
                total += self.product_total(key)
        return total


class CartDeleteView(DeleteView):
    model = Cart
    success_url = reverse_lazy('webapp:cart')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class CartDeleteOneView(DeleteView):
    model = Cart
    success_url = reverse_lazy('webapp:cart')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        cart = self.object
        cart.qty -= 1
        if cart.qty < 1:
            cart.delete()
        else:
            cart.save()
        return HttpResponseRedirect(success_url)


class OrderCreate(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('webapp:index')

    # def form_valid(self, form):
    #     order = form.save()
    #     for item in Cart.objects.all():
    #         OrderProduct.objects.create(product=item.product, qty=item.qty, order=order)
    #         item.product.amount -= item.qty
    #         item.product.save()
    #         item.delete()
    #
    #     return HttpResponseRedirect(self.success_url)

    def form_valid(self, form):
        order = form.save()

        products = []
        order_products = []

        for item in Cart.objects.all():
            order_products.append(OrderProduct(product=item.product, qty=item.qty, order=order))
            item.product.amount -= item.qty
            products.append(item.product)

        OrderProduct.objects.bulk_create(order_products)
        Product.objects.bulk_update(products, ("amount",))
        Cart.objects.all().delete()
        return HttpResponseRedirect(self.success_url)
