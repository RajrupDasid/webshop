from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator

STATE_CHOICE=(
    ('Andaman & Nicobar Island','Andaman & Nicrobar Island'),
    ('Andhra Pradesh','Andhra Pradesh'),
    ('Arunachal Pradesh','Arunachal Pradesh'),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('Chandigarh','Chandigarh'),
    ('Chhattishgarh','Chhattishgarh'),
    ('Dadar & Nagar Haveli','Dadar & Nagar Haveli'),
    ('Daman and Diu','Daman & Diu'),
    ('Delhi','Delhi'),
    ('Mumbai','Mumbai'),
    ('Rajasthan','Rajasthan'),
    ('UttraKhand','Uttrakhand'),
    ('Uttar Pradesh','Uttar Pradesh'),
    ('West Bengal','West Bengal'),
)
class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=120)
    locality=models.CharField(max_length=120)
    city=models.CharField(max_length=100)
    zipcode = models.IntegerField()
    state=models.CharField(choices=STATE_CHOICE,max_length=100)
    def __str__(self):
        return str(self.id)
CATEGOTY_CHOICE=(
    ('M','Mobile'),
    ('L','Laptop'),
    ('GP','Graphics Card'),
    ('CP','Processors'),
)
class Product(models.Model):
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    discount_price=models.FloatField()
    description=models.TextField()
    brand=models.CharField(max_length=100)
    category=models.CharField(choices=CATEGOTY_CHOICE,max_length=2)
    product_image=models.ImageField(upload_to='productimg')
    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    def __str__(self):
        return str(self.id)
    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price
STATUS_CHOICES=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)

class OrderPlaced(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')
    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price


