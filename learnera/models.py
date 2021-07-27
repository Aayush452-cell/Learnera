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

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    payment_status=models.IntegerField(default=2)
    items_json = models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=90)
    phone = models.CharField(max_length=111, default="")
    email = models.CharField(max_length=111)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=50)

class contribution(models.Model):
    contribution_id = models.AutoField(primary_key=True)
    social_id = models.CharField(max_length=500)
    email = models.CharField(max_length=200)
    content_url = models.URLField(max_length=200)
    course_name = models.CharField(max_length=2000)
    cost = models.CharField(max_length=500)
    short_desc = models.CharField(max_length=2000)
    full_desc = models.CharField(max_length=5000)
    def __str__(self):
        return self.email

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")


    def __str__(self):
        return self.name