
class GetTotal:
    self.qty = qty
    self.product_price = product_price

    def get_product_total(self):
        return qty * product_price

    def get_total(self):
        total = 0
        for cart in cls.objects.all():
            total += cart.get_product_total()
        return total
