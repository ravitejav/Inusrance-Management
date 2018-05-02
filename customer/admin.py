from django.contrib import admin
from.models import customer, policy, policy_type, payment, nominee, policy_payment, policy_holder
# Register your models here.
admin.site.register(customer)
admin.site.register(policy)
admin.site.register(policy_type)
admin.site.register(payment)
admin.site.register(nominee)
admin.site.register(policy_payment)
admin.site.register(policy_holder)