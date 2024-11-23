from django.db import models
from django.utils import timezone
from django.db.models import Sum

class Product(models.Model):
    """Mahsulot"""
    name = models.CharField(max_length=100)
    time_per_unit = models.IntegerField(help_text="Bir dona mahsulot uchun ketadigan vaqt (minutda)")
    
    def __str__(self):
        return self.name

class ProductionLine(models.Model):
    """Patok"""
    name = models.CharField(max_length=100)
    worker_time_per_day = models.IntegerField(
        default=500,
        help_text="Bir ishchining bir kundagi ishlash vaqti (minutda)"
    )
    
    def __str__(self):
        return self.name

class DailyProduction(models.Model):
    """Kunlik ishlab chiqarish"""
    date = models.DateField()
    production_line = models.ForeignKey(ProductionLine, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='DailyProductionProduct')
    workers_count = models.IntegerField(help_text="Ishchilar soni")
    
    total_minutes = models.IntegerField(
        help_text="Umumiy ishchi vaqti (workers_count * worker_time_per_day)",
        editable=False
    )

    def save(self, *args, **kwargs):
        # Umumiy ishchi vaqtini hisoblash
        self.total_minutes = self.workers_count * self.production_line.worker_time_per_day
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} - {self.production_line}"

class DailyProductionProduct(models.Model):
    """Kunlik ishlab chiqarish mahsuloti"""
    daily_production = models.ForeignKey(DailyProduction, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    expected_quantity = models.FloatField(help_text="Kutilayotgan mahsulot soni", editable=False)
    actual_quantity = models.IntegerField(default=0, help_text="Haqiqiy ishlab chiqarilgan mahsulot soni")
    
    def save(self, *args, **kwargs):
        # Kutilayotgan mahsulot sonini hisoblash
        self.expected_quantity = (
            self.daily_production.total_minutes / self.product.time_per_unit
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.daily_production.date} - {self.product}"

class ProductionHourlyRecord(models.Model):
    """Soatlik ishlab chiqarish qaydnomasi"""
    daily_production = models.ForeignKey(DailyProduction, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(help_text="Shu vaqtgacha qilingan mahsulot soni")
    minutes_spent = models.IntegerField(help_text="Ushbu mahsulot uchun sarflangan vaqt (minutda)")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Kunlik mahsulot ishlab chiqarish miqdorini yangilash
        daily_product, created = DailyProductionProduct.objects.get_or_create(
            daily_production=self.daily_production, product=self.product
        )
        daily_product.actual_quantity = self.quantity
        daily_product.save()

    def __str__(self):
        return f"{self.timestamp} - {self.product} - {self.quantity}"

