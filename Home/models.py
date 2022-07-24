from django.db import models
from django.shortcuts import render, redirect,  HttpResponseRedirect
from django.contrib.auth.hashers import  check_password
from django.views import View
from django.contrib.auth.models import User
import datetime
import os

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    slug = models.SlugField(max_length=200, unique=True)
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    def __str__(self):
        return self.name

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name
    

def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('media/productimage/', filename)


class Product(models.Model):
    id=models.AutoField(auto_created=True,primary_key=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE,null=True, blank=True,)
    name = models.CharField(max_length=200, db_index=True,blank=True)
    slug = models.SlugField(max_length=200, db_index=True,blank=True)
    image=models.ImageField(upload_to=filepath,blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(null=True, blank=True,max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
   
    
    class Meta:
        db_table = "ProductForm"
        ordering = ('name',)
        index_together = (('id', 'slug'),)
    def __str__(self):
        return self.name

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in =ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category = category_id)
        else:
            return Product.get_all_products();

    class Meta:
        db_table="Products"

class Blogs(models.Model):
    blog_id=models.AutoField(auto_created=True,primary_key=True)
    blog_name=models.CharField(max_length=200)
    blog_details=models.CharField(max_length=200)
    blog_image=models.FileField(upload_to='blog_image')


    class Meta:
        db_table="blog"


class Comment(models.Model):
    c_id=models.AutoField(auto_created=True,primary_key=True)
    c_name=models.CharField(max_length=200)
    c_email=models.CharField(max_length=200)
    c_message=models.CharField(max_length=200)

    class Meta:
        db_table="comment"

class Review(models.Model):
    r_id=models.AutoField(auto_created=True,primary_key=True)
    r_name=models.CharField(max_length=200)
    r_email=models.CharField(max_length=200)
    r_message=models.CharField(max_length=200)

    class Meta:
        db_table="review"

class Customer(models.Model):
    id=models.AutoField(auto_created=True,primary_key=True)
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=500)

    def __str__(self):
        return self.first_name

    def register(self):
        self.save()

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False


    def isExists(self):
        if Customer.objects.filter(email = self.email):
            return True

        return  False
    
    def __str__(self):
        return self.first_name

class signupasseller(models.Model):
    id=models.AutoField(auto_created=True,primary_key=True)
    username=models.CharField(max_length=200)
    firstname=models.CharField(max_length=200)
    lastname=models.CharField(max_length=200)
    phone=models.CharField(max_length=200)
    address=models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=10)


    class Meta:
        db_table="Creator"

    def __str__(self):   
    		return self.username

class Order(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,
                                 on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    color = models.CharField(max_length=50, default='', blank=True, null=True)
    size = models.CharField(max_length=50, default='', blank=True, null=True)
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')

  


class editOrders(models.Model):
    productname = models.CharField(max_length=50, default='', null=True)
    customer = models.CharField(max_length=50, default='', null=True)
    price = models.IntegerField(null=True)
    color = models.CharField(max_length=50, default='', blank=True, null=True)
    size = models.CharField(max_length=50, default='', blank=True, null=True)
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)

    class Meta:
        db_table="orderform"

    def __str__(self):
        return self.productname


class adminaccount(models.Model):
    id=models.AutoField(auto_created=True,primary_key=True)
    username=models.CharField(max_length=200)
    firstname=models.CharField(max_length=200)
    lastname=models.CharField(max_length=200)
    phone=models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=10)



    class Meta:
        db_table="adminform"

    def __str__(self):
    		return self.username



# RATE_CHOICES = [
#     (1,'1 - very bad'),
#     (2,'2 - bad'),
#     (3,'3 - decent'),
#     (4,'4 - good'),
#     (5,'5 - perfect'),
# ]

# class review(models.model){
#     rate = models.PositiveSmallIntergerField()
# }

class contactform(models.Model):
    id=models.AutoField(auto_created=True,primary_key=True)
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    messgae = models.CharField(max_length=500)

    def __str__(self):
    	return self.username