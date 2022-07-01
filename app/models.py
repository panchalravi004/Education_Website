from ast import mod
from distutils.command.upload import upload
from email.policy import default
from django.db import models
from django.forms import CharField
from autoslug import AutoSlugField
from matplotlib.image import thumbnail
from matplotlib.pyplot import title

# Create your models here.
class Categories(models.Model):
    icon = models.CharField(max_length=200,null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def get_all_category(self):
        return Categories.objects.all().order_by('-id')

class Author(models.Model):
    author_profile = models.ImageField(upload_to='author')
    name = models.CharField(max_length=100,null=True)
    about_author = models.TextField()

    def __str__(self):
        return self.name

class Levels(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Language(models.Model):

    language = models.CharField(max_length=100)
    def __str__(self):
        return self.language

class Course(models.Model):

    STATUS = (
        ('PUBLISH','PUBLISH'),
        ('DRAFT','DRAFT'),
    )

    featured_image = models.ImageField(upload_to='featured_img',null=True)
    featured_video = models.CharField(max_length=300,null=True)
    title = models.CharField(max_length=500)
    created_at = models.DateField(auto_now_add=True)
    author = models.ForeignKey(Author,on_delete=models.CASCADE,null=True)
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    level = models.ForeignKey(Levels,on_delete=models.CASCADE,null=True)
    language = models.ForeignKey(Language,on_delete=models.CASCADE,null=True)
    Deadline = models.CharField(max_length=200,null=True)
    description = models.TextField()
    price = models.IntegerField(null=True,default=0)
    discount = models.IntegerField(null=True)
    slug = AutoSlugField(populate_from='title',unique=True,null=True,default=None)
    status = models.CharField(choices=STATUS,max_length=100,null=True)
    certificate = models.BooleanField(null=True,default=False)

    def __str__(self):
        return self.title

class What_you_learn(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    points = models.CharField(max_length=200)

    def __str__(self):
        return self.points

class Requirements(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    points = models.CharField(max_length=350)

    def __str__(self):
        return self.points

class Lesson(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name + " - " + self.course.title

class Video(models.Model):
    serial_number = models.IntegerField(null=True)
    thumbnail = models.ImageField(upload_to='yt_thumbnail',null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    youtube_id = models.CharField(max_length=200)
    time_duration = models.FloatField(null=True)
    preview = models.BooleanField(default=False)

    def __str__(self):
            return self.title
