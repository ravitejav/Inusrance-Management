from .models import agent, office
from customer.models import *
from django.http import Http404, HttpResponseRedirect
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db import connection
from datetime import datetime

app_name = 'agent'

#admin functions here

def home(request):
    return render(request, 'agent/home.html', {'data':"ravi"})

def loginstaff(request):
    name = str(request.POST.get("username"))
    passa = str(request.POST.get("passa"))
    query = "SELECT * FROM agent_agent WHERE pass_word='" + passa + "' and agentid=" + name
    cursor2 = connection.cursor()
    cursor2.execute(query)
    row2 = cursor2.fetchall()
    count = len(row2)
    if count==1 :
        request.session['agentname']=name;
        request.session['password'] =passa;
        request.session['name']=row2[0][1]
        return render(request, 'agent/agenthome.html', {'data':row2[0][1]})
    else:
        return HttpResponseRedirect('/in/')

def loginuser(request):
    name = str(request.POST.get("username"))
    passa = str(request.POST.get("passa"))
    query = "SELECT * FROM customer_customer WHERE pass_word='" + passa + "' and cust_id=" + name
    cursor2 = connection.cursor()
    cursor2.execute(query)
    row2 = cursor2.fetchall()
    count = len(row2)
    if count==1 :
        request.session["username"]=name;
        request.session["passa"] = passa;
        request.session['cusname']=row2[0][0]+row2[0][1];
        return HttpResponseRedirect('/cust/')
    else:
        return HttpResponseRedirect('/in/')

def autoauth(request):
    name = request.session['agentname']
    passa = request.session['password']
    query = "SELECT * FROM agent_agent WHERE pass_word='" + passa + "' and agentid=" + name
    cursor2 = connection.cursor()
    cursor2.execute(query)
    row2 = cursor2.fetchall()
    count = len(row2)
    if count==1:
        return True;
    else:
        return False

def stafflogout(request):
    if autoauth(request):
        del request.session['agentname']
        del request.session['password']
        del request.session['name']
        return HttpResponseRedirect('/in')
    else:
        return HttpResponseRedirect('/in')

def changepass(request):
    if(autoauth(request)):
        oldpassword=str(request.POST.get("oldpass"))
        newpassword=str(request.POST.get("newpass"))
        conpassword=str(request.POST.get("conpass"))
        if(oldpassword!=request.session['password']):
            return render(request, 'agent/changepass.html', {'data': request.session['name'], 'error':"Old password mismatch" })
        else:
            if newpassword==conpassword:
                query="UPDATE agent_agent SET pass_word='"+ conpassword +"' WHERE agentid=" + str(request.session['agentname'])
                cursor2 = connection.cursor()
                cursor2.execute(query)
                request.session['password']=conpassword
                return render(request, 'agent/changepass.html', {'data': request.session['name'], 'error':"Successfully changed your password"})
            else:
                return render(request, 'agent/changepass.html', {'data': request.session['name'], 'error':"New password mismatch"})
    else:
        return HttpResponseRedirect('/in')

def addcus(request):
    if(autoauth(request)):
        return render(request, 'agent/addcus.html', {'data': request.session['name']})
    else:
        return HttpResponseRedirect('/in')

def changepassword(request):
    if autoauth(request):
        return render(request, 'agent/changepass.html', {'data': request.session['name']})
    else:
        return HttpResponseRedirect('/in')

def addtodb(request):
    if autoauth(request):
        newagent = customer()
        newagent.Fname=str(request.POST.get('first_name'))
        newagent.Lname=str(request.POST.get('second_name'))
        newagent.phone_no=str(request.POST.get('phone'))
        newagent.email=str(request.POST.get('email'))
        newagent.pass_word=str(request.POST.get('passa'))
        newagent.age=str(request.POST.get('age'))
        newagent.DOB=str(request.POST.get('dob'))
        newagent.address=str(request.POST.get('per_add'))
        newagent.sex=str(request.POST.get('gender'))
        newagent.Cagent_id= agent.objects.only('agentid').get(agentid=request.session['agentname'])
        newagent.save()
        return render(request, 'agent/agenthome.html', {'data': request.session['name'], 'error':newagent.cust_id})
    else:
        return HttpResponseRedirect('/in')

def transaction(request):
    if autoauth(request):
        return render(request, 'agent/tran.html', {'data': request.session['name']})
    else:
        return HttpResponseRedirect('/in')

def viewtrans(request):
    if autoauth(request):
        name=str(request.POST.get('custid'))
        query="SELECT DISTINCT cp.policyno_id,cp.payment_num,cp.payment_amount,cp.payment_date,pt.policy_name FROM customer_payment cp,customer_customer c,customer_policy cpo,customer_policy_holder ch,customer_policy_type pt WHERE "
        query=query+"ch.customer_id_id =" + str(name) + " and ch.pol_no_id=cp.policyno_id and cpo.policy_num=cp.policyno_id and pt.policy_code=cpo.policycode_id"
        cursor2 = connection.cursor()
        cursor2.execute(query)
        row2=cursor2.fetchall()
        return render(request, 'agent/view.html', {'data': request.session['name'], 'logdata': row2})
    else:
        return HttpResponseRedirect('/in')

def update(request):
    if autoauth(request):
        return render(request, 'agent/update.html', {'data': request.session['name']})
    else:
        return HttpResponseRedirect('/in')


def updatedone(request):
    if autoauth(request):
        query="SELECT * FROM customer_customer WHERE cust_id=" + str(request.POST.get('id'))
        cursor2 = connection.cursor()
        cursor2.execute(query)
        row2 = cursor2.fetchall()
        return render(request, 'agent/updatepage.html', {'data':request.session['name'], 'logdata':row2})
    else:
        return HttpResponseRedirect('/in')

def updatedonetodb(request):
    if autoauth(request):
        newagent = customer.objects.get(cust_id=int(request.POST.get('cusid')))
        newagent.phone_no=str(request.POST.get('phone'))
        newagent.email=str(request.POST.get('email'))
        newagent.age=str(request.POST.get('age'))
        newagent.DOB=str(request.POST.get('dob'))
        newagent.address=str(request.POST.get('per_add'))
        newagent.sex=str(request.POST.get('gender'))
        newagent.save()
        return render(request, 'agent/agenthome.html', {'data': request.session['name'], 'error':newagent.cust_id})
    else:
        return HttpResponseRedirect('/in')

def addpolicy(request):
    if autoauth(request):
        query = "SELECT * FROM customer_policy_type WHERE 1"
        cursor2 = connection.cursor()
        cursor2.execute(query)
        row2 = cursor2.fetchall()
        return render(request, 'agent/addpolicy.html', {'data': request.session['name'],'d':row2})
    else:
        return HttpResponseRedirect('/in')

def addpoltocus(request):
    if autoauth(request):
        print("working mate")
        query = "SELECT count(*) FROM customer_policy_type WHERE 1"
        cursor2 = connection.cursor()
        cursor2.execute(query)
        ad=cursor2.fetchall()
        total=ad[0][0]
        query = "SELECT * FROM customer_policy_type WHERE 1"
        cursor2 = connection.cursor()
        cursor2.execute(query)
        row=cursor2.fetchall()
        i=0
        st=""
        cusid=str(request.POST.get('cusid'))
        while total>i:
            print('working again', i)
            e=str(row[i][1])
            if str(request.POST.get(e))=='1':
                z=str(row[i][1])+"amt"
                amt=str(request.POST.get(z))
                z = str(row[i][1])+"span"
                span=str(request.POST.get(z))
                pol=policy()
                pol.policycode=policy_type.objects.get(policy_code=int(e))
                pol.save()
                ph=policy_holder()
                ph.pol_no=policy.objects.get(policy_num=int(pol.policy_num))
                ph.term=int(span)
                ph.amt_pay=int(amt)
                ph.customer_id=customer.objects.get(cust_id=int(cusid))
                ph.save()
                st=st+"For your policy "+str(row[i][0])+", given policy number is " +str(ph.pol_no)+" "
                i = i + 1
            else:
                i = i + 1
        return render(request, 'agent/agenthome.html', {'data': request.session['name'], 'error':st})
    else:
       return HttpResponseRedirect('\in')