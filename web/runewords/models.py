from django.db import models


class Rune(models.Model):
    num = models.IntegerField()
    name = models.CharField(max_length=10)
    effect = models.TextField()


class RuneWord(models.Model):
    name = models.CharField(max_length=255)
    effect = models.TextField()
    weapons = models.CharField(max_length=255, db_index=True)
    char_level = models.IntegerField()
    runes = models.ManyToManyField(Rune, db_index=True)
