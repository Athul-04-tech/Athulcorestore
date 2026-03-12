from django.contrib import admin
<<<<<<< HEAD
from .models import (
    SellerProfile,
    Product,
    ProductVariant,
    ProductImage,
    Attribute,
    AttributeOption,
    VariantAttributeBridge,
    InventoryLog,
)

admin.site.register(SellerProfile)
admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(ProductImage)
admin.site.register(Attribute)
admin.site.register(AttributeOption)
admin.site.register(VariantAttributeBridge)
admin.site.register(InventoryLog)
=======
from .models import Product,ProductVariant,ProductImage,Attribute,AttributeOption,VariantAttributeBridge,SellerProfile,ReturnRequest
# Register your models here.
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductVariant)
admin.site.register(Attribute)
admin.site.register(SellerProfile)
admin.site.register(ReturnRequest)
>>>>>>> 0535505a6c50a24310abeca2da23094c6efe64aa
