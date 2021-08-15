from django.http import HttpResponse,Http404
from django.shortcuts import redirect, render
from .models import Rawmaterialdata,TodaysProdData,Instockqty,Totalselling,Manufacturingprice
from django.contrib.auth.models import User,auth
from django.contrib import messages
from json import dumps
# Create your views here.

def Loginuser(request):
    if request.method == "POST":
        vusername=request.POST.get('username')
        vpassword=request.POST.get('password')
        log_user=auth.authenticate(username=vusername,password=vpassword)
        if log_user is not None:
            auth.login(request,log_user)
            return redirect('/dashbord')
        else:
            messages.info(request,"username or password is in correct",extra_tags='alert-danger')
            return redirect('/')
    else:
        return render(request,'userlogin.html') 

def Userlogout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect("/")
    else:
        return HttpResponse("Error....")

def Dashbord(request):
    if request.user.is_authenticated:
        objtstock=Instockqty.objects.raw("select * from report_Instockqty join report_Manufacturingprice on report_Instockqty.name_id=report_Manufacturingprice.id order by report_Instockqty.name_id ASC")
        manuname=[]
        stockqty=[]
        for i in objtstock:
            manuname.append(i.name)
            stockqty.append(i.produceqty)
        manuJSON = dumps(manuname)
        stockJSON = dumps(stockqty)
        
        objrawdata=Rawmaterialdata.objects.raw("select * from report_rawmaterialdata join report_Manufacturingprice on report_rawmaterialdata.name_id = report_Manufacturingprice.id order by report_rawmaterialdata.name_id ASC")
        rawname=[]
        rawkqty=[]
        for i in objrawdata:
            rawname.append(i.name)
            rawkqty.append(i.rawqty)
        rawrawJSON = dumps(rawname)
        rawqtyJSON = dumps(rawkqty)

        context={'data':manuJSON,'sdata':stockJSON,'rndata':rawrawJSON,'rdata':rawqtyJSON}
        return render(request,'dashbord.html',context)
    else:
        return HttpResponse("Error....")
## show type of product and price
def Manufacturingcost(request):
    if request.user.is_authenticated:
        objmanu=Manufacturingprice.objects.all()
        return render(request,'manuprice.html',{'data':objmanu})
    else:
        return HttpResponse("Error....")
## edit product details
def Editproddetails(request,sid):
    if request.user.is_authenticated:
        objmanu=Manufacturingprice.objects.get(id=sid)
        if request.method == "POST":
            disc=request.POST.get('proddesc')
            manucost=request.POST.get('mprice')
            objmanu.disc=disc
            objmanu.manucost=manucost
            objmanu.save()
            messages.success(request," Details update successfullt..!!",extra_tags='alert-success')
            return redirect('/manucost')
        else:
            return render(request,'editmanuprod.html',{'data':objmanu})
    else:
        return HttpResponse("Error....")
## Add new type of product and price
def Addnewproduct(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            name=request.POST.get('prodname')
            disc=request.POST.get('proddesc')
            manucost=request.POST.get('mprice')
            objcnt=Manufacturingprice.objects.filter(name=name).count()
            if objcnt >= 1:
                messages.error(request,"This name is already exits...!!",extra_tags='alert-danger')
                return redirect('/addnewprod')
            else:
                objmanu=Manufacturingprice()
                objmanu.name=name
                objmanu.disc=disc
                objmanu.manucost=manucost
                objmanu.save()
                messages.success(request,"Product Add Successfully..!!",extra_tags='alert-success')
                return redirect('/manucost')
        else:
            return render(request,'addmanuprod.html')
    else:
        return HttpResponse("Error....")
## ajax (name already exits or not)
def CheckName(request):
    if request.user.is_authenticated:
        name=request.POST.get('name')
        objmanu=Manufacturingprice.objects.filter(name=name).count()
        return render(request,'checkname.html',{'data':objmanu})
    else:
        return HttpResponse("Error....")
## load Add raw material
def Rawmaterial(request):
    if request.user.is_authenticated:
        objmanu=Manufacturingprice.objects.all()
        return render(request,'rawmaterial.html',{'ptype':objmanu})
    else:
        return HttpResponse("Error....")
## Add raw material
def RawmaterialUpdate(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            name_id=request.POST.get('rawtype')
            rawqty=request.POST.get('quantity')
            totalInvest=request.POST.get('totalp')
            objrawdata=Rawmaterialdata.objects.filter(name_id=name_id).count()
            if objrawdata >=1:
                objrawdata=Rawmaterialdata.objects.get(name_id=name_id)
                objrawdata.rawqty=int(objrawdata.rawqty)+int(rawqty)
                objrawdata.totalqty=int(objrawdata.totalqty)+int(rawqty)
                objrawdata.totalInvest=int(objrawdata.totalInvest)+int(totalInvest)
            else:
                objrawdata=Rawmaterialdata()
                objrawdata.name_id=name_id
                objrawdata.rawqty=rawqty
                objrawdata.totalqty=rawqty
                objrawdata.totalInvest=totalInvest
            objrawdata.save()
            messages.success(request," Raw material Update Successfully..",extra_tags='alert-success')
            return redirect('/rawinput')
        else:
            return redirect('/rawinput')
    else:
        return HttpResponse("Error....")
## show total raw material
def ShowRawdata(request):
    if request.user.is_authenticated:
        objrawdata=Rawmaterialdata.objects.raw("select * from report_rawmaterialdata join report_Manufacturingprice on report_rawmaterialdata.name_id=report_Manufacturingprice.id order by report_rawmaterialdata.id ASC")
        return render(request,'showrawdata.html',{'data':objrawdata})
    else:
        return HttpResponse("Error....")
## Add todays production
def Todaysinput(request):
    if request.user.is_authenticated:
        objmanu=Manufacturingprice.objects.all()
        if request.method =="POST":
            date=request.POST.get('todaysdate')
            name_id=request.POST.get('rawtype')
            produce=request.POST.get('produceqty')
            reject=request.POST.get('rejectedqty')
            objcount=TodaysProdData.objects.filter(name_id=name_id,date=date).count() 
            objrawdata=Rawmaterialdata.objects.filter(name_id=name_id).count()
            objinstock=Instockqty.objects.filter(name_id=name_id).count()
            
            if objcount >=1:
                messages.warning(request, ' Data related this date is already exists!',extra_tags='alert-warning')
                return redirect('/todaysinput')

            elif objrawdata >=1:
                objrawdata=Rawmaterialdata.objects.get(name_id=name_id)
                if int(objrawdata.rawqty) <= (int(produce)+int(reject)):
                    messages.warning(request, ' Insufficient raw material..!',extra_tags='alert-warning')
                    return redirect('/todaysinput')
                else:
                    objtoday=TodaysProdData()
                    objtoday.date=date
                    objtoday.name_id=name_id
                    objtoday.produce=produce
                    objtoday.reject=reject
                    objtoday.save()

                    objrawdata.rawqty=int(objrawdata.rawqty)-int(produce)-int(reject)
                    objrawdata.save()
                    if objinstock >=1:
                        objinstock=Instockqty.objects.get(name_id=name_id)
                        objinstock.produceqty=int(objinstock.produceqty)+int(produce)
                        objinstock.rejectqty=int(objinstock.rejectqty)+int(reject)
                    else:
                        objinstock=Instockqty()
                        objinstock.name_id=name_id
                        objinstock.produceqty=produce
                        objinstock.rejectqty=reject
                    objinstock.save()

                    messages.success(request, ' Data Added Successfully!',extra_tags='alert-success')
                    return redirect('/todaysinput')
            else:
                messages.warning(request, ' Insufficient raw material.. or stock!',extra_tags='alert-warning')
                return redirect('/todaysinput')
        else:
            return render(request,'todaysdata.html',{'ptype':objmanu})
    else:
        return HttpResponse("Error....")
## show production
def Showproduction(request):
    if request.user.is_authenticated:
        objtoday=TodaysProdData.objects.raw("select * from report_todaysproddata join report_Manufacturingprice on report_todaysproddata.name_id=report_Manufacturingprice.id order by report_todaysproddata.date DESC")
        return render(request,'showproduction.html',{'data':objtoday})
    else:
        return HttpResponse("Error....")
## edit production 
def EditProduction(request,pid):
    if request.user.is_authenticated:
        objtoday=TodaysProdData.objects.get(id=pid)
        objmanu=Manufacturingprice.objects.all()
        if request.method =="POST":
            produce=request.POST.get('produceqty')
            reject=request.POST.get('rejectedqty')
            name_id=objtoday.name_id
            objtoday.produce=produce
            objtoday.reject=reject
            objtoday.save()
            objrawdata=Rawmaterialdata.objects.get(name_id=name_id)
            objrawdata.rawqty=int(objrawdata.rawqty)-int(produce)-int(reject)
            objrawdata.save()
            objinstock=Instockqty.objects.get(name_id=name_id)
            objinstock.produceqty=int(objinstock.produceqty)+int(produce)
            objinstock.rejectqty=int(objinstock.rejectqty)+int(reject)
            objinstock.save()
            return redirect('/showproduction')
        else:
            name_id=objtoday.name_id
            produce=objtoday.produce
            reject=objtoday.reject
            objrawdata=Rawmaterialdata.objects.get(name_id=name_id)
            objrawdata.rawqty=int(objrawdata.rawqty)+int(produce)+int(reject)
            objrawdata.save()
            objinstock=Instockqty.objects.get(name_id=name_id)
            objinstock.produceqty=int(objinstock.produceqty)-int(produce)
            objinstock.rejectqty=int(objinstock.rejectqty)-int(reject)
            objinstock.save()
            return render(request,'edittotalprod.html',{'data':objtoday,'ptype':objmanu})
    else:
        return HttpResponse("Error....")
## show Instock production
def Instock(request):
    if request.user.is_authenticated:
        objtoday=Instockqty.objects.raw("select * from report_Instockqty join report_Manufacturingprice on report_Instockqty.name_id=report_Manufacturingprice.id order by report_Instockqty.name_id ASC")
        return render(request,'instock.html',{'data':objtoday})
    else:
        return HttpResponse("Error....")
## show selling
def Showselling(request):
    if request.user.is_authenticated:
        objsell=Totalselling.objects.raw("select * from report_totalselling join report_Manufacturingprice on report_totalselling.name_id=report_Manufacturingprice.id order by report_totalselling.id DESC")
        return render(request,'showselling.html',{'data':objsell})
    else:
        return HttpResponse("Error....")
## sell product
def Prodselling(request):
    if request.user.is_authenticated:
        objmanu=Manufacturingprice.objects.all()
        if request.method =="POST":
            name_id=request.POST.get('rawtype')
            sellqty=request.POST.get('prodqty')
            sellingprice=request.POST.get('price')
            totalprofit=request.POST.get('totalprofit')
            totalprice=request.POST.get('totalprice')
            selldate=request.POST.get('todaysdate')
            objtoday=Instockqty.objects.get(name_id=name_id)
            if int(sellqty) <= int(objtoday.produceqty):
                objtoday.produceqty=int(objtoday.produceqty)-int(sellqty)
                objtoday.save()

                objsell=Totalselling()
                objsell.name_id=name_id
                objsell.sellqty=sellqty
                objsell.sellingprice=sellingprice
                objsell.totalprofit=totalprofit
                objsell.totalprice=totalprice
                objsell.selldate=selldate
                objsell.save()

                messages.success(request," Order Place Successfully..",extra_tags='alert-success')
                return redirect("/prodselling")
            else:
                messages.warning(request," You dont have enough Product to sell..",extra_tags='alert-warning')
                return redirect("/prodselling")
        else:
            return render(request,'totalselling.html',{'ptype':objmanu})
    else:
        return HttpResponse("Error....")


### ajax(get manufacturing cost for selected item)
def Getmanucost(request):
    if request.user.is_authenticated:
        name_id=request.POST.get('name')
        objmanu=Manufacturingprice.objects.get(id=name_id)
        return render(request,'getmanucost.html',{'data':objmanu})
    else:
        return HttpResponse("Error....")
### ajax(get available qty for selected item)  
def Getqty(request):
    if request.user.is_authenticated:
        name_id=request.POST.get('name')
        objtstock=Instockqty.objects.get(name_id=name_id)
        return render(request,'getqty.html',{'data':objtstock})
    

def ClearData(request):
    objtstock=Instockqty.objects.all()
    objsell=Totalselling.objects.all()
    objrawdata=Rawmaterialdata.objects.all()
    objtoday=TodaysProdData.objects.all()
    objrawdata.delete()
    objsell.delete()
    objtoday.delete()
    objtstock.delete()
    return redirect("/dashbord")