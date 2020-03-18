from django.db import models


class Rental(models.Model):
    ab_id = models.IntegerField(unique=True)
    name = models.TextField()
    host_id = models.IntegerField()
    host_name = models.CharField(max_length=500)
    neighbourhood_group = models.CharField(max_length=500)
    neighbourhood = models.CharField(max_length=500)
    latitude = models.FloatField()
    longitude = models.FloatField()
    room_type = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    minimum_nights = models.CharField(max_length=200)
    number_of_reviews = models.CharField(max_length=200)
    last_review = models.CharField(max_length=200)
    reviews_per_month = models.CharField(max_length=200)
    calculated_host_listings_count = models.CharField(max_length=200)
    availability_365 = models.CharField(max_length=200)
    bedroom_count = models.IntegerField(null=True)
