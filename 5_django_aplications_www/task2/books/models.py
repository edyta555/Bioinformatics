from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=100)
   
    def __str__(self):
        return self.category_name
    
class Book(models.Model):
    title = models.CharField(max_length=300)
    authors = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    was_read = models.BooleanField(default=False)
    comments = models.CharField(max_length=500)
    version = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title