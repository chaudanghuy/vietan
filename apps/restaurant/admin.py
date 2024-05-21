from django.contrib import admin
from .models import Restaurant, Menu, Food, FoodSub, Translation, Category, CategorySub, MyTable, Booking

# Register your models here.
admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(Food)
admin.site.register(FoodSub)
admin.site.register(Translation)
admin.site.register(Category)
admin.site.register(CategorySub)
admin.site.register(MyTable)
admin.site.register(Booking)