from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    part_no = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
class Part(models.Model):
    part_no = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.part_no

class Component(models.Model):
    part = models.ForeignKey(Part, related_name='components', on_delete=models.CASCADE)
    component_no = models.CharField(max_length=100)
    quantity = models.IntegerField()

    def __str__(self):
        return self.component_no

class PartComponent(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    part_serial_number = models.CharField(max_length=100)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    component_serial_number = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.part.part_no} - {self.component.component_no} - {self.component_serial_number}"