from django.db import models

# Create your models here.
class Results(models.Model):
    author=models.CharField(max_length=1200)
    subreddit=models.CharField(max_length=1200)
    comment=models.CharField(max_length=4800)
    subjectivity=models.CharField(max_length=32)
    polarity=models.CharField(max_length=32)
    querydate=models.CharField(max_length=64)
    queryuser=models.CharField(max_length=16)
    sentiment=models.CharField(max_length=32)
    
    def __str__(self):
       return self.subreddit
