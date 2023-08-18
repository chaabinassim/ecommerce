import requests
from requests.exceptions import HTTPError, ReadTimeout, ConnectionError, RequestException
from django.core.serializers.json import DjangoJSONEncoder
import json

def create_parcel_receiver(sender, instance, *args, **kwargs):
    try:
        if instance.status.name != "Confirmed":
            return  # Do nothing if status is not confirmed

        api_setting = Setting.objects.get(id=1)
        url = api_setting.parcel_url
        api_id = api_setting.api_id
        api_token = api_setting.api_token

        headers = {'X-API-ID': api_id, 'X-API-TOKEN': api_token}

        order_data = OrderSerializer(instance).data
        yalidine_orders = {instance.pk: order_data}
        yalidine_orders_json = json.dumps(yalidine_orders, cls=DjangoJSONEncoder)

        if instance.tracking_id:
            get_response = requests.get(f"{url}{instance.tracking_id}", headers=headers)
            get_response.raise_for_status()
            get_response_data = json.loads(get_response.content)

            if get_response_data['total_data'] == 1:
                print("one occurrence update")
                patch_response = requests.patch(f"{url}{instance.tracking_id}", data=yalidine_orders_json, headers=headers)
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
