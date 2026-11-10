from django.contrib import admin
from temp_app.models import User, Profile, Product, Cart, CartItem, Payment, ProductHistory, Comment, Rating

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Payment)
admin.site.register(ProductHistory)
admin.site.register(Comment)
admin.site.register(Rating)