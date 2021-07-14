from django.db import models

# Create your models here.

class allcourse(models.Model):
    id = models.AutoField
    course_name = models.CharField(max_length=120)
    category = models.CharField(max_length=50,default="")
    subcategory = models.CharField(max_length=50,default="")
    fee = models.IntegerField(default=0)
    sort_desc = models.CharField(max_length=5000)
    desc = models.CharField(max_length=50000)
    pub_date = models.DateField()
    image = models.ImageField(upload_to='learnera/images',default="")
    video_link = models.URLField(max_length=200)

    def __str__(self):
        return self.course_name


class profile(models.Model):
    id = models.AutoField
    name = models.CharField(max_length=120)
    email = models.CharField(max_length=120)
    picture_url = models.URLField(max_length=120)
    u_id = models.CharField(max_length=120)

    def __str__(self):
        return self.email
