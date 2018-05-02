from .models import *
from agent.models import *
from django.http import Http404, HttpResponseRedirect
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db import connection
from datetime import datetime

# Create your views here.

def home(request):
    return render(request, 'customer/customerhome.html', {'data': request.session['cusname']})


def autoauth(request):
    name = str(request.session["username"])
    passa = str(request.session["passa"])
    query = "SELECT * FROM customer_customer WHERE pass_word='" + passa + "' and cust_id=" + name
    cursor2 = connection.cursor()
    cursor2.execute(query)
    row2 = cursor2.fetchall()
    count = len(row2)
    if count==1 :
        return True
    else:
        return False

def logout(request):
    del request.session["username"]
    del request.session["passa"]
    return HttpResponseRedirect('/in')




def customerlogout(request):
        if autoauth(request):
            del request.session['username']
            del request.session['passa']
            del request.session['name']
            return HttpResponseRedirect('/in')
        else:
            return HttpResponseRedirect('/in')

def addnominee(request):
    if(autoauth(request)):
        return render(request, 'customer/addnominee.html', {'data': request.session['cusname']})
    else:
        return HttpResponseRedirect('/in')

def nomaddtodb(request):
    if(autoauth(request)):
        newcustomer = nominee()
        newcustomer.name = str(request.POST.get('name'))
        newcustomer.relationship = str(request.POST.get('rs'))
        newcustomer.DOB = str(request.POST.get('dob'))
        newcustomer.sex =str(request.POST.get('gender'))
        newcustomer.age=str(request.POST.get('age'))
        newcustomer.customer_id=customer.objects.only('cust_id').get(cust_id=request.session['username'])
        newcustomer.save()
        return render(request, 'customer/customerhome.html', {'data': request.session['cusname']})
    else:
        return HttpResponseRedirect('/in')

def changepassword(request):
    if autoauth(request):
        return render(request, 'customer/changepass.html', {'data': request.session['cusname']})
    else:
        return HttpResponseRedirect('/in')

def changepass(request):
    if(autoauth(request)):
        oldpassword=str(request.POST.get("oldpass"))
        newpassword=str(request.POST.get("newpass"))
        conpassword=str(request.POST.get("conpass"))
        if(oldpassword!=request.session['password']):
            return render(request, 'customer/changepass.html', {'data': request.session['cusname'], 'error':"Old password mismatch" })
        else:
            if newpassword==conpassword:
                query="UPDATE customer_customer SET pass_word='"+ conpassword +"' WHERE cust_id=" + str(request.session['username'])
                cursor2 = connection.cursor()
                cursor2.execute(query)
                request.session['passa']=conpassword
                return render(request, 'customer/changepass.html', {'data': request.session['cusname'], 'error':"Successfully changed your password"})
            else:
                return render(request, 'customer/changepass.html', {'data': request.session['cusname'], 'error':"New password mismatch"})
    else:
        return HttpResponseRedirect('/in')

def payment1(request):
    if autoauth(request):
        return render(request, 'customer/payment.html', {'data': request.session['cusname']})
    else:
        return HttpResponseRedirect('\in')

def pay(request):
    if autoauth(request):
        policynum = str(request.POST.get("polnum"))
        cardnum = str(request.POST.get("card"))
        amount = int(str(request.POST.get("amt")))
        query = "SELECT * FROM customer_policy_holder WHERE pol_no_id=" + str(policynum) + " and customer_id_id=" + str(request.session["username"])
        cursor2 = connection.cursor()
        cursor2.execute(query)
        row2 = cursor2.fetchall()
        count = len(row2)
        if(count==1 and amount!=0):
            query = "SELECT amt_pay,term FROM customer_policy_holder WHERE pol_no_id=" + str(policynum)+" and customer_id_id="+str(request.session["username"])+" "
            cursor2 = connection.cursor()
            cursor2.execute(query)
            row2 = cursor2.fetchall()
            count = len(row2)
            pay_amt=int(row2[0][0])
            pay_term=int(row2[0][1])
            if amount%pay_amt==0 and amount<=(pay_amt*pay_term):
                paid_terms=amount//pay_amt
                pa=payment()
                pa.payment_amount=amount
                myDate = datetime.now()
                pa.payment_date = myDate.strftime("%Y-%m-%d")
                pa.policyno=policy.objects.only('policy_num').get(policy_num=policynum)
                pa.save()
                paya=policy_payment()
                paya.policy_number=policy.objects.only('policy_num').get(policy_num=policynum)
                paya.payment_number=payment.objects.only('payment_num').get(payment_num=pa.payment_num)
                paya.save()
                query = "UPDATE customer_policy_holder SET term="+str(pay_term-paid_terms)+" WHERE pol_no_id=" + str(policynum) + " and customer_id_id=" + str(request.session["username"]) + " "
                cursor2 = connection.cursor()
                cursor2.execute(query)
                return render(request, 'customer/paying.html',  {'data': request.session['cusname'], 'error':"Paid for policy number "+str(policynum)+" remaining month are "+str(pay_term-paid_terms)})
            else:
                return render(request, 'customer/payment.html', {'data': request.session['cusname'], 'error':"Pay for one month"})
        else:
            return render(request, 'customer/payment.html', {'data': request.session['cusname'], 'error':"no policy Number found or you are paying zero rupees"})
    else:
        return HttpResponseRedirect('\in')