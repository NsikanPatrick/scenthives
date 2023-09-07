from django.db import models

# Create your models here.
from django.db import models
import uuid


# Create your models here.
class Category(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('B', 'Both'),
    )

    title = models.CharField(max_length=200)
    category_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    slug = models.SlugField(default=None)
    featured_product = models.OneToOneField('Perfume', on_delete=models.CASCADE, blank=True, null=True, related_name='featured_product')
    icon = models.CharField(max_length=100, default=None, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='B')

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    

class Perfume(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    discount = models. BooleanField(default=False)
    image = models.ImageField(upload_to = 'img/store',  blank = True, null=True, default='')
    price = models.FloatField(default=100.00)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='products')
    slug = models.SlugField(default=None, blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    inventory = models.IntegerField(default=5)
    top_deal=models.BooleanField(default=False)
    flash_sales = models.BooleanField(default=False)

    class Meta:
        ordering = ['price']  # Default pagination field for perfumes
    
    def __str__(self):
        return self.name


class PerfumeImage(models.Model):
    perfume = models.ForeignKey(Perfume, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="img/store", default="", null=True, blank=True)


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return str(self.id)

class Cartitems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', blank=True, null=True)
    perfume = models.ForeignKey(Perfume, on_delete=models.CASCADE, blank=True, null=True, related_name='cartitems')
    quantity = models.PositiveSmallIntegerField(default=0)


class Review(models.Model):
    perfume = models.ForeignKey("Perfume", on_delete=models.CASCADE, related_name = "reviews")
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(default="description")
    customer_name = models.CharField(max_length=50) 
    # The name field refers to the name of the person dropping the review
    # This should actually be grabbed from the logged in user
    
    def __str__(self):
        return self.description