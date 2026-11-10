from django.db import models

# Create your models here.

class User(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.email}"

class Profile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    personal_id = models.CharField(max_length=11)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return f"Profile of: {self.first_name} {self.last_name}"

class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.title}"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f"Cart of: {self.user.profile.first_name} {self.user.profile.last_name}"

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"

class Payment(models.Model):
    payment_method = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')

    def __str__(self):
        return f"{self.user.profile.first_name} {self.user.profile.last_name} - {self.amount}"

class ProductHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_history')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchase_history')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Product purchased by: {self.user.profile.first_name} {self.user.profile.last_name}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by: {self.user.profile.first_name} {self.user.profile.last_name}"

class Rating(models.Model):
    SCORE_CHOICES = [
        (1, '1 - ძალიან ცუდი'),
        (2, '2 - ცუდი'),
        (3, '3 - საშუალო'),
        (4, '4 - კარგი'),
        (5, '5 - შესანიშნავი'),
    ]

    purchased_item = models.OneToOneField(ProductHistory, on_delete=models.CASCADE, related_name='rating')
    score = models.PositiveSmallIntegerField(choices=SCORE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.purchased_item.product.title} - {self.score} stars"