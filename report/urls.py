from django.urls import path
from . import views
urlpatterns = [
    
    path('',views.Loginuser),
    path('userlogout',views.Userlogout),
    path('dashbord',views.Dashbord),
    path('rawinput',views.Rawmaterial),
    path('rawmaterialupdate',views.RawmaterialUpdate),
    path('showrawdata',views.ShowRawdata),
    path('todaysinput',views.Todaysinput),
    path('showproduction',views.Showproduction),
    path('editprod/<int:pid>',views.EditProduction),
    path('instock',views.Instock),
    path('showselling',views.Showselling),
    path('prodselling',views.Prodselling),
    path('manucost',views.Manufacturingcost),
    path('addnewprod',views.Addnewproduct),
    path('editmanu/<int:sid>',views.Editproddetails),
    path('chkname',views.CheckName),
    path('getmanucost',views.Getmanucost),
    path('getqty',views.Getqty),

    path('cleardata',views.ClearData),
]