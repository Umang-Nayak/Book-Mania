from django.contrib import admin
from book_admin.models import (Area, User, Category, Sub_category, Language, Book,
                               Order, Order_detail, Wishlist, Feedback, Cart)


admin.site.register(Area)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Sub_category)
admin.site.register(Language)
admin.site.register(Book)
admin.site.register(Order)
admin.site.register(Order_detail)
admin.site.register(Wishlist)
admin.site.register(Feedback)
admin.site.register(Cart)
