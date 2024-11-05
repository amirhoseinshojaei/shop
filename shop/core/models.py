from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.core.validators import RegexValidator
import uuid
from django.contrib.auth.hashers import make_password
import datetime
from django.utils import timezone
from django.db.models.signals import post_save
from slugify import slugify
# Create your models here.


# Status choices
STATUS_CHOICES = [
    ('in_stock','InStock'),
    ('out_of_stock', 'Out Of Stock'),
]


class MyAccountManager(BaseUserManager):
    def create_user(self, email, phone_number , password=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        # if not username:
        #     raise ValueError('Users must have an username')

        if not phone_number:
            raise ValueError('Users must have a phone number')

        user = self.model(
            email=self.normalize_email(email),
            # username=username,
            phone_number=phone_number
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password):
        user = self.create_user(
            email=self.normalize_email(email),
            # username=username,
            password=password,
            phone_number=phone_number
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser,PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    # username = models.CharField(max_length=250,unique=True)
    email = models.EmailField(unique=True)
    regex_phone = RegexValidator(
        regex=r'^09\d{9}$',
        message='number should be in correct format starting with 09'
    )
    phone_number = models.CharField(max_length=11, unique=True, validators=[regex_phone])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']
    objects = MyAccountManager()


    class Meta:
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.phone_number
    

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    

# Profilr Users
class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField(max_length=15000)
    postal_code = models.BigIntegerField()
    city = models.CharField(max_length=200)
    old_cart = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.user.phone_number
    

# Create a user profile by default when user signsup
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

# Automate profile things
post_save.connect(Profile, sender= User)




# Category for Products
class Categories(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Categories, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    

# Suppliers info
class Suppliers(models.Model):
    user = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'



# All of Products
class Products(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    category = models.ForeignKey(Categories, on_delete= models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=250, choices=STATUS_CHOICES, default='in_stock')
    is_suggestion = models.BooleanField(default=False , null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Products, self).save(*args, **kwargs)

    
    def calculate_discount_percentage(self):
        if self.is_sale and self.sale_price < self.price:
            discount = (self.price - self.sale_price) / self.price * 100
            return round(discount, 0)
        

    def __str__(self):
        return self.name

    











