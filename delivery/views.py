from django.shortcuts import render,redirect
from .models import *
import requests
import json
# Create your views here.

def update_wilayas(request):
    url ="https://api.yalidine.app/v1/wilayas/"
    try:
        api_setting = Setting.objects.first()
        api_id      = api_setting.api_id
        api_token   = api_setting.api_token
        
        get_wilayas_request = requests.get(url,headers = {'X-API-ID': api_id,'X-API-TOKEN':api_token})
        wilayas_dict = json.loads(get_wilayas_request.content) # convert the json response object to python dict
        print(get_wilayas_request)
        for wilaya in wilayas_dict['data'] :

         wilaya_id= wilaya['id']

         name = wilaya['name']
         if "'" in name:
            display_name = name.replace("'","")
         else:
            display_name = name

         zone = wilaya['zone']

         if wilaya['is_deliverable'] == 1:
            is_deliverable = True
         else :
            is_deliverable = False
        
        
         wilaya_obj, created = Wilaya.objects.get_or_create(wilaya_id=wilaya_id,name=name,display_name=display_name,zone=zone,is_deliverable=is_deliverable)

    except Exception as e:
        print(e)
    return redirect("/admin/delivery/wilaya/")



def update_communes(request):
   url ="https://api.yalidine.app/v1/communes/"
   has_more = True
   page_count = 1
   page_size = 100
   try:
      api_setting = Setting.objects.first()
      api_id      = api_setting.api_id
      api_token   = api_setting.api_token

      while(has_more):
         get_communes_request = requests.get(url,params={'PAGE': page_count,'PAGE_SIZE': page_size},headers = {'X-API-ID': api_id,'X-API-TOKEN':api_token})
         communes_dict = json.loads(get_communes_request.content) # convert the json response object to python dict

         for commune in communes_dict['data']:

            wilaya = Wilaya.objects.get(wilaya_id=commune['wilaya_id'])
            commune_id= commune['id']

            name = commune['name']
            if "'" in name:
               display_name = name.replace("'","")
   
            else:
               display_name = name

            delivery_time_parcel = commune['delivery_time_parcel']
            delivery_time_payment = commune['delivery_time_payment']

            if commune['is_deliverable'] == 1:
               is_deliverable = True
            else :
               is_deliverable = False

      
            if commune['has_stop_desk'] == 1:
               has_stop_desk = True
            else :
               has_stop_desk = False

            commune_obj, created = Commune.objects.get_or_create(commune_id=commune_id,name=name,display_name=display_name,wilaya=wilaya,is_deliverable=is_deliverable,has_stop_desk=has_stop_desk,delivery_time_parcel=delivery_time_parcel,delivery_time_payment=delivery_time_payment)
               
         
         
         has_more = communes_dict['has_more']
         page_count+=1

         

   except Exception as e:
      print(e)


   return redirect("/admin/delivery/commune/")




def update_centers(request):
   url ="https://api.yalidine.app/v1/centers/"
   has_more = True
   page_count = 1
   page_size = 100
   try:
      api_setting = Setting.objects.first()
      api_id      = api_setting.api_id
      api_token   = api_setting.api_token

      while(has_more):
         get_center_request = requests.get(url,params={'PAGE': page_count,'PAGE_SIZE': page_size},headers = {'X-API-ID': api_id,'X-API-TOKEN':api_token})
         centers_dict = json.loads(get_center_request.content) # convert the json response object to python dict

         for center in centers_dict['data']:

            wilaya = Wilaya.objects.get(wilaya_id=center['wilaya_id'])
            commune = Commune.objects.get(commune_id=center['commune_id'])
            center_id= center['center_id']
            address= center['address']

            name = center['name']
            if "'" in center:
               display_name = name.replace("'","")
   
            else:
               display_name = name

           

            center_obj, created = Center.objects.get_or_create(center_id=center_id,name=name,display_name=display_name,wilaya=wilaya,commune=commune,address=address)
               
         
         
         has_more = center_dict['has_more']
         page_count+=1

         

   except Exception as e:
      print(e)


   return redirect("/admin/delivery/center/")




def update_wilayas_fee(request):
   
   url ="https://api.yalidine.app/v1/deliveryfees/"
   try:
      api_setting = Setting.objects.first()
      api_id      = api_setting.api_id
      api_token   = api_setting.api_token
      
      get_wilayas_fee_request = requests.get(url,headers = {'X-API-ID': api_id,'X-API-TOKEN':api_token})
      wilayas_fee_dict = json.loads(get_wilayas_fee_request.content) # convert the json response object to python dict
   
      for wilaya_fee in wilayas_fee_dict['data'] :

         wilaya = Wilaya.objects.get(wilaya_id=wilaya_fee['wilaya_id'])
         home_fee = wilaya_fee['home_fee']
         desk_fee = wilaya_fee['desk_fee']

         wilaya_fee_obj, created = Fee.objects.get_or_create(wilaya=wilaya, home_fee=home_fee,desk_fee=desk_fee)

   except Exception as e:
      print(e)
   return redirect("/admin/delivery/fee/")