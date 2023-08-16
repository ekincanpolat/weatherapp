from django.db import models


class City(models.Model):
    city = models.TextField(max_length=50)

    def __str__(self):
        return self.city


class Weather(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    date = models.DateField()
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    temperature = models.IntegerField()

    def __str__(self):
        return f"{self.city.city} - {self.date}"
