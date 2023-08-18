from django.db import models
import random
from django.core.validators import RegexValidator
from django.db.models.signals import pre_save, post_save
from django.shortcuts import reverse
from delivery.models import *
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework import serializers
import json
import requests
from django.conf import settings
from products .models import Product
from django.contrib.auth.models import User
from django.http import Http404
from requests.exceptions import HTTPError, ReadTimeout, ConnectionError, RequestException
from decimal import Decimal

def unique_slug_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


def order_total_receiver(sender, instance, *args, **kwargs):
    instance.total_price =  instance.order_total


def order_status_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.status:
        status_list = OrderStatus.objects.filter(name="New")
        if status_list:
            order_status = status_list.first()
            print('not created')
        else:
            order_status = OrderStatus.objects.create(name="New")
            print("created")
        instance.status =order_status


def order_staff_member_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.staff_member:
        staff_members = StaffMember.objects.all()
        if staff_members:
            last_staff_member = Order.objects.order_by('-id').first().staff_member if Order.objects.exists() else None
            if last_staff_member:
                next_staff_member = staff_members.filter(id__gt=last_staff_member.id).first()
                if not next_staff_member:
                    next_staff_member = staff_members.first()
            else:
                next_staff_member = staff_members.first()
            instance.staff_member =next_staff_member
            

            
def is_stopdesk_pre_save_receiver(sender, instance, *args, **kwargs):
    if instance.is_stopdesk and instance.center:
        instance.state = instance.center.wilaya
        instance.city = instance.center.commune


def create_parcel_receiver(sender, instance, *args, **kwargs):
    try:
        if instance.status.name != "Confirmed":
            return  # Do nothing if status is not confirmed

        api_setting = Setting.objects.first()
        url = api_setting.parcel_url
        api_id = api_setting.api_id
        api_token = api_setting.api_token

        headers = {'X-API-ID': api_id, 'X-API-TOKEN': api_token}

        order_data = OrderSerializer(instance).data
        yalidine_order = json.dumps(order_data, cls=DjangoJSONEncoder)
        yalidine_orders = {instance.pk: order_data}
        yalidine_orders_json = json.dumps(yalidine_orders, cls=DjangoJSONEncoder)

        if instance.tracking_id:
            get_response = requests.get(f"{url}{instance.tracking_id}", headers=headers)
            get_response.raise_for_status()
            get_response_data = json.loads(get_response.content)

            if get_response_data['total_data'] == 1:
                print("one occurrence update")
                patch_response = requests.patch(f"{url}{instance.tracking_id}", data=yalidine_order, headers=headers)
                patch_response.raise_for_status()
                instance.error = "No Error"
                instance.error_message = "Parcel was updated successfully on yalidine"

            elif get_response_data['total_data'] == 0:
                post_response = requests.post(url, data=yalidine_orders_json, headers=headers)
                post_response.raise_for_status()
                post_response_data = json.loads(post_response.content)
                if post_response_data[f"order{instance.pk}"]['success']:
                    instance.tracking_id = post_response_data[f"order{instance.pk}"]['tracking']
                    instance.error = "No Error"
                    instance.error_message = "Parcel was created on yalidine and tracking id was updated here"
                else:
                    instance.error = "Failed"
                    instance.error_message = "Parcel creation on yalidine failed"

        else:
            get_response = requests.get(f"{url}?order_id=order{instance.pk}", headers=headers)
            get_response.raise_for_status()
            get_response_data = json.loads(get_response.content)

            if get_response_data['total_data'] == 1:
                instance.tracking_id = get_response_data['data'][0]['tracking']
                instance.error = "One occurrence"
                instance.error_message = "One parcel of this order was found on yalidine, maybe you confirmed this order earlier and deleted its tracking id"
                print("one occurrence")
            elif get_response_data['total_data'] > 1:
                instance.tracking_id = get_response_data['data'][0]['tracking']
                instance.error = "Duplicated"
                instance.error_message = "Multiple parcels of this order were found on yalidine. Go to yalidine and delete duplicates"
                print("duplicate")
            elif get_response_data['total_data'] == 0:
                post_response = requests.post(url, data=yalidine_orders_json, headers=headers)
                post_response.raise_for_status()
                post_response_data = json.loads(post_response.content)
                if post_response_data[f"order{instance.pk}"]['success']:
                    instance.tracking_id = post_response_data[f"order{instance.pk}"]['tracking']
                    instance.error = "No Error"
                    instance.error_message = "Parcel was created successfully on yalidine"
                else:
                    instance.error = "Failed"
                    instance.error_message = "Parcel creation on yalidine failed"

    except (HTTPError, ReadTimeout, ConnectionError, RequestException) as err:
        print("Error:", err)
        instance.error = type(err).__name__
        instance.error_message = f"{type(err).__name__}-{err}"
    except KeyError:
        instance.error = "KeyError"
        instance.error_message = "Can't find order with this id on yalidine"
    except Setting.DoesNotExist:
        instance.error = "No delivery settings"
        instance.error_message = "Set up delivery settings first"
 
            
       







class SessionManager(models.Manager):
    def new_or_get(self, request):
        session_id = request.session.get("session_id", None)
        qs = self.get_queryset().filter(id=session_id)
        if qs.count() == 1:
            new_obj = False
            session_obj = qs.first()
            if request.user.is_authenticated and session_obj.user is None:
                session_obj.user = request.user
                session_obj.save()
        else:
            session_obj = Session.objects.new(user=request.user)
            new_obj = True
            request.session['session_id'] = session_obj.id
        return session_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)

class Session(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    objects = SessionManager()

    def __str__(self):
        return str(self.id)



class OrderStatus(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=20,null=True, blank=True)

    def __str__(self):
        return self.name

class StaffMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


PARCEL_ERROR_CHOICES = (
    ("No Error", "No Error"),
    ("No delivery settings", "No delivery settings"),
    ("HTTP Error", "HTTP Error"),
    ("Time out", "Time out"),
    ("Connection error", "Exception request"),
    ("Exception request", "Exception request"),
    ("KeyError", "KeyError"),
    ("One occurrence", "One occurrence"),
    ("Duplicated", "Duplicated"),
    ("Failed", "Failed"),
    
)

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE,null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    state = models.ForeignKey(Wilaya, on_delete=models.CASCADE)
    city = models.ForeignKey(Commune, on_delete=models.CASCADE)
    center = models.ForeignKey(Center, on_delete=models.CASCADE, null=True, blank=True)
    status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True, blank=True)
    staff_member = models.ForeignKey(StaffMember, on_delete=models.SET_NULL, null=True, blank=True)
    phone_regex = RegexValidator(
        regex=r'^0[567]\d{8}$',
        message="Phone number must be 10 digits long and start with 05, 06, or 07."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=10)
    created_on  = models. DateField(auto_now_add=True)
    created_on_time  = models. TimeField(auto_now_add=True,null=True,blank=True)
    last_modified =  models.DateTimeField(auto_now=True)
    first_name     = models.CharField(max_length=128,)
    last_name    = models.CharField(max_length=128)
    full_adress    = models.CharField(max_length=128)
    is_stopdesk    =models.BooleanField(default=False,null=True,blank=True)
    # yalidine 
    tracking_id     = models.CharField(max_length=128,null=True,blank=True)
    error = models.CharField(
        max_length = 20,
        choices = PARCEL_ERROR_CHOICES,
        null=True,blank=True
        )
    error_message =models.CharField(max_length = 128,null=True,blank=True)


    @property
    def order_id(self):
        return f"order{self.pk}"

    @property
    def firstname(self):
        return self.first_name
    
    @property
    def familyname(self):
        return self.last_name

    @property
    def contact_phone(self):
        return self.phone_number

    @property
    def from_wilaya_name(self):
        settings =Setting.objects.first()
        if settings:
            return settings.sending_from.name
        else:
            return "Alger"

    @property
    def address(self):
        return self.full_adress

    @property
    def to_commune_name(self):
        return self.city.name
    
    @property
    def to_wilaya_name(self):
        return self.state.name
    
    @property
    def product_list(self):
        return f"{self.quantity}-{self.product.slug}"

    @property
    def price(self):
        return self.total_price
    
    @property
    def freeshipping(self):
        return True
    
    @property
    def stopdesk_id(self):
        return self.center.center_id
    

    @property
    def has_exchange(self):
        return False
    
    @property
    def order_total(self):
        product_price = self.product.discounted_price
        state = self.state
        state_fee = None
        
        if Fee.objects.filter(wilaya=state).exists():
            fee = Fee.objects.get(wilaya=state)
            if self.is_stopdesk:
                state_fee = fee.desk_fee
            else:
                state_fee = fee.home_fee
        
        total_amount = (product_price * Decimal(self.quantity)) + (state_fee if state_fee is not None else Decimal('0'))
        return total_amount
    

    def __str__(self):
        return f"Order #{self.pk}"
    
    def staff_order_update_absolute_url(self):
        return reverse('staff_order_update',kwargs={'pk':self.pk})

    
        
pre_save.connect(order_status_pre_save_receiver, sender=Order)
pre_save.connect(order_staff_member_pre_save_receiver, sender=Order)
pre_save.connect(order_total_receiver, sender=Order)
pre_save.connect(is_stopdesk_pre_save_receiver, sender=Order)
pre_save.connect(create_parcel_receiver, sender=Order)

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'order_id',
            'firstname',
            'familyname',
            'contact_phone',
            'address',
            'from_wilaya_name',
            'to_commune_name',
            'to_wilaya_name',
            'product_list',
            'price',
            'freeshipping',
            'is_stopdesk',
            'has_exchange',
            'stopdesk_id',
        ]





