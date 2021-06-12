from django.db import models

class User(model.Model):
    name = models.CharField(max_length=200)

class Group(model.Model):
    name = models.CharField(max_length=200)

class Event(model.Model):
    Fixed = 'fixed'
    Percent = 'percent'
    Equal = 'Equal'
    Types = [
        (Fixed, Fixed),
        (Percent, Percent),
        (Equal, Equal)
    ]
    
    name = models.CharField(max_length=200)
    type = models.CharField(
        max_length=50,
        choices=Types,
        default=Equal,
    )
    group = models.ForeignKey('Group', on_delete=models.CASCADE)

class Contributions(model.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    # To do - add validartion: 1 : 100
    percent = models.IntegerField()
    fixed = models.IntegerField()
    amount = models.IntegerField(defaul=0)

class Ledger(model.Model):
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    lender = models.ForeignKey('User', on_delete=models.CASCADE)
    borrower = models.ForeignKey('User', on_delete=models.CASCADE)
    amount = models.IntegerField(defaul=0)

    