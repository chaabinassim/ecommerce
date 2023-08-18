from django.shortcuts import render,redirect,get_object_or_404
from .models import *
import requests
import json
from django.db import transaction
# Create your views here.

def update_wilayas(request):
    url = "https://api.yalidine.app/v1/wilayas/"
    
    try:
        api_setting = Setting.objects.first()
        api_id = api_setting.api_id
        api_token = api_setting.api_token
        
        headers = {'X-API-ID': api_id, 'X-API-TOKEN': api_token}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses
        
        response_data = response.json()
        
        with transaction.atomic():
            for wilaya_data in response_data.get('data', []):
                wilaya_id = wilaya_data['id']
                name = wilaya_data['name']
                display_name = name.replace("'", "") if "'" in name else name
                zone = wilaya_data['zone']
                is_deliverable = wilaya_data['is_deliverable'] == 1
                
                Wilaya.objects.update_or_create(
                    wilaya_id=wilaya_id,
                    defaults={'name': name, 'display_name': display_name, 'zone': zone, 'is_deliverable': is_deliverable}
                )

    except requests.exceptions.RequestException as request_error:
        # Handle requests-related exceptions, like connection errors
        print("A request error occurred:", request_error)

    except Exception as other_error:
        # Handle other general exceptions
        print("An error occurred:", other_error)

    return redirect("/admin/delivery/wilaya/")


def update_communes(request):
    url = "https://api.yalidine.app/v1/communes/"
    page_size = 100
    
    try:
        api_setting = Setting.objects.first()
        api_id = api_setting.api_id
        api_token = api_setting.api_token

        page_count = 1
        has_more = True

        while has_more:
            get_communes_request = requests.get(url, params={'PAGE': page_count, 'PAGE_SIZE': page_size},
                                                headers={'X-API-ID': api_id, 'X-API-TOKEN': api_token})
            get_communes_request.raise_for_status()
            communes_dict = get_communes_request.json()

            with transaction.atomic():
                for commune in communes_dict['data']:
                    wilaya_id = commune['wilaya_id']
                    wilaya = Wilaya.objects.get(wilaya_id=wilaya_id)
                    commune_id = commune['id']

                    name = commune['name']
                    display_name = name.replace("'", "") if "'" in name else name

                    delivery_time_parcel = commune['delivery_time_parcel']
                    delivery_time_payment = commune['delivery_time_payment']

                    is_deliverable = commune['is_deliverable'] == 1
                    has_stop_desk = commune['has_stop_desk'] == 1

                    Commune.objects.update_or_create(
                        commune_id=commune_id,
                        defaults={'name': name, 'display_name': display_name, 'wilaya': wilaya,
                                  'is_deliverable': is_deliverable, 'has_stop_desk': has_stop_desk,
                                  'delivery_time_parcel': delivery_time_parcel,
                                  'delivery_time_payment': delivery_time_payment}
                    )

            has_more = communes_dict['has_more']
            page_count += 1

    except requests.exceptions.RequestException as request_error:
        # Handle requests-related exceptions, like connection errors
        print("A request error occurred: %s", request_error)

    except Exception as other_error:
        # Handle other general exceptions
        print("An error occurred: %s", other_error)

    return redirect("/admin/delivery/commune/")


def update_centers(request):
    url = "https://api.yalidine.app/v1/centers/"
    page_size = 100

    try:
        api_setting = Setting.objects.first()
        api_id = api_setting.api_id
        api_token = api_setting.api_token

        page_count = 1
        has_more = True

        while has_more:
            get_centers_request = requests.get(url, params={'PAGE': page_count, 'PAGE_SIZE': page_size},
                                               headers={'X-API-ID': api_id, 'X-API-TOKEN': api_token})
            get_centers_request.raise_for_status()
            centers_dict = get_centers_request.json()

            with transaction.atomic():
                for center_data in centers_dict.get('data', []):
                    wilaya_id = center_data['wilaya_id']
                    commune_id = center_data['commune_id']
                    wilaya = get_object_or_404(Wilaya, wilaya_id=center_data['wilaya_id'])
                    commune = get_object_or_404(Commune, commune_id=center_data['commune_id'])
                    center_id = center_data['center_id']
                    address = center_data['address']

                    name = center_data['name']
                    display_name = name.replace("'", "") if "'" in name else name

                    Center.objects.update_or_create(
                        center_id=center_id,
                        defaults={'name': name, 'display_name': display_name, 'wilaya': wilaya,
                                  'commune': commune, 'address': address}
                    )

            has_more = centers_dict.get('has_more', False)
            page_count += 1

    except requests.exceptions.RequestException as request_error:
        # Handle requests-related exceptions, like connection errors
        print("A request error occurred: %s", request_error)

    except Exception as other_error:
        # Handle other general exceptions
        print("An error occurred: %s", other_error)

    return redirect("/admin/delivery/center/")


def update_wilayas_fee(request):
    url = "https://api.yalidine.app/v1/deliveryfees/"
    
    try:
        api_setting = Setting.objects.first()
        api_id = api_setting.api_id
        api_token = api_setting.api_token
        
        headers = {'X-API-ID': api_id, 'X-API-TOKEN': api_token}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        wilayas_fee_dict = response.json()
        
        with transaction.atomic():
            for wilaya_fee_data in wilayas_fee_dict.get('data', []):
                wilaya_id = wilaya_fee_data['wilaya_id']
                wilaya = Wilaya.objects.get(wilaya_id=wilaya_id)

                home_fee = wilaya_fee_data['home_fee']
                desk_fee = wilaya_fee_data['desk_fee']

                Fee.objects.update_or_create(
                    wilaya=wilaya,
                    defaults={'home_fee': home_fee, 'desk_fee': desk_fee}
                )

    except requests.exceptions.RequestException as request_error:
        # Handle requests-related exceptions, like connection errors
        print("A request error occurred: %s", request_error)

    except Exception as other_error:
        # Handle other general exceptions
        print("An error occurred: %s", other_error)

    return redirect("/admin/delivery/fee/")

