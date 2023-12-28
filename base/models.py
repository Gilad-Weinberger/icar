from django.db import models

class Car(models.Model):
    image = models.ImageField(upload_to='car_images/')
    license_number = models.CharField(max_length=8, blank=True)
    recognition_result = models.JSONField(blank=True, null=True)
