from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import operator_only, allowed_users
from django.http import JsonResponse
from invoice.models import *
from invoice.forms import *
from django.db.models import Sum
import datetime
import random
import string
from collections import OrderedDict
from .tasks import *


# Create your views here.
@login_required(login_url="login")
@operator_only
def home(request):
    vehicle = Vehicle.objects.all()
    # get count for models
    total = Vehicle.objects.all().count()
    driver = Driver.objects.all().count()
    student = Student.objects.all().count()
    faculty = Faculty.objects.all().count()
    staff = Staff.objects.all().count()
    return render(request, "dashboard.html",
                  {"vehicle": vehicle, "driver": driver, "staff": staff,
                   "student": student, "faculty": faculty,
                   "room_name": "broadcast", "total": total})


# error page
@login_required(login_url='login')
@allowed_users(allowed_roles=['operator', 'principal'])
def error_404_view(request, exception):
    return render(request, 'error/404.html')


# start vehicle
@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def create_vehicle(request):
    if request.method == "POST":
        form = VehicleForm(request.POST or None)
        if form.is_valid():
            if Vehicle.objects.filter(vehicle_no=form.cleaned_data['vehicle_no']).exists():
                return render(request, "invoice/create_vehicle.html", {"form": form, "error": "Vehicle already exists"})
            else:
                instance = form.save(commit=False)
                if request.user.is_authenticated:
                    instance.user = request.user
                instance.save()
                return redirect("view_vehicle")
    else:
        form = VehicleForm()
    return render(request, "invoice/create_vehicle.html", {"form": form, "room_name": "broadcast"})


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator", "principal"])
def view_vehicle(request):
    vehicle = Vehicle.objects.all()
    # get count for models
    total = Vehicle.objects.all().count()
    driver = Driver.objects.all().count()
    staff = Staff.objects.all().count()
    student = Student.objects.all().count()
    faculty = Faculty.objects.all().count()
    return render(
        request,
        "dashboard.html",
        {
            "vehicle": vehicle,
            "total": total,
            "driver": driver,
            "staff": staff,
            "student": student,
            "faculty": faculty,
            "room_name": "broadcast",
        },
    )


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def detail_vehicle(request, id):
    vehicle = get_object_or_404(Vehicle, id=id)
    return render(
        request,
        "invoice/detail_vehicle.html",
        {
            "vehicle": vehicle,
            "room_name": "broadcast",
        },
    )


# start Driver Views
@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def create_driver(request):
    form = DriverForm()
    if request.method == 'POST':
        form = DriverForm(request.POST, request.FILES)
        document = request.FILES.getlist("document")
        if form.is_valid():
            if Driver.objects.filter(name=form.cleaned_data['name']).exists():
                return render(request, "invoice/create_driver.html", {"form": form, "error": "Driver already exists"})

            elif Driver.objects.filter(phone=form.cleaned_data['phone']).exists():
                return render(request, "invoice/create_driver.html", {"form": form, "error": "Driver Phone already exists"})

            elif Driver.objects.filter(dl_no=form.cleaned_data['dl_no']).exists():
                return render(request, "invoice/create_driver.html", {"form": form, "error": "Driver License already exists"})

            elif Driver.objects.filter(adhar=form.cleaned_data['adhar']).exists():
                return render(request, "invoice/create_driver.html", {"form": form, "error": "Driver Aadhar already exists"})

            elif Driver.objects.filter(pan=form.cleaned_data['pan']).exists():
                return render(request, "invoice/create_driver.html", {"form": form, "error": "Driver Pan already exists"})

            else:
                form = form.save(commit=False)
                for doc in document:
                    form.document = doc
                    form.save()
                return redirect("driver_list")
    return render(request, "invoice/create_driver.html", {"form": form, "room_name": "broadcast"})


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def view_driver(request):
    driver = Driver.objects.all().order_by('-id')[:15]
    employee_id = request.POST.get('employee_id')
    if employee_id:
        driver = Driver.objects.filter(employee_id=employee_id)
        return render(request, "invoice/driver_list.html", {"driver": driver, "room_name": "broadcast"})
    return render(request, "invoice/driver_list.html", {"driver": driver, "room_name": "broadcast"})


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def detail_driver(request, id):
    driver = get_object_or_404(Driver, id=id)
    return render(request, "invoice/detail_driver.html", {"driver": driver, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def update_driver(request, id):
    driver = Driver.objects.get(id=id)
    form = UpdateDriverForm(request.POST, instance=driver)
    if request.method == "POST":
        form = UpdateDriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            return redirect("driver_list")
    else:
        form = UpdateDriverForm(instance=driver)
    return render(request, "invoice/create_driver.html", {"form": form, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def delete_driver(request, id):
    driver_obj = get_object_or_404(Driver, id=id)
    driver_obj.delete()
    return redirect("driver_list")


# Start staff views
@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def create_staff(request):
    form = StaffForm()
    if request.method == "POST":
        form = StaffForm(request.POST, request.FILES)
        document = request.FILES.getlist("document")
        if form.is_valid():
            if Staff.objects.filter(name=form.cleaned_data['name']).exists():
                return render(request, "invoice/create_staff.html", {"form": form, "error": "Staff already exists"})

            elif Staff.objects.filter(phone=form.cleaned_data['phone']).exists():
                return render(request, "invoice/create_staff.html", {"form": form, "error": "Staff Phone already exists"})

            elif Staff.objects.filter(adhar=form.cleaned_data['adhar']).exists():
                return render(request, "invoice/create_staff.html", {"form": form, "error": "Staff Aadhar already exists"})

            elif Staff.objects.filter(pan=form.cleaned_data['pan']).exists():
                return render(request, "invoice/create_staff.html", {"form": form, "error": "Staff Pan already exists"})

            else:
                form = form.save(commit=False)
                for doc in document:
                    form.document = doc
                    form.save()
                return redirect("staff_list")
    return render(request, "invoice/create_staff.html", {"form": form, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def view_staff(request):
    staff = Staff.objects.all().order_by('-id')[:15]
    helper = Staff.objects.filter(designation="Helper").count()
    office_staff = Staff.objects.filter(designation="Office Staff").count()
    mechanic = Staff.objects.filter(designation="Mechanic").count()
    # totoal staff count
    total = Staff.objects.all().count()
    # search
    employee_id = request.POST.get('employee_id')
    if employee_id:
        staff = Staff.objects.filter(employee_id=employee_id)
        return render(request, "invoice/staff_list.html", {"staff": staff, "total": total, "room_name": "broadcast"})
    return render(request, "invoice/staff_list.html", {"staff": staff, "helper": helper, "office_staff": office_staff, "mechanic": mechanic, "total": total, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def detail_staff(request, id):
    staff = get_object_or_404(Staff, id=id)
    return render(request, "invoice/detail_staff.html", {"staff": staff, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def update_staff(request, id):
    staff = Staff.objects.get(id=id)
    form = UpdateStaffForm(request.POST, instance=staff)
    if request.method == "POST":
        form = UpdateStaffForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            return redirect("staff_list")
    else:
        form = UpdateStaffForm(instance=staff)
    return render(request, "invoice/create_staff.html", {"form": form, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def delete_staff(request, id):
    staff_obj = get_object_or_404(Staff, id=id)
    staff_obj.delete()
    return redirect("staff_list")


# start Logsheet
@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def get_logsheet_distance_to(request, id):
    logsheet = Logsheet.objects.filter(log__vehicle=id).last() or None
    if logsheet:
        return JsonResponse({"distance_to": logsheet.distance_to})
    if logsheet is None:
        return JsonResponse({"distance_to": 0})


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def create_logsheet(request):
    drivers = Driver.objects.all()
    vehicles = Vehicle.objects.all()
    if request.method == "POST":
        vehicle_id = request.POST.get("vehicle")
        vehicle = Vehicle.objects.get(id=vehicle_id)
        date = request.POST.get("date")
        # logsheet data
        trip = request.POST.getlist("trip")
        time_from = request.POST.getlist("start_time")
        time_to = request.POST.getlist("end_time")
        source = request.POST.getlist("source")
        destination = request.POST.getlist("destination")
        distance_from = request.POST.getlist("distance_from")
        distance_to = request.POST.getlist("distance_to")
        driver_id = request.POST.getlist("driver")
        driver = []
        for i in driver_id:
            data = Driver.objects.filter(id__in=i)
            for d in data:
                driver.append(d)
        # main logic
        if vehicle and date:
            log = Log(vehicle=vehicle, date_time=date)
            log.save()
            data = zip(trip, driver, distance_from, distance_to,
                       time_from, time_to, source, destination)
            for trip, driver, distance_from, distance_to, time_from, time_to, source, destination in data:
                if trip and driver and distance_from and distance_to and time_from and time_to and source and destination:
                    if source == destination:
                        log.delete()
                        return render(request, "invoice/create_logsheet.html", {"error": "Source and Destination can't be same", "drivers": drivers, "vehicles": vehicles, "room_name": "broadcast", })         
                    elif int(distance_from) > int(distance_to):
                        log.delete()
                        return render(request, "invoice/create_logsheet.html", {"error": "Distance from can't be greater than distance to", "drivers": drivers, "vehicles": vehicles, "room_name": "broadcast", })     
                    elif time_from > time_to:
                        log.delete()
                        return render(request, "invoice/create_logsheet.html", {"error": "Time from can't be greater than time to", "drivers": drivers, "vehicles": vehicles, "room_name": "broadcast", })
                    else:
                        logdetail = Logsheet(log=log, trip=trip, driver=driver, distance_from=distance_from, distance_to=distance_to,
                                            time_from=time_from, time_to=time_to, source=source, destination=destination,)
                        logdetail.save()
                else:
                    log.delete()
                    return render(request, "invoice/create_logsheet.html", {"error": "Please fill all fields", "drivers": drivers, "vehicles": vehicles, "room_name": "broadcast", },)
            return redirect("logsheet_list")
        else:
            return render(request, "invoice/create_logsheet.html", {"error": "Please fill all fields", "drivers": drivers, "vehicles": vehicles, "room_name": "broadcast", },)
    return render(request, "invoice/create_logsheet.html", {"drivers": drivers, "vehicles": vehicles, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def view_logsheet(request):
    # date lookup exact, gt, gte, lt, lte, ne, in, range
    date = request.POST.get("date")
    vehicle = request.POST.get("vehicle")
    if date and vehicle:
        logs = Log.objects.filter(date=date, vehicle__vehicle_no=vehicle)
        return render(request, "invoice/logsheet_list.html", {"logs": logs, "room_name": "broadcast"})

    elif date:
        logs = Log.objects.filter(date=date)
        return render(request, "invoice/logsheet_list.html", {"logs": logs, "room_name": "broadcast"})

    elif vehicle:
        logs = Log.objects.filter(vehicle__vehicle_no=vehicle)
        return render(request, "invoice/logsheet_list.html", {"logs": logs, "room_name": "broadcast"})

    else:
        logs = Log.objects.filter(date_time__exact=datetime.date.today()).order_by('id')
        # logs = Log.objects.all().order_by('-id')[:15]
        return render(request, "invoice/logsheet_list.html", {"logs": logs, "room_name": "broadcast"})


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def update_logsheet(request, id):
    drivers = Driver.objects.all()
    vehicles = Vehicle.objects.all()
    log = Log.objects.get(id=id)
    if request.method == "POST":
        vehicle_id = request.POST.get("vehicle")
        vehicle = Vehicle.objects.get(id=vehicle_id)
        date = request.POST.get("date")
        # logsheet data
        trip = request.POST.getlist("trip")
        time_from = request.POST.getlist("time_from")
        time_to = request.POST.getlist("time_to")
        source = request.POST.getlist("source")
        destination = request.POST.getlist("destination")
        distance_from = request.POST.getlist("distance_from")
        distance_to = request.POST.getlist("distance_to")
        driver_id = request.POST.getlist("driver")
        driver = []
        for i in driver_id:
            data = Driver.objects.filter(id__in=i)
            for d in data:
                driver.append(d)
        # main logic
        if vehicle and date and trip and driver and time_from and time_to and source and destination:
            Logsheet.objects.filter(log=log).delete()
            Log.objects.filter(id=id).update(vehicle=vehicle, date_time=date)
            data = zip(trip, driver, distance_from, distance_to,
                       time_from, time_to, source, destination)
            for trip, driver, distance_from, distance_to, time_from, time_to, source, destination in data:
                if trip and driver and distance_from and distance_to and time_from and time_to and source and destination:
                    if source == destination:
                        return render(request, "invoice/update_logsheet.html", {"error": "Source and Destination can't be same", "drivers": drivers, "vehicles": vehicles, "log": log, "room_name": "broadcast", })                    
                    elif time_from > time_to:
                        return render(request, "invoice/update_logsheet.html", {"error": "Time from can't be greater than time to", "drivers": drivers, "vehicles": vehicles, "log": log, "room_name": "broadcast", })
                    logdetail = Logsheet(log=log, trip=trip, driver=driver, distance_from=distance_from, distance_to=distance_to,
                                         time_from=time_from, time_to=time_to, source=source, destination=destination,)
                    logdetail.save()
                else:
                    return render(request, "invoice/update_logsheet.html", {"error": "Please fill all fields", "drivers": drivers, "vehicles": vehicles, "room_name": "broadcast", },)
            return redirect("logsheet_list")
        else:
            return render(request, "invoice/update_logsheet.html", {"drivers": drivers, "vehicles": vehicles, "log": log, "room_name": "broadcast", "error": "Please fill all the fields", })
    return render(request, "invoice/update_logsheet.html", {"log": log, 'drivers': drivers, 'vehicles': vehicles, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def delete_logsheet(request, id):
    log = Log.objects.get(id=id)
    log.delete()
    return redirect("logsheet_list")


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def logsheet_other(request):
    log = Log.objects.all().order_by('-date_time')
    return render(request, "invoice/logsheet_other.html", {"log": log, "room_name": "broadcast", })


# start fuel view
@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def get_vehicle_progressive_km(request, id):
    fuel = Fuel.objects.filter(vehicle=id).order_by('-id')[:1]
    if fuel:
        for f in fuel:
            return JsonResponse({
                'vehicle': f.vehicle.vehicle_no,
                'progressive_km': f.progressive_km,
                "room_name": "broadcast",
            })
    else:
        return JsonResponse({
            'vehicle': "",
            'progressive_km': 0,
            "room_name": "broadcast",
        })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def create_fuel(request):
    vehicles = Vehicle.objects.all()
    if request.method == "POST":
        vehicle_id = request.POST.get("vehicle")
        vehicle = Vehicle.objects.get(id=vehicle_id)   # get vehicle object
        fuel_type = request.POST.get("fuel_type")
        vendor_name = request.POST.get("vendor_name")
        indent_no = request.POST.get("indent_no")
        quantity = request.POST.get("quantity")
        bill_no = request.POST.get("bill_no")
        amount = request.POST.get("amount")
        previous_km = request.POST.get("previous_km")
        progressive_km = request.POST.get("progressive_km")
        date = request.POST.get("date")

        if vehicle and fuel_type and vendor_name and indent_no and quantity and bill_no and amount and previous_km and progressive_km and date:
            if Fuel.objects.filter(vehicle=vehicle, bill_no=bill_no).exists():
                return render(request, "invoice/create_fuel.html", {"vehicles": vehicles, "room_name": "broadcast", "error": "Bill No Already Exists !"})

            else:
                fuel = Fuel(vehicle=vehicle, fuel_type=fuel_type, vendor_name=vendor_name, indent_no=indent_no,
                            quantity=quantity, bill_no=bill_no, amount=amount, previous_km=previous_km, progressive_km=progressive_km, date=date)
                fuel.save()
                return redirect("fuel_list")
    return render(request, "invoice/create_fuel.html", {"vehicles": vehicles, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def view_fuel(request):
    fuel = Fuel.objects.all()
    month_filter = request.POST.get("month")
    vehicle_filter = request.POST.get("vehicle")
    if month_filter and vehicle_filter:
        fuel = fuel.filter(date__month=month_filter.split(
            "-")[1], vehicle__vehicle_no=vehicle_filter)
        amount = fuel.all().aggregate(Sum("amount"))["amount__sum"] or 0
        return render(request, "invoice/fuel_list.html", {"fuel": fuel, "amount": amount, "room_name": "broadcast", })

    elif month_filter:
        fuel = fuel.filter(date__month=month_filter.split("-")[1])
        amount = fuel.all().aggregate(Sum("amount"))["amount__sum"] or 0
        return render(request, "invoice/fuel_list.html", {"fuel": fuel, "amount": amount, "room_name": "broadcast", })

    elif vehicle_filter:
        fuel = fuel.filter(vehicle__vehicle_no=vehicle_filter)
        amount = fuel.all().aggregate(Sum("amount"))["amount__sum"] or 0
        return render(request, "invoice/fuel_list.html", {"fuel": fuel, "amount": amount, "room_name": "broadcast", })

    else:
        fuel = fuel.all()
        return render(request, "invoice/fuel_list.html", {"fuel": fuel, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def detail_fuel(request, id):
    fuel = get_object_or_404(Fuel, id=id)
    return render(request, "invoice/detail_fuel.html", {"fuel": fuel, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def update_fuel(request, id):
    fuel = Fuel.objects.get(id=id)
    if request.method == "POST":
        vehicle_id = request.POST.get("vehicle")
        vehicle = Vehicle.objects.get(id=vehicle_id)
        fuel_type = request.POST.get("fuel_type")
        vendor_name = request.POST.get("vendor_name")
        indent_no = request.POST.get("indent_no")
        quantity = request.POST.get("quantity")
        bill_no = request.POST.get("bill_no")
        amount = request.POST.get("amount")
        previous_km = float(request.POST.get("previous_km"))
        progressive_km = float(request.POST.get("progressive_km"))
        date = request.POST.get("date")

        if previous_km > progressive_km:
            return render(request, "invoice/update_fuel.html", {"fuel": fuel, "room_name": "broadcast", "error": "Previous Km is greater than progressive km"})
        else:
            Fuel.objects.filter(id=id).update(
                vehicle=vehicle,
                fuel_type=fuel_type,
                vendor_name=vendor_name,
                indent_no=indent_no,
                quantity=quantity,
                bill_no=bill_no,
                amount=amount,
                previous_km=previous_km,
                progressive_km=progressive_km,
                date=date)
            return redirect("fuel_list")
        return render(request, "invoice/update_fuel.html", {"fuel": fuel, "room_name": "broadcast", })
    return render(request, "invoice/update_fuel.html", {"fuel": fuel, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def delete_fuel(request, id):
    fuel = Fuel.objects.get(id=id)
    fuel.delete()
    return redirect("fuel_list")


# start Lubricant
@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def get_oilchange(request, id):
    lubricant = Lubricant.objects.filter(vehicle=id).order_by('-id')[:1]
    if lubricant:
        for f in lubricant:
            return JsonResponse({
                'vehicle': f.vehicle.vehicle_no,
                'progressive_km': f.progressive_km,
                "room_name": "broadcast",
            })
    else:
        return JsonResponse({
            'vehicle': "",
            'progressive_km': 0,
            "room_name": "broadcast",
        })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def create_lubricant(request):
    vehicles = Vehicle.objects.all()
    if request.method == "POST":
        vehicle_id = request.POST.get("vehicle")
        vehicle = Vehicle.objects.get(id=vehicle_id)   # get vehicle object
        oil_type = request.POST.get("oil_type")
        supplier_name = request.POST.get("supplier_name")
        bill_no = request.POST.get("bill_no")
        grade = request.POST.get("grade")
        quantity = request.POST.get("quantity")
        cost = request.POST.get("cost")
        previous_km = request.POST.get("previous_km")
        progressive_km = request.POST.get("progressive_km")
        date = request.POST.get("date")
        # main filter
        if Lubricant.objects.filter(vehicle=vehicle, bill_no=bill_no).exists():
            return render(request, "invoice/create_lubricant.html", {"room_name": "broadcast", "vehicles": vehicles, "error": "Vehicle and Bill No already exists !"})

        else:
            lubricant = Lubricant(vehicle=vehicle, oil_type=oil_type, supplier_name=supplier_name, bill_no=bill_no,
                                  grade=grade, quantity=quantity, cost=cost, previous_km=previous_km, progressive_km=progressive_km, date=date)
            lubricant.save()
            return redirect("lubricant_list")
    return render(request, "invoice/create_lubricant.html", {"room_name": "broadcast", "vehicles": vehicles, })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def view_lubricant(request):
    oil = Lubricant.objects.all()
    month_filter = request.POST.get("month")
    vehicle_filter = request.POST.get("vehicle")
    if month_filter and vehicle_filter:
        oil = oil.filter(date__month=month_filter.split(
            "-")[1], vehicle__vehicle_no=vehicle_filter)
        amount = oil.all().aggregate(Sum("cost"))["cost__sum"] or 0
        return render(request, "invoice/lubricant_list.html", {"oil": oil, "amount": amount, "room_name": "broadcast", })

    elif month_filter:
        oil = oil.filter(date__month=month_filter.split("-")[1])
        amount = oil.all().aggregate(Sum("cost"))["cost__sum"] or 0
        return render(request, "invoice/lubricant_list.html", {"oil": oil, "amount": amount, "room_name": "broadcast", })

    elif vehicle_filter:
        oil = oil.filter(vehicle__vehicle_no=vehicle_filter)
        amount = oil.all().aggregate(Sum("cost"))["cost__sum"] or 0
        return render(request, "invoice/lubricant_list.html", {"oil": oil, "amount": amount, "room_name": "broadcast", })

    else:
        oil = oil.all()
        return render(request, "invoice/lubricant_list.html", {"oil": oil, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def detail_lubricant(request, id):
    oil = get_object_or_404(Lubricant, id=id)
    return render(request, "invoice/detail_lubricant.html", {"oil": oil, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def update_lubricant(request, id):
    lubricant = Lubricant.objects.get(id=id)
    if request.method == "POST":
        vehicle_id = request.POST.get("vehicle")
        vehicle = Vehicle.objects.get(id=vehicle_id)
        oil_type = request.POST.get("oil_type")
        supplier_name = request.POST.get("supplier_name")
        bill_no = request.POST.get("bill_no")
        grade = request.POST.get("grade")
        quantity = request.POST.get("quantity")
        cost = request.POST.get("cost")
        previous_km = float(request.POST.get("previous_km"))
        progressive_km = float(request.POST.get("progressive_km"))
        date = request.POST.get("date")
        if previous_km > progressive_km:
            return render(request, "invoice/update_lubricant.html", {"lubricant": lubricant, "room_name": "broadcast", "error": "Previous KM should be less than Progressive KM"})
        else:
            Lubricant.objects.filter(id=id).update(
                vehicle=vehicle,
                oil_type=oil_type,
                supplier_name=supplier_name,
                bill_no=bill_no,
                grade=grade,
                quantity=quantity,
                cost=cost,
                previous_km=previous_km,
                progressive_km=progressive_km,
                date=date)
            return redirect("lubricant_list")
    return render(request, "invoice/update_lubricant.html", {"lubricant": lubricant, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def delete_lubricant(request, id):
    lubricant = Lubricant.objects.get(id=id)
    lubricant.delete()
    return redirect("lubricant_list")


# start Tyres views
@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def get_tyre(request, tyre_no):
    # tyre = Tyre.objects.filter(vehicle=id).order_by('-id')[:1]
    tyre = Tyre.objects.filter(tyre_no=tyre_no).order_by('-id')[:1]
    print(tyre)
    if tyre:
        for t in tyre:
            return JsonResponse({
                'vehicle': t.vehicle.vehicle_no,
                'rebelt_no': t.rebelt_no,
                'removal_km': t.removal_km,
                "tyre_no": t.tyre_no,
                "room_name": "broadcast",
            })
    else:
        return JsonResponse({
            'vehicle': "",
            'removal_km': 0,
            "tyre_no": "",
            "room_name": "broadcast",
        })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def create_tyre(request):
    vehicles = Vehicle.objects.all()
    if request.method == "POST":
        vehicle_id = request.POST.get("vehicle")
        vehicle = Vehicle.objects.get(id=vehicle_id)   # get vehicle object
        version = request.POST.get("version")
        position = request.POST.get("position")
        scrap = request.POST.get("scrap")

        tyre_no = request.POST.get("tyre_no")
        rebelt_no = request.POST.get("rebelt_no")
        tyre_type = request.POST.get("tyre_type")

        make = request.POST.get("make")
        size = request.POST.get("size")
        vendor_name = request.POST.get("vendor_name")
        amount = request.POST.get("amount")
        bill_no = request.POST.get("bill_no")
        cause_of_removal = request.POST.get("cause_of_removal")

        fitted_km = request.POST.get("fitted_km")
        fitted_date = request.POST.get("fitted_date")
        removal_km = request.POST.get("removal_km")
        removal_date = request.POST.get("removal_date")
        documents = request.FILES.getlist("document")
        actual_km = float(removal_km) - float(fitted_km)
        if vehicle and version and position and scrap and tyre_no and tyre_type and make and size and vendor_name and amount and fitted_km and fitted_date:
            if Tyre.objects.filter(bill_no=bill_no).exists():
                return render(request, "invoice/create_tyre.html", {"vehicles": vehicles, "room_name": "broadcast", "error": "Tyre with this Bill No already exists"})
            else:
                tyre = Tyre.objects.create(
                    vehicle=vehicle,
                    version=version,
                    position=position,
                    scrap=scrap,
                    tyre_no=tyre_no,
                    rebelt_no=rebelt_no,
                    tyre_type=tyre_type,
                    make=make,
                    size=size,
                    vendor_name=vendor_name,
                    amount=amount,
                    bill_no=bill_no,
                    cause_of_removal=cause_of_removal,
                    fitted_km=fitted_km,
                    fitted_date=fitted_date,
                    removal_km=removal_km,
                    removal_date=removal_date,
                    documents=documents,
                    actual_km=actual_km,
                )
                return redirect("tyre_list")
        else:
            return render(request, "invoice/create_tyre.html", {"vehicles": vehicles, "room_name": "broadcast", "error": "Please fill all the fields"})
    return render(request, "invoice/create_tyre.html", {"room_name": "broadcast", "vehicles": vehicles, })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def view_tyre(request):
    tyre = Tyre.objects.all()
    tyre_no = request.POST.get("tyre_no")
    month_filter = request.POST.get("month")

    if month_filter and tyre_no:
        tyre = tyre.filter(
            fitted_date__month=month_filter.split("-")[1], tyre_no=tyre_no)
        amount = tyre.all().aggregate(Sum("amount"))["amount__sum"] or 0
        total_km = tyre.all().aggregate(Sum("actual_km"))["actual_km__sum"] or 0
        return render(request, "invoice/tyre_list.html", {"tyre": tyre, "amount": amount, "total_km":total_km, "room_name": "broadcast", })

    elif month_filter:
        tyre = tyre.filter(fitted_date__month=month_filter.split("-")[1])
        amount = tyre.all().aggregate(Sum("amount"))["amount__sum"] or 0
        total_km = tyre.all().aggregate(Sum("actual_km"))["actual_km__sum"] or 0
        return render(request, "invoice/tyre_list.html", {"tyre": tyre, "amount": amount, "total_km":total_km, "room_name": "broadcast", })

    elif tyre_no:
        tyre = tyre.filter(tyre_no=tyre_no)
        amount = tyre.all().aggregate(Sum("amount"))["amount__sum"] or 0
        total_km = tyre.all().aggregate(Sum("actual_km"))["actual_km__sum"] or 0
        return render(request, "invoice/tyre_list.html", {"tyre": tyre, "amount": amount, "total_km":total_km, "room_name": "broadcast", })

    else:
        tyre = tyre.all().order_by("tyre_no")
        return render(request, "invoice/tyre_list.html", {"tyre": tyre, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def detail_tyre(request, id):
    tyre = get_object_or_404(Tyre, id=id)
    return render(request, "invoice/detail_tyre.html", {"tyre": tyre, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def update_tyre(request, id):
    tyre = Tyre.objects.get(id=id)
    if request.method == "POST":
        vehicle_id = request.POST.get("vehicle")
        vehicle = Vehicle.objects.get(id=vehicle_id)   # get vehicle object
        version = request.POST.get("version")
        position = request.POST.get("position")
        scrap = request.POST.get("scrap")

        tyre_no = request.POST.get("tyre_no")
        rebelt_no = request.POST.get("rebelt_no")
        tyre_type = request.POST.get("tyre_type")

        make = request.POST.get("make")
        size = request.POST.get("size")
        vendor_name = request.POST.get("vendor_name")
        amount = request.POST.get("amount")
        bill_no = request.POST.get("bill_no")
        cause_of_removal = request.POST.get("cause_of_removal")

        fitted_km = float(request.POST.get("fitted_km"))
        fitted_date = request.POST.get("fitted_date")
        removal_km = float(request.POST.get("removal_km"))
        removal_date = request.POST.get("removal_date")
        actual_km = removal_km - fitted_km
        if fitted_km > removal_km:
            return render(request, "invoice/update_tyre.html", {"tyre": tyre, "room_name": "broadcast", "error": "Fitted km should be less than removal km"})
        else:
            tyre = Tyre.objects.filter(id=id).update(
                vehicle=vehicle,
                version=version,
                position=position,
                tyre_no=tyre_no,
                rebelt_no=rebelt_no,
                tyre_type=tyre_type,
                make=make,
                size=size,
                bill_no=bill_no,
                vendor_name=vendor_name,
                amount=amount,
                cause_of_removal=cause_of_removal,
                scrap=scrap,
                fitted_km=fitted_km,
                fitted_date=fitted_date,
                removal_km=removal_km,
                removal_date=removal_date,
                actual_km=actual_km,
            )
        return redirect("tyre_list")
    return render(request, "invoice/update_tyre.html", {"room_name": "broadcast", "tyre": tyre, })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def delete_tyre(request, id):
    tyre = Tyre.objects.get(id=id)
    tyre.delete()
    return redirect("tyre_list")


# start battery
@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def get_battery(request, battery_no):
    # battery = Battery.objects.filter(vehicle=id).order_by('-id')[:1]
    battery = Battery.objects.filter(battery_no=battery_no).order_by('-id')[:1]
    if battery:
        for b in battery:
            return JsonResponse({
                'vehicle': b.vehicle.vehicle_no,
                "battery_no": b.battery_no,
                "removal_km": b.removal_km,
                "room_name": "broadcast",
            })
    else:
        return JsonResponse({
            'vehicle': "",
            "battery_no": "",
            "removal_km": 0,
            "room_name": "broadcast",
        })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def create_battery(request):
    vehicles = Vehicle.objects.all()
    if request.method == "POST":
        vehicle_id = request.POST.get("vehicle")
        vehicle = Vehicle.objects.get(id=vehicle_id)
        type = request.POST.get("type")
        battery_no = request.POST.get("battery_no")
        vendor_name = request.POST.get("vendor_name")
        make = request.POST.get("make")
        amount = request.POST.get("amount")
        cause_of_removal = request.POST.get("cause_of_removal")
        bill_no = request.POST.get("bill_no")
        fitted_km = request.POST.get("fitted_km")
        removal_km = request.POST.get("removal_km")
        fitted_date = request.POST.get("fitted_date")
        removal_date = request.POST.get("removal_date")
        # main
        if vehicle and type and battery_no and vendor_name and make and amount and fitted_km and fitted_date and removal_km and removal_date:
            if (Battery.objects.filter(bill_no=bill_no).exists()):
                return render(request, "invoice/create_battery.html", {"vehicles": vehicles, "room_name": "broadcast", "error": "Battery with this bill no already exists"})
            else:
                battery = Battery(
                    vehicle=vehicle,
                    type=type,
                    battery_no=battery_no,
                    vendor_name=vendor_name,
                    make=make,
                    bill_no=bill_no,
                    amount=amount,
                    cause_of_removal=cause_of_removal,
                    fitted_km=fitted_km,
                    fitted_date=fitted_date,
                    removal_km=removal_km,
                    removal_date=removal_date,
                )
            battery.save()
            return redirect("battery_list")
        else:
            return render(request, "invoice/create_battery.html", {"vehicles": vehicles, "room_name": "broadcast", "error": "Please fill all the fields"})
    return render(request, "invoice/create_battery.html", {"room_name": "broadcast", "vehicles": vehicles, })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def view_battery(request):
    battery = Battery.objects.all()
    month_filter = request.POST.get("month")
    vehicle_filter = request.POST.get("vehicle")
    battery_filter = request.POST.get("battery")
    # searching
    if month_filter and vehicle_filter:
        battery = battery.filter(fitted_date__month=month_filter.split(
            "-")[1], vehicle__vehicle_no=vehicle_filter)
        amount = battery.all().aggregate(Sum("amount"))["amount__sum"] or 0
        return render(request, "invoice/battery_list.html", {"battery": battery, "amount": amount, "room_name": "broadcast", })

    elif month_filter:
        battery = battery.filter(fitted_date__month=month_filter.split("-")[1])
        amount = battery.all().aggregate(Sum("amount"))["amount__sum"] or 0
        return render(request, "invoice/battery_list.html", {"battery": battery, "amount": amount, "room_name": "broadcast", })

    elif vehicle_filter:
        battery = battery.filter(vehicle__vehicle_no=vehicle_filter)
        amount = battery.all().aggregate(Sum("amount"))["amount__sum"] or 0
        return render(request, "invoice/battery_list.html", {"battery": battery, "amount": amount, "room_name": "broadcast", })

    elif battery_filter:
        battery = battery.filter(battery_no=battery_filter)
        amount = battery.all().aggregate(Sum("amount"))["amount__sum"] or 0
        return render(request, "invoice/battery_list.html", {"battery": battery, "amount": amount, "room_name": "broadcast", })

    elif battery_filter and vehicle_filter:
        battery = battery.filter(battery_no=battery_filter,
                                 vehicle__vehicle_no=vehicle_filter)
        amount = battery.all().aggregate(Sum("amount"))["amount__sum"] or 0
        return render(request, "invoice/battery_list.html", {"battery": battery, "amount": amount, "room_name": "broadcast", })

    elif battery_filter and month_filter:
        battery = battery.filter(battery_no=battery_filter,
                                 fitted_date__month=month_filter.split("-")[1])
        amount = battery.all().aggregate(Sum("amount"))["amount__sum"] or 0
        return render(request, "invoice/battery_list.html", {"battery": battery, "amount": amount, "room_name": "broadcast", })
           
    
    else:
        battery = battery.all().order_by("battery_no")
        return render(request, "invoice/battery_list.html", {"battery": battery, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def detail_battery(request, id):
    battery = get_object_or_404(Battery, id=id)
    return render(request, "invoice/detail_battery.html", {"battery": battery, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def update_battery(request, id):
    battery = Battery.objects.get(id=id)
    if request.method == "POST":
        vehicle_id = request.POST.get("vehicle")
        vehicle = Vehicle.objects.get(id=vehicle_id)
        type = request.POST.get("type")
        battery_no = request.POST.get("battery_no")
        vendor_name = request.POST.get("vendor_name")
        make = request.POST.get("make")
        cause_of_removal = request.POST.get("cause_of_removal")
        bill_no = request.POST.get("bill_no")
        amount = request.POST.get("amount")
        fitted_km = float(request.POST.get("fitted_km"))
        removal_km = float(request.POST.get("removal_km"))
        fitted_date = request.POST.get("fitted_date")
        removal_date = request.POST.get("removal_date")
        # main
        if fitted_km > removal_km:
            return render(request, "invoice/update_battery.html", {"room_name": "broadcast", "battery": battery, "error": "Fitted KM should be less than Removal KM"})

        elif fitted_date > removal_date:
            return render(request, "invoice/update_battery.html", {"room_name": "broadcast", "battery": battery, "error": "Fitted Date should be less than Removal Date"})

        else:
            battery = Battery.objects.filter(id=id).update(
                vehicle=vehicle,
                type=type,
                battery_no=battery_no,
                vendor_name=vendor_name,
                make=make,
                cause_of_removal=cause_of_removal,
                bill_no=bill_no,
                amount=amount,
                fitted_km=fitted_km,
                removal_km=removal_km,
                fitted_date=fitted_date,
                removal_date=removal_date)
            return redirect("battery_list")
    return render(request, "invoice/update_battery.html", {"room_name": "broadcast", "battery": battery, })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def delete_battery(request, id):
    battery = Battery.objects.get(id=id)
    battery.delete()
    return redirect("battery_list")


# Documents views
@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def create_tax(request):
    form = TaxationForm()
    if request.method == "POST":
        form = TaxationForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data["tax_from"] > form.cleaned_data["tax_to"]:
                return render(request, "invoice/create_tax.html", {"form": form, "room_name": "broadcast", "error": "Tax From should be less than Tax To"})
            form.save()
            return redirect("tax_list")
    return render(request, "invoice/create_tax.html", {"form": form, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def tax_list(request):
    tax = Tax.objects.all()
    month_filter = request.POST.get("month")
    vehicle_filter = request.POST.get("vehicle")
    # searching
    if month_filter and vehicle_filter:
        tax = tax.filter(tax_from__month=month_filter.split(
            "-")[1], vehicle__vehicle_no=vehicle_filter)
        amount = tax.all().aggregate(Sum("tax_amount"))["tax_amount__sum"] or 0
        return render(request, "invoice/tax_list.html", {"tax": tax, "amount": amount, "room_name": "broadcast", })
    elif month_filter:
        tax = tax.filter(tax_from__month=month_filter.split("-")[1])
        amount = tax.all().aggregate(Sum("tax_amount"))["tax_amount__sum"] or 0
        return render(request, "invoice/tax_list.html", {"tax": tax, "amount": amount, "room_name": "broadcast", })
    elif vehicle_filter:
        tax = tax.filter(vehicle__vehicle_no=vehicle_filter)
        amount = tax.all().aggregate(Sum("tax_amount"))["tax_amount__sum"] or 0
        return render(request, "invoice/tax_list.html", {"tax": tax, "amount": amount, "room_name": "broadcast", })
    else:
        tax = tax.all().order_by("tax_no").order_by("-id")
        return render(request, "invoice/tax_list.html", {"tax": tax, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def update_tax(request, id):
    tax = Tax.objects.get(id=id)
    form = TaxationForm(instance=tax)
    if request.method == "POST":
        form = TaxationForm(request.POST, request.FILES, instance=tax)
        if form.is_valid():
            form.save()
            return redirect("tax_list")
    return render(request, "invoice/update_tax.html", {"form": form, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def delete_tax(request, id):
    tax = Tax.objects.get(id=id)
    tax.delete()
    return redirect("tax_list")


# Insurance views
@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def create_insurance(request):
    form = InsuranceForm()
    if request.method == "POST":
        form = InsuranceForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data["insurance_from"] > form.cleaned_data["insurance_to"]:
                return render(request, "invoice/create_insurance.html", {"form": form, "room_name": "broadcast", "error": "Insurance From should be less than Insurance To"})
            form.save()
            return redirect("insurance_list")
    return render(request, "invoice/create_insurance.html", {"form": form, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def insurance_list(request):
    insurance = Insurance.objects.all()
    month_filter = request.POST.get("month")
    vehicle_filter = request.POST.get("vehicle")
    # searching
    if month_filter and vehicle_filter:
        insurance = insurance.filter(insurance_from__month=month_filter.split(
            "-")[1], vehicle__vehicle_no=vehicle_filter)
        amount = insurance.all().aggregate(Sum("insurance_amount"))[
            "insurance_amount__sum"] or 0
        return render(request, "invoice/insurance_list.html", {"insurance": insurance, "amount": amount, "room_name": "broadcast", })
    elif month_filter:
        insurance = insurance.filter(
            insurance_from__month=month_filter.split("-")[1])
        amount = insurance.all().aggregate(Sum("insurance_amount"))[
            "insurance_amount__sum"] or 0
        return render(request, "invoice/insurance_list.html", {"insurance": insurance, "amount": amount, "room_name": "broadcast", })
    elif vehicle_filter:
        insurance = insurance.filter(vehicle__vehicle_no=vehicle_filter)
        amount = insurance.all().aggregate(Sum("insurance_amount"))[
            "insurance_amount__sum"] or 0
        return render(request, "invoice/insurance_list.html", {"insurance": insurance, "amount": amount, "room_name": "broadcast", })
    else:
        insurance = insurance.all().order_by("-id")
        return render(request, "invoice/insurance_list.html", {"insurance": insurance, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def update_insurance(request, id):
    insurance = Insurance.objects.get(id=id)
    form = InsuranceForm(instance=insurance)
    if request.method == "POST":
        form = InsuranceForm(request.POST, request.FILES, instance=insurance)
        if form.is_valid():
            form.save()
            return redirect("insurance_list")
    return render(request, "invoice/update_insurance.html", {"form": form, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def delete_insurance(request, id):
    insurance = Insurance.objects.get(id=id)
    insurance.delete()
    return redirect("insurance_list")


# Permit views
@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def create_permit(request):
    form = PermitForm()
    if request.method == "POST":
        form = PermitForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data["permit_from"] > form.cleaned_data["permit_to"]:
                return render(request, "invoice/create_permit.html", {"form": form, "room_name": "broadcast", "error": "Permit From should be less than Permit To"})
            form.save()
            return redirect("permit_list")
    return render(request, "invoice/create_permit.html", {"form": form, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def permit_list(request):
    permit = Permit.objects.all()
    month_filter = request.POST.get("month")
    vehicle_filter = request.POST.get("vehicle")
    # searching
    if month_filter and vehicle_filter:
        permit = permit.filter(permit_from__month=month_filter.split(
            "-")[1], vehicle__vehicle_no=vehicle_filter)
        amount = permit.all().aggregate(Sum("permit_amount"))[
            "permit_amount__sum"] or 0
        return render(request, "invoice/permit_list.html", {"permit": permit, "amount": amount, "room_name": "broadcast", })
    elif month_filter:
        permit = permit.filter(permit_from__month=month_filter.split("-")[1])
        amount = permit.all().aggregate(Sum("permit_amount"))[
            "permit_amount__sum"] or 0
        return render(request, "invoice/permit_list.html", {"permit": permit, "amount": amount, "room_name": "broadcast", })
    elif vehicle_filter:
        permit = permit.filter(vehicle__vehicle_no=vehicle_filter)
        amount = permit.all().aggregate(Sum("permit_amount"))[
            "permit_amount__sum"] or 0
        return render(request, "invoice/permit_list.html", {"permit": permit, "amount": amount, "room_name": "broadcast", })
    else:
        permit = permit.all().order_by("-id")
        return render(request, "invoice/permit_list.html", {"permit": permit, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def update_permit(request, id):
    permit = Permit.objects.get(id=id)
    form = PermitForm(instance=permit)
    if request.method == "POST":
        form = PermitForm(request.POST, request.FILES, instance=permit)
        if form.is_valid():
            form.save()
            return redirect("permit_list")
    return render(request, "invoice/update_permit.html", {"form": form, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def delete_permit(request, id):
    permit = Permit.objects.get(id=id)
    permit.delete()
    return redirect("permit_list")


# Emission views
@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def create_emission(request):
    form = EmissionForm()
    if request.method == "POST":
        form = EmissionForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data["emission_from"] > form.cleaned_data["emission_to"]:
                return render(request, "invoice/create_emission.html", {"form": form, "room_name": "broadcast", "error": "Emission From should be less than Emission To"})
            form.save()
            return redirect("emission_list")
    return render(request, "invoice/create_emission.html", {"form": form, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def emission_list(request):
    emission = Emission.objects.all()
    month_filter = request.POST.get("month")
    vehicle_filter = request.POST.get("vehicle")
    # searching
    if month_filter and vehicle_filter:
        emission = emission.filter(emission_from__month=month_filter.split(
            "-")[1], vehicle__vehicle_no=vehicle_filter)
        amount = emission.all().aggregate(Sum("emission_amount"))[
            "emission_amount__sum"] or 0
        return render(request, "invoice/emission_list.html", {"emission": emission, "amount": amount, "room_name": "broadcast", })
    elif month_filter:
        emission = emission.filter(
            emission_from__month=month_filter.split("-")[1])
        amount = emission.all().aggregate(Sum("emission_amount"))[
            "emission_amount__sum"] or 0
        return render(request, "invoice/emission_list.html", {"emission": emission, "amount": amount, "room_name": "broadcast", })
    elif vehicle_filter:
        emission = emission.filter(vehicle__vehicle_no=vehicle_filter)
        amount = emission.all().aggregate(Sum("emission_amount"))[
            "emission_amount__sum"] or 0
        return render(request, "invoice/emission_list.html", {"emission": emission, "amount": amount, "room_name": "broadcast", })
    else:
        emission = emission.all().order_by("-id")
        return render(request, "invoice/emission_list.html", {"emission": emission, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def update_emission(request, id):
    emission = Emission.objects.get(id=id)
    form = EmissionForm(instance=emission)
    if request.method == "POST":
        form = EmissionForm(request.POST, request.FILES, instance=emission)
        if form.is_valid():
            form.save()
            return redirect("emission_list")
    return render(request, "invoice/update_emission.html", {"form": form, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def delete_emission(request, id):
    emission = Emission.objects.get(id=id)
    emission.delete()
    return redirect("emission_list")


# Fitness Certificate views
@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def create_fitness(request):
    form = FitnessForm()
    if request.method == "POST":
        form = FitnessForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data["fc_from"] > form.cleaned_data["fc_to"]:
                return render(request, "invoice/create_fitness.html", {"form": form, "room_name": "broadcast", "error": "Fitness From should be less than Fitness To"})
            form.save()
            return redirect("fitness_list")
    return render(request, "invoice/create_fitness.html", {"form": form, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def fitness_list(request):
    fitness = Fitness.objects.all()
    month_filter = request.POST.get("month")
    vehicle_filter = request.POST.get("vehicle")
    # searching
    if month_filter and vehicle_filter:
        fitness = fitness.filter(fc_from__month=month_filter.split(
            "-")[1], vehicle__vehicle_no=vehicle_filter)
        amount = fitness.all().aggregate(Sum("fc_amount"))[
            "fc_amount__sum"] or 0
        return render(request, "invoice/fitness_list.html", {"fitness": fitness, "amount": amount, "room_name": "broadcast", })
    elif month_filter:
        fitness = fitness.filter(fc_from__month=month_filter.split("-")[1])
        amount = fitness.all().aggregate(Sum("fc_amount"))[
            "fc_amount__sum"] or 0
        return render(request, "invoice/fitness_list.html", {"fitness": fitness, "amount": amount, "room_name": "broadcast", })
    elif vehicle_filter:
        fitness = fitness.filter(vehicle__vehicle_no=vehicle_filter)
        amount = fitness.all().aggregate(Sum("fc_amount"))[
            "fc_amount__sum"] or 0
        return render(request, "invoice/fitness_list.html", {"fitness": fitness, "amount": amount, "room_name": "broadcast", })
    else:
        fitness = fitness.all().order_by("-id")
        return render(request, "invoice/fitness_list.html", {"fitness": fitness, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def update_fitness(request, id):
    fitness = Fitness.objects.get(id=id)
    form = FitnessForm(instance=fitness)
    if request.method == "POST":
        form = FitnessForm(request.POST, request.FILES, instance=fitness)
        if form.is_valid():
            form.save()
            return redirect("fitness_list")
    return render(request, "invoice/update_fitness.html", {"form": form, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def delete_fitness(request, id):
    fitness = Fitness.objects.get(id=id)
    fitness.delete()
    return redirect("fitness_list")


# Repair views
@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def create_repair(request):
    form = RepairForm()
    if request.method == "POST":
        form = RepairForm(request.POST)
        if form.is_valid():
            if Repair.objects.filter(vehicle=form.cleaned_data["vehicle"], bill_no=form.cleaned_data["bill_no"]).exists():
                return render(request, "invoice/create_repair.html", {"form": form, "error": "Repair with Bill No already exists", "room_name": "broadcast", })
            form.save()
            return redirect("repair_list")
        else:
            return render(request, "invoice/create_repair.html", {"form": form, "room_name": "broadcast", })
    return render(request, "invoice/create_repair.html", {"form": form, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def view_repair(request):
    repair = Repair.objects.all()
    vehicle = request.POST.get("vehicle")
    month = request.POST.get("month")
    if vehicle and month:
        repair = repair.filter(vehicle__vehicle_no=vehicle,
                               date__month=month.split("-")[1])
        amount = repair.all().aggregate(Sum("amount"))["amount__sum"] or 0
        return render(request, "invoice/repair_list.html", {"repair": repair, "amount": amount, "room_name": "broadcast", })

    elif vehicle:
        repair = repair.filter(vehicle__vehicle_no=vehicle)
        amount = repair.all().aggregate(Sum("amount"))["amount__sum"] or 0
        return render(request, "invoice/repair_list.html", {"repair": repair, "amount": amount, "room_name": "broadcast", })

    elif month:
        repair = repair.filter(date__month=month.split("-")[1])
        amount = repair.all().aggregate(Sum("amount"))["amount__sum"] or 0
        return render(request, "invoice/repair_list.html", {"repair": repair, "amount": amount, "room_name": "broadcast", })

    else:
        repair = repair.all()
        return render(request, "invoice/repair_list.html", {"repair": repair, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def detail_repair(request, id):
    repair = get_object_or_404(Repair, id=id)
    return render(request, "invoice/detail_repair.html", {"repair": repair, "room_name": "broadcast", })


# start spareparts views
@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def create_spare(request):
    vehicles = Vehicle.objects.all()
    if request.method == "POST":
        vehicle_id = request.POST.get("vehicle")
        vehicle = Vehicle.objects.get(id=vehicle_id)
        vendor_name = request.POST.get("vendor_name")
        bill_no = request.POST.get("bill_no")
        cause_of_removal = request.POST.get("cause_of_removal")
        date = request.POST.get("date")
        # get details
        sl_no = request.POST.getlist("sl_no")
        product_name = request.POST.getlist("product_name")
        quantity = request.POST.getlist("quantity")
        cost = request.POST.getlist("cost")
        amount = request.POST.getlist("amount")
        # create token
        char = string.ascii_uppercase + string.digits
        token = ''.join(random.choice(char) for _ in range(10))
        # save spare models
        if sl_no and product_name and quantity and cost and amount:
            spare = Spare(vehicle=vehicle, vendor_name=vendor_name, bill_no=bill_no,
                          cause_of_removal=cause_of_removal, date=date, token_no=token)
            spare.save()
            data = zip(sl_no, product_name, quantity, cost, amount)
            for d in data:
                sparepart = SpareParts(
                    spare=spare, sl_no=d[0], product_name=d[1], quantity=d[2], cost=d[3], amount=d[4])
                sparepart.save()
            return redirect("service_list")
        else:
            spare.delete()
            return render(request, "invoice/create_spare.html", {"vehicles": vehicles, "error": "Please fill all the fields", "room_name": "broadcast", })
    return render(request, "invoice/create_spare.html", {"room_name": "broadcast", "vehicles": vehicles, })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def view_spare(request):
    sparepart = SpareParts.objects.all()
    vehicle = request.POST.get("vehicle")
    bill = request.POST.get("bill_no")
    month_filter = request.POST.get("month")

    # seraching by month and vehicle
    if month_filter and vehicle:
        sparepart = sparepart.filter(spare__date__month=month_filter.split(
            "-")[1], spare__vehicle__vehicle_no=vehicle)
        spare = Spare.objects.filter(date__month=month_filter.split(
            "-")[1], vehicle__vehicle_no=vehicle)

        amount = sparepart.all().aggregate(Sum("amount"))["amount__sum"] or 0
        return render(request, "invoice/spare_list.html", {"sparepart": sparepart, "spare": spare, "amount": amount, "room_name": "broadcast"})

    elif month_filter:
        sparepart = sparepart.filter(
            spare__date__month=month_filter.split("-")[1])
        spare = Spare.objects.filter(date__month=month_filter.split("-")[1])
        amount = sparepart.all().aggregate(Sum("amount"))["amount__sum"] or 0
        return render(request, "invoice/spare_list.html", {"sparepart": sparepart, "spare": spare, "amount": amount, "room_name": "broadcast"})

    elif vehicle:
        sparepart = sparepart.filter(spare__vehicle__vehicle_no=vehicle)
        spare = Spare.objects.filter(vehicle__vehicle_no=vehicle)
        amount = sparepart.all().aggregate(Sum("amount"))["amount__sum"] or 0
        return render(request, "invoice/spare_list.html", {"sparepart": sparepart, "spare": spare, "amount": amount, "room_name": "broadcast"})

    elif bill:
        sparepart = sparepart.filter(spare__bill_no=bill)
        spare = Spare.objects.filter(bill_no=bill)
        amount = sparepart.all().aggregate(Sum("amount"))["amount__sum"] or 0
        return render(request, "invoice/spare_list.html", {"sparepart": sparepart, "spare": spare, "amount": amount, "room_name": "broadcast", })

    else:
        sparepart = sparepart.all()
        spare = Spare.objects.all()
        return render(request, "invoice/spare_list.html", {"sparepart": sparepart, "spare": spare, "room_name": "broadcast"})


# start other expense view
@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def create_other(request):
    vehicles = Vehicle.objects.all()
    if request.method == "POST":
        vehicle_id = request.POST.get("vehicle")
        vehicle = Vehicle.objects.get(id=vehicle_id)
        vendor_name = request.POST.get("vendor_name")
        bill_no = request.POST.get("bill_no")
        date = request.POST.get("date")
        # details
        sl_no = request.POST.getlist("sl_no")
        product_name = request.POST.getlist("product_name")
        quantity = request.POST.getlist("quantity")
        cost = request.POST.getlist("cost")
        # total amount of each product by multiplying quantity and cost
        amount = request.POST.getlist("amount")

        if sl_no and product_name and quantity and cost and amount:
            other = Other(vehicle=vehicle, vendor_name=vendor_name,
                          bill_no=bill_no, date=date)
            other.save()
            data = zip(sl_no, product_name, quantity, cost, amount)
            for d in data:
                otherexpense = OtherExpense(
                    other=other, sl_no=d[0], product_name=d[1], quantity=d[2], cost=d[3], amount=d[4])
                otherexpense.save()
            return redirect("other_list")
    return render(request, "invoice/create_other.html", {"room_name": "broadcast", "vehicles": vehicles, })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def view_other(request):
    otherexpense = OtherExpense.objects.all()
    month_filter = request.POST.get("month")
    vehicle = request.POST.get("vehicle")
    bill = request.POST.get("bill_no")
    # seraching by month and vehicle
    if month_filter and vehicle:
        otherexpense = otherexpense.filter(other__date__month=month_filter.split(
            "-")[1], other__vehicle__vehicle_no=vehicle)
        other = Other.objects.filter(date__month=month_filter.split(
            "-")[1], vehicle__vehicle_no=vehicle)
        amount = otherexpense.all().aggregate(
            Sum("amount"))["amount__sum"] or 0
        return render(request, "invoice/other_list.html", {"otherexpense": otherexpense, "other": other, "amount": amount, "room_name": "broadcast", })

    elif month_filter:
        otherexpense = otherexpense.filter(
            other__date__month=month_filter.split("-")[1])
        other = Other.objects.filter(date__month=month_filter.split("-")[1])
        amount = otherexpense.all().aggregate(
            Sum("amount"))["amount__sum"] or 0
        return render(request, "invoice/other_list.html", {"otherexpense": otherexpense, "other": other, "amount": amount, "room_name": "broadcast", })

    elif vehicle:
        otherexpense = otherexpense.filter(other__vehicle__vehicle_no=vehicle)
        other = Other.objects.filter(vehicle__vehicle_no=vehicle)
        amount = otherexpense.all().aggregate(
            Sum("amount"))["amount__sum"] or 0
        return render(request, "invoice/other_list.html", {"otherexpense": otherexpense, "other": other, "amount": amount, "room_name": "broadcast", })

    elif bill:
        otherexpense = otherexpense.filter(other__bill_no=bill)
        other = Other.objects.filter(bill_no=bill)
        amount = otherexpense.all().aggregate(
            Sum("amount"))["amount__sum"] or 0
        return render(request, "invoice/other_list.html", {"otherexpense": otherexpense, "other": other, "amount": amount, "room_name": "broadcast", })

    else:
        otherexpense = otherexpense.all()
        other = Other.objects.all()
        return render(request, "invoice/other_list.html", {"otherexpense": otherexpense, "other": other, "room_name": "broadcast", })


# Scrap Expense View
@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def create_scrap(request):
    form = ScrapForm()
    if request.method == "POST":
        form = ScrapForm(request.POST, request.FILES)
        document = request.FILES.getlist("document")
        if form.is_valid():
            if Scrap.objects.filter(vehicle=form.cleaned_data["vehicle"], bill_no=form.cleaned_data["bill_no"]).exists():
                return render(request, "invoice/create_scrap.html", {"form": form, "error": "Scrap with Bill No already exists", "room_name": "broadcast", })
            form = form.save(commit=False)
            for doc in document:
                form.document = doc
                form.save()
            return redirect("scrap_list")
        else:
            return render(request, "invoice/create_scrap.html", {"form": form, "room_name": "broadcast", })
    return render(request, "invoice/create_scrap.html", {"form": form, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def view_scrap(request):
    scrap = Scrap.objects.all()
    month_filter = request.POST.get("month")
    vehicle_filter = request.POST.get("vehicle")
    if month_filter and vehicle_filter:
        scrap = scrap.filter(date__month=month_filter.split(
            "-")[1], vehicle__vehicle_no=vehicle_filter)
        amount = scrap.all().aggregate(Sum("amount"))["amount__sum"] or 0
        return render(request, "invoice/scrap_list.html", {"scrap": scrap, "amount": amount, "room_name": "broadcast", })

    elif month_filter:
        scrap = scrap.filter(date__month=month_filter.split("-")[1])
        amount = scrap.all().aggregate(Sum("amount"))["amount__sum"] or 0
        return render(request, "invoice/scrap_list.html", {"scrap": scrap, "amount": amount, "room_name": "broadcast", })

    elif vehicle_filter:
        scrap = scrap.filter(vehicle__vehicle_no=vehicle_filter)
        amount = scrap.all().aggregate(Sum("amount"))["amount__sum"] or 0
        return render(request, "invoice/scrap_list.html", {"scrap": scrap, "amount": amount, "room_name": "broadcast", })

    else:
        scrap = scrap.all()
        return render(request, "invoice/scrap_list.html", {"scrap": scrap, "room_name": "broadcast", })


# student view
@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def create_student(request):
    form = StudentForm()
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        document = request.FILES.getlist("document")
        if form.is_valid():
            if Student.objects.filter(name=form.cleaned_data["name"]).exists():
                return render(request, "invoice/create_student.html", {"form": form, "error": "Student with this name already exists", "room_name": "broadcast", })

            elif Student.objects.filter(usn=form.cleaned_data["usn"]).exists():
                return render(request, "invoice/create_student.html", {"form": form, "error": "Student with this USN already exists", "room_name": "broadcast", })

            elif Student.objects.filter(contact=form.cleaned_data["contact"]).exists():
                return render(request, "invoice/create_student.html", {"form": form, "error": "Student with this Contact already exists", "room_name": "broadcast", })

            else:
                form = form.save(commit=False)
                for doc in document:
                    form.document = doc
                    form.save()
                return redirect("student_list")
        else:
            return render(request, "invoice/create_student.html", {"form": form, "room_name": "broadcast", })
    return render(request, "invoice/create_student.html", {"form": form, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def student_list(request):
    student = Student.objects.all()
    usn_filter = request.POST.get("usn")
    if usn_filter:
        student = student.filter(usn__icontains=usn_filter)
        return render(request, "invoice/student_list.html", {"student": student, "room_name": "broadcast", })
    else:
        student = student.all()
        return render(request, "invoice/student_list.html", {"student": student, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def student_detail(request, id):
    student = get_object_or_404(Student, id=id)
    return render(request, "invoice/detail_student.html", {"student": student, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def student_update(request, id):
    student = Student.objects.get(id=id)
    form = StudentUpdateForm(request.POST, instance=student)
    if request.method == "POST":
        form = StudentUpdateForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect("student_list")
    else:
        form = StudentUpdateForm(instance=student)
    return render(request, "invoice/create_student.html", {"form": form, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def student_delete(request, id):
    student = Student.objects.get(id=id)
    student.delete()
    return redirect("student_list")


# Faculty views
@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def create_faculty(request):
    if request.method == "POST":
        form = FacultyForm(request.POST or request.FILES)
        document = request.FILES.getlist("document")
        if form.is_valid():
            if Faculty.objects.filter(name=form.cleaned_data["name"]).exists():
                return render(request, "invoice/create_faculty.html", {"form": form, "error": "Faculty with this name already exists", "room_name": "broadcast", })

            elif Faculty.objects.filter(contact=form.cleaned_data["contact"]).exists():
                return render(request, "invoice/create_faculty.html", {"form": form, "error": "Faculty with this contact already exists", "room_name": "broadcast", })

            else:
                form = form.save(commit=False)
                for doc in document:
                    form.document = doc
                    form.save()
                return redirect("faculty_list")
    else:
        form = FacultyForm()
    return render(request, "invoice/create_faculty.html", {"form": form, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def faculty_list(request):
    faculty = Faculty.objects.all()
    name_filter = request.POST.get("name")
    if name_filter:
        faculty = faculty.filter(name__icontains=name_filter)
        return render(request, "invoice/faculty_list.html", {"faculty": faculty, "room_name": "broadcast", })
    else:
        faculty = faculty.all()
        return render(request, "invoice/faculty_list.html", {"faculty": faculty, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def detail_faculty(request, id):
    faculty = get_object_or_404(Faculty, id=id)
    return render(request, "invoice/detail_faculty.html", {"faculty": faculty, "room_name": "broadcast", })


@login_required(login_url="login")
@allowed_users(allowed_roles=["operator"])
def faculty_delete(request, id):
    faculty = Faculty.objects.get(id=id)
    faculty.delete()
    redirect("faculty_list")


# Report views
@login_required(login_url="login")
@allowed_users(allowed_roles=["principal", "operator"])
def year_report(request):
    vehicle_data = []
    all_vehicle_expenses = OrderedDict({})
    for vehicle in Vehicle.objects.all():
        expenses = OrderedDict({})
        months_full = ["january", "february", "march", "april", "may", "june",
                       "july", "august", "september", "october", "november", "december"]
        for month in months_full:
            expenses.setdefault(month, 0)
            all_vehicle_expenses.setdefault(month, 0)

        for fuel in vehicle.fuels.all().order_by("-date"):
            month_name = fuel.date.strftime("%B").lower()
            expenses.setdefault(month_name, 0)
            expenses[month_name] += fuel.amount

            all_vehicle_expenses.setdefault(month_name, 0)
            all_vehicle_expenses[month_name] += fuel.amount

        for lubricant in vehicle.lubricants.all().order_by("-date"):
            month_name = lubricant.date.strftime("%B").lower()
            expenses.setdefault(month_name, 0)
            expenses[month_name] += lubricant.cost

            all_vehicle_expenses.setdefault(month_name, 0)
            all_vehicle_expenses[month_name] += lubricant.cost

        for tyre in vehicle.tyres.all().order_by("-fitted_date"):
            month_name = tyre.fitted_date.strftime("%B").lower()
            expenses.setdefault(month_name, 0)
            expenses[month_name] += tyre.amount

            all_vehicle_expenses.setdefault(month_name, 0)
            all_vehicle_expenses[month_name] += tyre.amount

        for battery in vehicle.batteries.all().order_by("-fitted_date"):
            month_name = battery.fitted_date.strftime("%B").lower()
            expenses.setdefault(month_name, 0)
            expenses[month_name] += battery.amount

            all_vehicle_expenses.setdefault(month_name, 0)
            all_vehicle_expenses[month_name] += battery.amount

        for repair in vehicle.repairs.all().order_by("-date"):
            month_name = repair.date.strftime("%B").lower()
            expenses.setdefault(month_name, 0)
            expenses[month_name] += repair.amount

            all_vehicle_expenses.setdefault(month_name, 0)
            all_vehicle_expenses[month_name] += repair.amount

        for spare in vehicle.spares.all().order_by("-date"):
            month_name = spare.date.strftime("%B").lower()
            expenses.setdefault(month_name, 0)
            expenses[month_name] += spare.total

            all_vehicle_expenses.setdefault(month_name, 0)
            all_vehicle_expenses[month_name] += spare.total

        vehicle_data.append([vehicle.vehicle_no, expenses])
        print(vehicle_data)
        print(all_vehicle_expenses)

    return render(request, "invoice/year_report.html", {
        "vehicle_prices": vehicle_data,
        "total_expenses": all_vehicle_expenses,
        'room_name': "broadcast",
        "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    })



@login_required(login_url="login")
@allowed_users(allowed_roles=["principal", "operator"])
def full_details(request):
    log = Log.objects.all()
    fuel = Fuel.objects.all()
    lubricant = Lubricant.objects.all()
    tyre = Tyre.objects.all()
    battery = Battery.objects.all()
    tax = Tax.objects.all()
    insurance = Insurance.objects.all()
    fitness = Fitness.objects.all()
    permit = Permit.objects.all()
    emission = Emission.objects.all()
    repair = Repair.objects.all()
    spare = Spare.objects.all()
    other = Other.objects.all()
    scrap = Scrap.objects.all()
    student = Student.objects.all()
    if request.method == "POST":
        vehicle = request.POST.get("vehicle")
        month = request.POST.get("month")
        year = request.POST.get("year")
        if vehicle and month and year:
            log = log.filter(vehicle__vehicle_no=vehicle, date_time__month=month, date_time__year=year)
            fuel = fuel.filter(vehicle__vehicle_no=vehicle, date__month=month, date__year=year)
            lubricant = lubricant.filter(vehicle__vehicle_no=vehicle, date__month=month, date__year=year)
            tyre = tyre.filter(vehicle__vehicle_no=vehicle, fitted_date__month=month, fitted_date__year=year)
            battery = battery.filter(vehicle__vehicle_no=vehicle, fitted_date__month=month, fitted_date__year=year)
            tax = tax.filter(vehicle__vehicle_no=vehicle, tax_from__month=month, tax_from__year=year)
            insurance = insurance.filter(vehicle__vehicle_no=vehicle, insurance_from__month=month, insurance_from__year=year)
            fitness = fitness.filter(vehicle__vehicle_no=vehicle, fc_from__month=month, fc_from__year=year)
            permit = permit.filter(vehicle__vehicle_no=vehicle, permit_from__month=month, permit_from__year=year)
            emission = emission.filter(vehicle__vehicle_no=vehicle, emission_from__month=month, emission_from__year=year)
            repair = repair.filter(vehicle__vehicle_no=vehicle, date__month=month, date__year=year)
            spare = spare.filter(vehicle__vehicle_no=vehicle, date__month=month, date__year=year)
            other = other.filter(vehicle__vehicle_no=vehicle, date__month=month, date__year=year)
            scrap = scrap.filter(vehicle__vehicle_no=vehicle, date__month=month, date__year=year)
            student = student.filter(vehicle__vehicle_no=vehicle, enroll_date__month=month, enroll_date__year=year)
            # total expenses for a vehicle from each model
            fuel_amount = fuel.all().aggregate(Sum("amount"))["amount__sum"] or 0
            lubricant_amount = lubricant.all().aggregate(Sum("cost"))["cost__sum"] or 0
            tyre_amount = tyre.all().aggregate(Sum("amount"))["amount__sum"] or 0
            battery_amount = battery.all().aggregate(Sum("amount"))["amount__sum"] or 0
            tax_amount = tax.all().aggregate(Sum("tax_amount"))["tax_amount__sum"] or 0
            insurance_amount = insurance.all().aggregate(Sum("insurance_amount"))["insurance_amount__sum"] or 0
            fitness_amount = fitness.all().aggregate(Sum("fc_amount"))["fc_amount__sum"] or 0
            permit_amount = permit.all().aggregate(Sum("permit_amount"))["permit_amount__sum"] or 0
            emission_amount = emission.all().aggregate(Sum("emission_amount"))["emission_amount__sum"] or 0
            repair_amount = repair.all().aggregate(Sum("amount"))["amount__sum"] or 0
            scrap_amount = scrap.all().aggregate(Sum("amount"))["amount__sum"] or 0
            # spare part amount
            spare_amount = 0
            for i in spare:
                spare_amount = spare_amount + i.total
            # other amount
            other_amount = 0
            for i in other:
                other_amount = other_amount + i.total
            
            
            context = {
                'vehicle': vehicle,
                'log': log,
                'fuel': fuel,
                'lubricant': lubricant,
                'tyre': tyre,
                'battery': battery,
                'tax': tax,
                'insurance': insurance,
                'fitness': fitness,
                'permit': permit,
                'emission': emission,
                'repair': repair,
                'spare': spare,
                'other': other,
                'scrap': scrap,
                'student': student,
                # amount
                'fuel_amount': fuel_amount,
                'lubricant_amount': lubricant_amount,
                'tyre_amount': tyre_amount,
                'battery_amount': battery_amount,
                'tax_amount': tax_amount,
                'insurance_amount': insurance_amount,
                'fitness_amount': fitness_amount,
                'permit_amount': permit_amount,
                'emission_amount': emission_amount,
                'repair_amount': repair_amount,
                'spare_amount': spare_amount,
                'other_amount': other_amount,
                'scrap_amount': scrap_amount,
                'room_name': "broadcast",
            }
            return render(request, "invoice/year_detail.html", context)
        else:
            return redirect("full_details")
    return render(request, "invoice/year_detail.html",{'room_name': "broadcast",})


# invoice views
@login_required(login_url="login")
@allowed_users(allowed_roles=["operator", "principal"])
def invoice(request):
    fuel = Fuel.objects.all()
    lubricant = Lubricant.objects.all()
    tyre = Tyre.objects.all()
    battery = Battery.objects.all()
    sparepart = SpareParts.objects.all()
    other = OtherExpense.objects.all()
    repair = Repair.objects.all()
    # model for taxation
    tax = Tax.objects.all()
    insurance = Insurance.objects.all()
    permit = Permit.objects.all()
    emission = Emission.objects.all()
    fitness = Fitness.objects.all()
    # get signature query
    today = datetime.date.today()
    sign = Signature.objects.filter(date__day=today.day) or None
    if sign:
        sign = sign[0]
    # get total amount
    vehicle_filter = request.POST.get("vehicle")
    month_filter = request.POST.get("month")
    # filtering
    if month_filter and vehicle_filter:
        fuel = fuel.filter(date__month=month_filter.split(
            "-")[1], vehicle__vehicle_no=vehicle_filter)
        lubricant = lubricant.filter(date__month=month_filter.split(
            "-")[1], vehicle__vehicle_no=vehicle_filter)
        tyre = tyre.filter(fitted_date__month=month_filter.split(
            "-")[1], vehicle__vehicle_no=vehicle_filter)
        battery = battery.filter(fitted_date__month=month_filter.split(
            "-")[1], vehicle__vehicle_no=vehicle_filter,)
        repair = repair.filter(date__month=month_filter.split(
            "-")[1], vehicle__vehicle_no=vehicle_filter)
        sparepart = sparepart.filter(spare__date__month=month_filter.split(
            "-")[1], spare__vehicle__vehicle_no=vehicle_filter)
        other = other.filter(other__date__month=month_filter.split(
            "-")[1], other__vehicle__vehicle_no=vehicle_filter)
        # model for taxation
        tax = tax.filter(tax_from__month=month_filter.split(
            "-")[1], vehicle__vehicle_no=vehicle_filter)
        insurance = insurance.filter(insurance_from__month=month_filter.split(
            "-")[1], vehicle__vehicle_no=vehicle_filter)
        permit = permit.filter(permit_from__month=month_filter.split(
            "-")[1], vehicle__vehicle_no=vehicle_filter)
        emission = emission.filter(emission_from__month=month_filter.split(
            "-")[1], vehicle__vehicle_no=vehicle_filter)
        fitness = fitness.filter(fc_from__month=month_filter.split(
            "-")[1], vehicle__vehicle_no=vehicle_filter)
        # Amount for all model
        fuel_amount = fuel.all().aggregate(Sum("amount"))["amount__sum"] or 0
        lubricant_amount = lubricant.all().aggregate(Sum("cost"))[
            "cost__sum"] or 0
        tyre_amount = tyre.all().aggregate(Sum("amount"))["amount__sum"] or 0
        battery_amount = battery.all().aggregate(
            Sum("amount"))["amount__sum"] or 0
        repair_amount = repair.all().aggregate(
            Sum("amount"))["amount__sum"] or 0
        sparepart_amount = sparepart.all().aggregate(
            Sum("amount"))["amount__sum"] or 0
        other_amount = other.all().aggregate(Sum("amount"))["amount__sum"] or 0
        # individual amount for taxation
        tax_amount = tax.all().aggregate(Sum("tax_amount"))[
            "tax_amount__sum"] or 0
        insurance_amount = insurance.all().aggregate(Sum("insurance_amount"))[
            "insurance_amount__sum"] or 0
        permit_amount = permit.all().aggregate(Sum("permit_amount"))[
            "permit_amount__sum"] or 0
        emission_amount = emission.all().aggregate(Sum("emission_amount"))[
            "emission_amount__sum"] or 0
        fitness_amount = fitness.all().aggregate(
            Sum("fc_amount"))["fc_amount__sum"] or 0

        total = (fuel_amount + tyre_amount + battery_amount + sparepart_amount + other_amount + repair_amount + lubricant_amount
                 + tax_amount + insurance_amount + permit_amount + emission_amount + fitness_amount)
        # total decimal
        total = round(total, 2)
        # render the invoice
        return render(request, "invoice/invoice.html",
                      {"vehicle": vehicle_filter,
                       "fuel_amount": fuel_amount,
                       "lubricant_amount": lubricant_amount,
                       "tyre_amount": tyre_amount,
                       "repair_amount": repair_amount,
                       "battery_amount": battery_amount,
                       "spare_amount": sparepart_amount,
                       "other_amount": other_amount,
                       "tax_amount": tax_amount,
                       "insurance_amount": insurance_amount,
                       "permit_amount": permit_amount,
                       "emission_amount": emission_amount,
                       "fitness_amount": fitness_amount,
                       "total": total,
                       "sign": sign,
                       "room_name": "broadcast",
                       },)
    else:
        fuel = fuel.all()
        tyre = tyre.all()
        battery = battery.all()
        sparepart = sparepart.all()
        other = other.all()
        repair = repair.all()
        return render(request, "invoice/invoice.html", {
            "fuel": fuel,
            "tyre": tyre,
            "battery": battery,
            "spare": sparepart,
            "other": other,
            "repair": repair,
            "room_name": "broadcast",
        },)



# Invoice for principal
@login_required(login_url="login")
@allowed_users(allowed_roles=["principal"])
def principal_page(request):
    form = SignatureForm(request.POST, request.FILES)
    # get the all the data from the model
    fuel = Fuel.objects.all()
    lubricant = Lubricant.objects.all()
    tyre = Tyre.objects.all()
    battery = Battery.objects.all()
    sparepart = SpareParts.objects.all()
    other = OtherExpense.objects.all()
    repair = Repair.objects.all()
    tax = Tax.objects.all()
    insurance = Insurance.objects.all()
    permit = Permit.objects.all()
    emission = Emission.objects.all()
    fitness = Fitness.objects.all()
    # get total amount
    vehicle_filter = request.POST.get("vehicle")
    month_filter = request.POST.get("month")
    if month_filter and vehicle_filter:
        fuel = fuel.filter(date__month=month_filter.split("-")[1], vehicle__vehicle_no=vehicle_filter)
        lubricant = lubricant.filter(date__month=month_filter.split("-")[1], vehicle__vehicle_no=vehicle_filter)
        tyre = tyre.filter(fitted_date__month=month_filter.split("-")[1], vehicle__vehicle_no=vehicle_filter)
        battery = battery.filter(fitted_date__month=month_filter.split("-")[1], vehicle__vehicle_no=vehicle_filter,)
        repair = repair.filter(date__month=month_filter.split("-")[1], vehicle__vehicle_no=vehicle_filter)
        sparepart = sparepart.filter(spare__date__month=month_filter.split("-")[1], spare__vehicle__vehicle_no=vehicle_filter)
        other = other.filter(other__date__month=month_filter.split("-")[1], other__vehicle__vehicle_no=vehicle_filter)
        tax = tax.filter(tax_from__month=month_filter.split("-")[1], vehicle__vehicle_no=vehicle_filter)
        insurance = insurance.filter(insurance_from__month=month_filter.split("-")[1], vehicle__vehicle_no=vehicle_filter)
        permit = permit.filter(permit_from__month=month_filter.split("-")[1], vehicle__vehicle_no=vehicle_filter)
        emission = emission.filter(emission_from__month=month_filter.split("-")[1], vehicle__vehicle_no=vehicle_filter)
        fitness = fitness.filter(fc_from__month=month_filter.split("-")[1], vehicle__vehicle_no=vehicle_filter)

        # Amount for all model
        fuel_amount = fuel.all().aggregate(Sum("amount"))["amount__sum"] or 0
        lubricant_amount = lubricant.all().aggregate(Sum("cost"))["cost__sum"] or 0
        tyre_amount = tyre.all().aggregate(Sum("amount"))["amount__sum"] or 0
        battery_amount = battery.all().aggregate(Sum("amount"))["amount__sum"] or 0
        repair_amount = repair.all().aggregate(Sum("amount"))["amount__sum"] or 0
        sparepart_amount = sparepart.all().aggregate(Sum("amount"))["amount__sum"] or 0
        other_amount = other.all().aggregate(Sum("amount"))["amount__sum"] or 0
        tax_amount = tax.all().aggregate(Sum("tax_amount"))["tax_amount__sum"] or 0
        insurance_amount = insurance.all().aggregate(Sum("insurance_amount"))["insurance_amount__sum"] or 0
        permit_amount = permit.all().aggregate(Sum("permit_amount"))["permit_amount__sum"] or 0
        emission_amount = emission.all().aggregate(Sum("emission_amount"))["emission_amount__sum"] or 0
        fitness_amount = fitness.all().aggregate(Sum("fc_amount"))["fc_amount__sum"] or 0
        # total amount
        total = (fuel_amount + tyre_amount + battery_amount + sparepart_amount +
                other_amount + repair_amount + lubricant_amount + tax_amount + insurance_amount +
                permit_amount + emission_amount + fitness_amount)
        # total decimal
        total = round(total, 2)
        # render the invoice
        return render(request, "principal/principal.html",
                      {"vehicle": vehicle_filter,
                       "fuel_amount": fuel_amount,
                       "lubricant_amount": lubricant_amount,
                       "tyre_amount": tyre_amount,
                       "repair_amount": repair_amount,
                       "battery_amount": battery_amount,
                       "spare_amount": sparepart_amount,
                       "other_amount": other_amount,
                        "tax_amount": tax_amount,
                        "insurance_amount": insurance_amount,
                        "permit_amount": permit_amount,
                        "emission_amount": emission_amount,
                        "fitness_amount": fitness_amount,
                       "total": total,
                       "form": form,
                       "room_name": "broadcast",
                       },)

    elif request.method == "POST":
        form = SignatureForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            if request.user.is_authenticated:
                instance.user = request.user
                instance.status = True
            instance.save()
            return JsonResponse({'error': False, 'message': 'Signature Uploaded Successfully !'})
        else:
            form = SignatureForm()
        return render(request, "principal/principal.html", {"form": form, "room_name": "broadcast", })

    else:
        fuel = fuel.all()
        tyre = tyre.all()
        battery = battery.all()
        sparepart = sparepart.all()
        other = other.all()
        repair = repair.all()
        lubricant = lubricant.all()
        tax = tax.all()
        insurance = insurance.all()
        permit = permit.all()
        emission = emission.all()
        fitness = fitness.all()
        return render(request, "principal/principal.html", {
            "fuel": fuel,
            "tyre": tyre,
            "battery": battery,
            "spare": sparepart,
            "other": other,
            "repair": repair,
            "lubricant": lubricant,
            "tax": tax,
            "insurance": insurance,
            "permit": permit,
            "emission": emission,
            "fitness": fitness,
            "room_name": "broadcast",
        },)




#new try
