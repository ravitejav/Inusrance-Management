from django.db import models
from agent.models import agent
# Create your models here.
class customer(models.Model):
    Fname = models.CharField(max_length=80)
    Lname = models.CharField(max_length=80)
    address = models.CharField(max_length=100)
    phone_no = models.IntegerField()
    age = models.IntegerField()
    sex = models.CharField(max_length=1)
    DOB = models.DateField()
    cust_id = models.AutoField(primary_key=True)
    Cagent_id = models.ForeignKey(agent, on_delete=models.CASCADE)
    pass_word = models.CharField(max_length=50)
    email = models.CharField(max_length=100)

    def __str__(self):
        return str(self.cust_id)

class policy_type(models.Model):
    policy_name = models.CharField(max_length=40)
    policy_code = models.IntegerField(primary_key=True)

    def __str__(self):
        return str(self.policy_code)

class policy(models.Model):
    policy_num = models.AutoField(primary_key=True)
    policycode = models.ForeignKey(policy_type, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.policy_num)

class payment(models.Model):
    payment_date = models.DateField()
    payment_amount = models.IntegerField()
    payment_num = models.AutoField(primary_key=True)
    policyno = models.ForeignKey(policy, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.payment_num)

class nominee(models.Model):
    name = models.CharField(max_length=70)
    relationship = models.CharField(max_length=50)
    DOB = models.DateField()
    sex = models.CharField(max_length=1)
    customer_id =  models.ForeignKey(customer, on_delete=models.CASCADE)
    age=models.IntegerField()

class policy_payment(models.Model):
    policy_number = models.ForeignKey(policy, on_delete=models.CASCADE)
    payment_number =  models.ForeignKey(payment, on_delete=models.CASCADE)

class policy_holder(models.Model):
    customer_id =  models.ForeignKey(customer, on_delete=models.CASCADE)
    pol_no =  models.ForeignKey(policy, on_delete=models.CASCADE)
    term=models.IntegerField()
    amt_pay=models.IntegerField()




