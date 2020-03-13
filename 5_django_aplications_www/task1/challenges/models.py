from django.db import models
import datetime
# Create your models here.

class Challenge(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=40)
    counter = models.IntegerField(default=0)
    version = models.IntegerField(default=1)
    days = models.IntegerField(default=0)
    begin = models.DateField(default=datetime.date.today())

    def __str__(self):
        return self.name

    def fraction(self):
        return str((self.counter*100)//self.days) + "%"

    def beginStr(self):
        return str(self.begin.strftime('%Y-%m-%d'))


