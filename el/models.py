from django.db import models

# Create your models here.
class Customer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    

class Product(models.Model):
    PURPOSE = (
        ('ELECTRICAL RED/ORANGE', 'ELECTRICAL RED/ORANGE'),
        ('POTABLE WATER - BLUE', 'POTABLE WATER - BLUE'),
        ('SANITARY ORANGE/BROWN', 'SANITARY ORANGE/BROWN'),
    )
    kind = models.CharField(max_length=50, default='PVC')
    purpose = models.CharField(max_length=50, choices=PURPOSE)
    description = models.CharField(max_length=50)
    size_in = models.CharField(max_length=50)
    size_mm = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.purpose} - {self.description} - {self.size_in} {self.size_mm} - {self.brand}'
    
    
class Order(models.Model):
    STATUS = (
        ('INITIAL', 'INITIAL'),
        ('PENDING', 'PENDING'),
        ('OUT FOR DELIVERY','OUT FOR DELIVERY'),
        ('DELIVERED','DELIVERED'),
    )
    customer = models.ForeignKey(Customer, on_delete= models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete= models.SET_NULL, null=True)
    status = models.CharField(max_length=50, choices=STATUS, default='INITIAL')
    qty = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return f'{self.id} - {self.customer}'