from django.contrib import admin
from .models import Product, ProductionLine, PatokDailyIsh, PatokDailyProducts, SoatlikProductPatok

admin.site.register(Product)
admin.site.register(ProductionLine)
admin.site.register(PatokDailyIsh)
admin.site.register(PatokDailyProducts) 
admin.site.register(SoatlikProductPatok)    
