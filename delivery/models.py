from django.db import models

# Create your models here.




class Wilaya(models.Model):

    wilaya_id      = models.IntegerField()
    name           = models.CharField(max_length=122)
    display_name   = models.CharField(max_length=122,null=True,blank=True)
    zone           = models.IntegerField()
    is_deliverable = models.BooleanField()

    def __str__(self):
        return self.name



class Commune(models.Model):
    commune_id = models.IntegerField()
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE)
    name = models.CharField(max_length=122)
    display_name   = models.CharField(max_length=122,null=True,blank=True)
    is_deliverable = models.BooleanField()
    has_stop_desk = models.BooleanField()
    delivery_time_parcel = models.IntegerField()
    delivery_time_payment = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.name


class Center(models.Model):
    center_id = models.IntegerField()
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE)
    name = models.CharField(max_length=122)
    display_name   = models.CharField(max_length=122,null=True,blank=True)
    address = models.CharField(max_length=122,null=True,blank=True)
    

    def __str__(self):
        return self.name

class Fee(models.Model):
    
    wilaya   = models.ForeignKey(Wilaya, on_delete=models.CASCADE)
    home_fee = models.PositiveIntegerField()
    desk_fee = models.PositiveIntegerField()
    

    def __str__(self):
        return f"{self.wilaya}-{self.home_fee}"

    
class Setting(models.Model):
    api_id    = models.CharField(max_length=128)
    api_token = models.CharField(max_length=128)
    sending_from =  models.ForeignKey(Wilaya, on_delete=models.CASCADE,null=True,blank=True)
    parcel_url = models.CharField(max_length=128,blank=True,null=True)
    wilaya_url = models.CharField(max_length=128,blank=True,null=True)
    communes_url = models.CharField(max_length=128,blank=True,null=True)

    def __str__(self):
        return self.api_id