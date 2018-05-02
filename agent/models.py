from django.db import models

# Create your models here.

class office(models.Model):
    office_name = models.CharField(max_length=50, primary_key=True)
    adress = models.CharField(max_length=120)
    phone_no = models.IntegerField()
    manager_name = models.CharField(max_length=40)

    def __str__(self):
        return str(self.office_name)


class agent(models.Model):
    fname = models.CharField(max_length=80)
    lname = models.CharField(max_length=60)
    address=models.CharField(max_length=120)
    phone_no = models.CharField(max_length=20)
    sex = models.CharField(max_length=1)
    age = models.IntegerField()
    dob = models.DateField()
    pass_word = models.CharField(max_length=50)
    agentid = models.AutoField(primary_key=True)
    agent_office_name = models.ForeignKey(office, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.agentid)
