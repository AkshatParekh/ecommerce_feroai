from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=18)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='order_customer')
    order_number = models.CharField(max_length=15, unique=True)
    order_date = models.DateField()
    address = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        # Check if the order is being created for the first time
        if not self.order_number:
            latest_order = Order.objects.order_by('-id').first()

            if latest_order:
                last_order_number = int(latest_order.order_number[6:])
                new_order_number = f"ORD0000{str(last_order_number + 1)}"
            else:
                new_order_number = "ORD00001"
            self.order_number = new_order_number

        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_item_order')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_item_product')
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product} -> {self.quantity}"
