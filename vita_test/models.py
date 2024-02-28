from django.db import models


# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=1024, unique=True)
    description = models.TextField(blank=True)
    pet_project_ideas = models.TextField(blank=True)
    useful_links = models.TextField(blank=True)
    useful_books = models.TextField(blank=True)
    useful_courses = models.TextField(blank=True)


class Skill(models.Model):
    name = models.CharField(max_length=1024, unique=True)
    description = models.TextField(blank=True)
    topics = models.ManyToManyField(Topic, blank=True)


class Profession(models.Model):
    name = models.CharField(max_length=1024, unique=True)
    description = models.TextField(blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
