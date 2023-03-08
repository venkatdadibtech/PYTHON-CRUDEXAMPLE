from django.shortcuts import render,redirect
from storeproapp.models import Employee
from storeproapp.forms import EmployeeForm  
from django.http import HttpResponse
from django.db import connection


# Create your views here.
def show(request):  
    employees = Employee.objects.all()  
    return render(request,"show.html",{'employees':employees})

def inse(request):  
    return render(request,"insert.html") 

def emp(request):  
    if request.method == "POST":  
        form = EmployeeForm(request.POST)  
        if form.is_valid():  
            try:  
                with connection.cursor() as cursor:
                  cursor.execute("SELECT insert_employee()")
                return HttpResponse("Stored Procedure Called Successfully")
            except:  
                pass  
    else:  
        form = EmployeeForm()  
    return render(request,'index.html',{'form':form})

def insertdata(request):
    if request.method == 'POST':
        p_name = request.POST.get('txtempid')
        p_age = request.POST.get('txtempname')
        p_salary = request.POST.get('txtempmail')
        p_hire_date = request.POST.get('txtempcont')
        cursor = connection.cursor()
        cursor.execute('call insert_employee(%s,%s,%s,%s)',(p_name,p_age,p_salary,p_hire_date))
        connection.commit()
        print("Data Successfully Inserted")
        connection.close()
    return  redirect('/show')
def edit(request, id):  
    employee = Employee.objects.get(id=id)  
    return render(request,'edit.html', {'employee':employee})
def updatedata(request,id):
    if request.method == 'POST':  
        #p_id=Employee.objects.get(id=id)
        p_id=request.POST.get('id_id')
        p_eid=request.POST.get('id_eid')
        p_name=request.POST.get('id_ename')
        p_email=request.POST.get('id_eemail')
        p_econtact=request.POST.get('id_econtact')
        cursor = connection.cursor()
        cursor.execute('call update_employee(%s,%s,%s,%s,%s)',(p_id,p_econtact,p_name,p_email,p_eid))
        connection.commit()
        print("Data Successfully Updated")
        connection.close()
    return  redirect('/show')

def destroy(request, id):   
        p_id=int(id)
        cursor = connection.cursor()
        cursor.execute('call delete_employee(%s)',[p_id])
        connection.commit()
        print("Data Successfully Updated")
        connection.close()
        return  redirect('/show')