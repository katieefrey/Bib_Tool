from django.db import models
from bibmanage.models import Batch, Bibgroup
from users.models import CustomUser

# Create your models here.

class Status(models.Model):
    status = models.CharField(max_length=50)
    # yes, no, maybe, doubtful

    def __str__(self):
        return f"{self.status}"


class Affil(models.Model):
    name = models.CharField(max_length=50)
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    # HCO, SAO, both, unknown, neither, either

    def __str__(self):
        return f"{self.name}"


class Guess(models.Model):
    guess = models.CharField(max_length=50)
    # likely, review, reivew-visiting, review-nonSAO, review-nonCfA, doubtful

    def __str__(self):
        return f"{self.guess}"


class Article(models.Model):
    bibcode = models.CharField(max_length=19, unique=True)
    title = models.CharField(max_length=250, null=True, blank=True)
    adminbibgroup = models.ForeignKey(Bibgroup, on_delete=models.CASCADE)
    #bibgroupcheck = models.ForeignKey(Bibgroup, on_delete=models.CASCADE)
    guess = models.ForeignKey(Guess, on_delete=models.CASCADE)
    query = models.CharField(max_length=100, null=True, blank=True)
    affils = models.TextField(null=True, blank=True)
    authnum = models.IntegerField(null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    inst = models.ForeignKey(Affil, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.bibcode} {self.status} {self.inst}"


class Work(models.Model):
    username = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    bibcode = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} {self.bibcode}"