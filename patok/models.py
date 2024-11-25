from typing import Iterable
from django.db import models
from django.utils import timezone
from django.db.models import Sum

class Product(models.Model):
    """Mahsulot"""
    name = models.CharField(max_length=100)
    time_per_unit = models.IntegerField(help_text="Bir dona mahsulot uchun ketadigan vaqt (minutda)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProductionLine(models.Model):
    """Patok"""
    name = models.CharField(max_length=100)
    worker_time_per_day = models.IntegerField(
        default=500,
        help_text="Bir ishchining bir kundagi ishlash vaqti (minutda)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class PatokDailyIsh(models.Model):
    """Patok kunlik ishlab chiqarish"""
    production_line = models.ForeignKey(ProductionLine, on_delete=models.CASCADE)
    workers_count = models.IntegerField(help_text="Ishchilar soni")
    productlar = models.ManyToManyField('PatokDailyProducts', related_name='daily_production_product')
    total_minutes = models.IntegerField(
        help_text="Umumiy ishchi vaqti (workers_count * worker_time_per_day)",
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Umumiy ishchi vaqtini hisoblash
        self.total_minutes = self.workers_count * self.production_line.worker_time_per_day
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.production_line} - {self.workers_count}"
    
class PatokDailyProducts(models.Model):
    """Patok kunlik ishlab chiqarish mahsuloti"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    kutilayotgan = models.FloatField(help_text="Kutilayotgan mahsulot soni", editable=False,default=0)
    real_ish = models.IntegerField(default=0, help_text="Haqiqiy ishlab chiqarilgan mahsulot soni")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs):
    #     # Kutilayotgan mahsulot sonini hisoblash
    #     self.kutilayotgan = self.daily_ish.total_minutes / self.product.time_per_unit
    #     super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.product} - {self.real_ish}"
    
class Clock(models.Model):
    clock = models.TimeField()
    def __str__(self) -> str:
        return f'{self.clock}'


class SoatlikProductPatok(models.Model):
    """Soatlik mahsulot patok"""
    patok  = models.ForeignKey(ProductionLine,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    clock = models.ForeignKey(Clock,on_delete=models.CASCADE)
    patokdailyish = models.ForeignKey(PatokDailyIsh,on_delete=models.CASCADE)
    patokproducts = models.ForeignKey(PatokDailyProducts,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    comment = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.product} - {self.patok}"
    


    
    