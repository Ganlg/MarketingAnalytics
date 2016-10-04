from django.db import models

# Create your models here.
class Service(models.Model):
    id = models.PositiveIntegerField(unique=True, primary_key=True, null=False, db_index=True)
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=250, null=True)

    def __str__(self):
        return "{}-{}".format(self.id, self.name)