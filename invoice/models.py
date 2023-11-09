from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import MINUTES, PeriodicTask, CrontabSchedule, PeriodicTasks
import datetime
import json

# Create your models here.


class Notify(models.Model):
    message = models.TextField(max_length=500)
    broadcast_on = models.DateTimeField(blank=True, null=True)
    sent = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.message

@receiver(post_save, sender=Notify)
def notify(sender, instance, created, **kwargs):
    if created:
        schedule, created = CrontabSchedule.objects.get_or_create(hour = instance.broadcast_on.hour, minute = instance.broadcast_on.minute, day_of_month = instance.broadcast_on.day, month_of_year = instance.broadcast_on.month)
        task = PeriodicTask.objects.create(crontab=schedule, name=instance.message+str(instance.id), task='invoice.tasks.broadcast_notification',args=json.dumps((instance.id,)))



# Vehicle models
class Vehicle(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="vehicles")
    vehicle_no = models.CharField(max_length=100, blank=False, null=False)
    type = models.CharField(max_length=100, blank=False, null=False,)
    owner_name = models.CharField(max_length=100, blank=False, null=False)

    wheel_base = models.CharField(max_length=100, blank=False, null=False,)
    engine_no = models.CharField(max_length=100, blank=False, null=False,unique=True)
    chasis_no = models.CharField(
        max_length=100, blank=False, null=False, unique=True)
    body_type = models.CharField(max_length=100, blank=False, null=False)
    fuel_type = models.CharField(max_length=100, blank=False, null=False)
    fuel_capacity = models.FloatField(blank=False, null=False)
    make = models.CharField(max_length=100, null=False, blank=False)

    seating_capacity = models.IntegerField(blank=False, null=False)
    unloaden_weight = models.IntegerField(blank=False, null=False)
    loaden_weight = models.IntegerField(blank=False, null=False)

    tyre_size = models.CharField(max_length=100, blank=False, null=False)
    registration_date = models.DateField(blank=False, null=False)
    target_kmpl = models.FloatField(blank=False, null=False, )

    def __str__(self):
        return self.vehicle_no


# Driver Name Model
class Driver(models.Model):
    def upload_to(instance, filename):
        return 'Driver/{0}/{1}'.format(instance.name, filename)
    employee_id = models.CharField(max_length=100, blank=False, null=False)
    name = models.CharField(max_length=100, blank=False, null=False)
    phone_regex = RegexValidator(r'^[0-9]{10}$', 'Phone number must be 10 digits')
    phone = models.CharField(validators=[phone_regex], blank=False, null=False,max_length=10)
    adhar = models.CharField(max_length=12, blank=False, null=False,unique=True)
    pan = models.CharField(max_length=10, blank=True, null=True,unique=True)
    address = models.CharField(max_length=100, blank=False, null=False)
    join_date = models.DateField(blank=False, null=False)
    resign_date = models.DateField(blank=True, null=True)
    dl_no = models.CharField(max_length=100, blank=False, null=False)
    dl_from = models.DateField(blank=False, null=False)
    dl_to = models.DateField(blank=False, null=False)
    document = models.ImageField(upload_to=upload_to, blank=False, null=False)

    def __str__(self):
        return self.name


# staff model
class Staff(models.Model):
    def upload_to(instance, filename):
        return 'Staff/{0}/{1}'.format(instance.name, filename)
    TYPE = (('Mechanic', 'Mechanic'), ('Office Staff',
            'Office Staff'), ('Helper', 'Helper'))
    designation = models.CharField(max_length=100, choices=TYPE, blank=False, null=False)
    employee_id = models.CharField(max_length=100, blank=False, null=False)
    name = models.CharField(max_length=100, blank=False, null=False)
    phone_regex = RegexValidator(r'^[0-9]{10}$', 'Phone number must be 10 digits')
    phone = models.CharField(validators=[phone_regex], blank=False, null=False,max_length=10)
    adhar = models.CharField(max_length=12, blank=False, null=False,unique=True)
    pan = models.CharField(max_length=10, blank=True, null=True,unique=True)
    address = models.CharField(max_length=100, blank=False, null=False)
    join_date = models.DateField(blank=False, null=False)
    resign_date = models.DateField(blank=True, null=True)
    document = models.ImageField(upload_to=upload_to, blank=False, null=False)

    def __str__(self):
        return self.name


# Logsheet Model
class Log(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    date_time = models.DateTimeField(
        default=timezone.now, blank=True, null=True)

    @property
    def doeking_km(self):
        if Logsheet.objects.filter(log=self).exists():
            return Logsheet.objects.filter(log=self).last().doeking_km
        elif Logsheet.objects.filter(log=self) == None:
            return 0
        else:
            return 0

    @property
    def daily_km(self):
        return Logsheet.objects.filter(log=self).aggregate(Sum('daily_km'))['daily_km__sum']

    @property
    def total_km(self):
        if Logsheet.objects.filter(log=self).exists():
            return Logsheet.objects.filter(log=self).last().doeking_km
        
        elif Logsheet.objects.filter(log__vehicle=self.vehicle) == None:
            return 0
        
        else:
            return 0

    
    @property
    def total_trip(self):
        return Logsheet.objects.filter(log=self).count()
    

    
    

    def __str__(self):
        return self.vehicle.vehicle_no


# Logsheet Details Model
class Logsheet(models.Model):
    log = models.ForeignKey(
        Log, on_delete=models.CASCADE, related_name="logsheets")
    driver = models.ForeignKey(
        Driver, on_delete=models.CASCADE, blank=True, null=True)
    trip = models.IntegerField(blank=False, null=False)
    distance_from = models.FloatField(blank=True, null=True, )
    distance_to = models.FloatField(blank=True, null=True, )
    time_from = models.TimeField(blank=False, null=False, default=timezone.now)
    time_to = models.TimeField(blank=False, null=False, default=timezone.now)
    source = models.CharField(max_length=100, blank=True, null=True)
    destination = models.CharField(max_length=100, blank=True, null=True)
    daily_km = models.FloatField(blank=True, null=True,)
    doeking_km = models.FloatField(blank=True, null=True,)

    def save(self, *args, **kwargs):
        self.daily_km = int(float(self.distance_to)) - \
            int(float(self.distance_from))
        previous_day = Logsheet.objects.filter(
            log__vehicle=self.log.vehicle).order_by('-id').first()
        if previous_day:
            self.doeking_km = int(
                float(previous_day.distance_to)) + self.daily_km
        else:
            self.doeking_km = self.daily_km
        super(Logsheet, self).save(*args, **kwargs)

    def __str__(self):
        return self.log.vehicle.vehicle_no + " " + str(self.log.date_time.date()) + " " + str(self.trip)


# Fuel Model
class Fuel(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="fuels")
    fuel_type = models.CharField(max_length=100, blank=False, null=False)
    vendor_name = models.CharField(max_length=200, blank=True, null=True)
    indent_no = models.IntegerField(blank=True, null=True)
    quantity = models.FloatField(blank=False, null=False)
    bill_no = models.CharField(max_length=200, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True, )
    previous_km = models.FloatField(blank=False, null=False, )
    progressive_km = models.FloatField(blank=True, null=True, )
    date = models.DateField(blank=False, null=False)

    def save(self, *args, **kwargs):
        if self.progressive_km == None:
            self.progressive_km = 0
        super(Fuel, self).save(*args, **kwargs)

    @property
    def total_km(self):
        if Logsheet.objects.filter(log__vehicle=self.vehicle).exists():
            return Logsheet.objects.filter(log__vehicle=self.vehicle).last().doeking_km
        
        elif Logsheet.objects.filter(log__vehicle=self.vehicle) == None:
            return 0
        
        else:
            return 0
        

    @property
    def actual_km(self):
        return self.progressive_km - self.previous_km

    @property
    def kmpl(self):
        res = self.actual_km / self.quantity
        return '{:.2f}'.format(res)

    def __str__(self):
        return self.vehicle.vehicle_no + " " + str(self.date)


# oil changes
class Lubricant(models.Model):
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name="lubricants")
    oil_type = models.CharField(max_length=100, blank=False, null=False)
    supplier_name = models.CharField(max_length=200, blank=False, null=False)
    bill_no = models.CharField(max_length=200, blank=True, null=True)
    grade = models.CharField(max_length=200, blank=False, null=False)
    quantity = models.FloatField(blank=False, null=False)
    cost = models.FloatField(blank=False, null=False, )
    previous_km = models.FloatField(blank=False, null=False, )
    progressive_km = models.FloatField(blank=True, null=True, )
    date = models.DateField(blank=False, null=False)

    @property
    def total_km(self):
        if Logsheet.objects.filter(log__vehicle=self.vehicle).exists():
            return Logsheet.objects.filter(log__vehicle=self.vehicle).last().doeking_km
        
        elif Logsheet.objects.filter(log__vehicle=self.vehicle) == None:
            return 0
        
        else:
            return 0

    @property
    def doeking_km(self):
        if Logsheet.objects.filter(log__vehicle=self.vehicle).exists():
            return Logsheet.objects.filter(log__vehicle=self.vehicle).last().doeking_km
        elif Logsheet.objects.filter(log__vehicle=self.vehicle) == None:
            return 0
        else:
            return 0

    @property
    def actual_km(self):
        return self.progressive_km - self.previous_km

    @property
    def kmpl(self):
        res = self.actual_km / self.quantity
        return '{:.2f}'.format(res)

    def __str__(self):
        return self.vehicle.vehicle_no + " " + str(self.date)


# Tyre Model
class Tyre(models.Model):
    def file_upload(self, filename):
        return 'tyre/{0}/{1}'.format(self.vehicle.vehicle_no, filename)
    VERSION = (('New', 'New'), ('Rebelt', 'Rebelt'))
    SCRAP = (('Yes', 'Yes'), ('No', 'No'))
    POSITION = (
        ("RH", "Front Right"),
        ("LH", "Front Left"),
        ("ORI", "Off Rear Inner"),
        ("ORO", "Off Rear Outer"),
        ("NRI", "Nor Rear Inner"),
        ("NRO", "Nor Rear Outer"),
    )
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name="tyres")
    version = models.CharField(
        max_length=100, choices=VERSION, blank=False, null=False)
    position = models.CharField(
        max_length=10, choices=POSITION, blank=False, null=False)
    scrap = models.CharField(
        max_length=100, choices=SCRAP, blank=True, null=True)

    tyre_no = models.CharField(max_length=100, blank=False, null=False)
    rebelt_no = models.CharField(max_length=100, blank=True, null=True)
    tyre_type = models.CharField(max_length=100, blank=True, null=True)

    make = models.CharField(max_length=100, blank=False, null=False)
    size = models.CharField(max_length=100, blank=False, null=False)
    vendor_name = models.CharField(max_length=100, blank=False, null=False)
    amount = models.FloatField(blank=False, null=False, )
    bill_no = models.CharField(max_length=100, blank=True, null=True)
    cause_of_removal = models.TextField(blank=True, null=True)

    fitted_km = models.FloatField(blank=False, null=False,)
    fitted_date = models.DateField(blank=False, null=False,)
    removal_km = models.FloatField(blank=True, null=True, )
    removal_date = models.DateField(blank=True, null=True, default=timezone.now)
    documents = models.FileField(upload_to=file_upload, blank=True, null=True)
    actual_km = models.FloatField(blank=True, null=True, )

    def save(self, *args, **kwargs):
        if self.version == 'New':
            self.rebelt_no = 0
        super(Tyre, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.tyre_no)


# Battery Model
class Battery(models.Model):
    TYPE = (('New', 'New'), ('InterChange', 'InterChange'))
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name="batteries")
    type = models.CharField(max_length=100, choices=TYPE,
                            blank=False, null=False)
    battery_no = models.CharField(max_length=100, blank=False, null=False)
    vendor_name = models.CharField(max_length=100, blank=False, null=False)
    make = models.CharField(max_length=100, blank=False, null=False)
    amount = models.FloatField(blank=False, null=False, )
    cause_of_removal = models.TextField(blank=True, null=True)
    bill_no = models.CharField(max_length=100, blank=True, null=True)

    fitted_km = models.FloatField(blank=False, null=False, )
    fitted_date = models.DateField(blank=False, null=False,)
    removal_km = models.FloatField(blank=True, null=True, )
    removal_date = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.removal_km == '':
            return 0.0
        elif self.removal_date == '':
            return datetime.date.today()
        super(Battery, self).save(*args, **kwargs)

    @property
    def actual_km(self):
        if self.removal_km == None:
            return 0
        else:
            return self.removal_km - self.fitted_km

    @property
    def battery_worked_days(self):
        if self.removal_date == None:
            return 0
        else:
            return (self.removal_date - self.fitted_date).days

    def __str__(self):
        return self.battery_no


# Tax Model
class Tax(models.Model):
    def get_upload_path(instance, filename): return 'documents/{0}/{1}'.format(instance.vehicle.vehicle_no, filename)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="taxes")
    tax_no = models.CharField(max_length=100, blank=False, null=False ,unique=True)
    tax_amount = models.FloatField(blank=False, null=False, )
    tax_from = models.DateField(blank=False, null=False)
    tax_to = models.DateField(blank=False, null=False)
    expire_time = models.TimeField(blank=True, null=True,auto_now=True,editable=True)
    tax_document = models.FileField(upload_to=get_upload_path, blank=True, null=True)

    def __str__(self):
        return self.tax_no + " " + str(self.expire_time)

@receiver(post_save, sender=Tax)
def create_notify(sender, instance, created, **kwargs):
    if created:
        if (instance.tax_to <= datetime.date.today()):
            current_date = datetime.datetime.now()
            current_time = current_date.time().strftime("%H:%M:%S")
            ahead_time = datetime.datetime.strptime(current_time, "%H:%M:%S") + datetime.timedelta(minutes=1)
            #notify model create
            Notify.objects.create(
            message="Taxation of {0} is due for {1}.".format(instance.vehicle.vehicle_no,instance.tax_to),
            broadcast_on = datetime.datetime.combine(current_date, ahead_time.time()),
            sent = False,
        )
        else:
            date = instance.tax_to - datetime.timedelta(days=15)
            if (date <= datetime.date.today()):
                current_date = datetime.datetime.now()
                current_time = current_date.time().strftime("%H:%M:%S")
                ahead_time = datetime.datetime.strptime(current_time, "%H:%M:%S") + datetime.timedelta(minutes=1)
                #notify model create
                Notify.objects.create(
                message="Taxation of {0} is due for {1}.".format(instance.vehicle.vehicle_no,instance.tax_to),
                broadcast_on = datetime.datetime.combine(current_date, ahead_time.time()),
                sent = False,
            )
            else:
                time = instance.expire_time
                Notify.objects.create(
                message="Taxation of {0} will expire {1}.".format(instance.vehicle.vehicle_no,instance.tax_to),
                broadcast_on = datetime.datetime.combine(date, time),
                sent = False,
            )



# Insurance Model
class Insurance(models.Model):
    def get_upload_path(instance, filename): return 'documents/{0}/{1}'.format(instance.vehicle.vehicle_no, filename)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="insurances")
    company_name = models.CharField(max_length=100, blank=False, null=False)
    insurance_no = models.CharField(max_length=100, blank=False, null=False, unique=True)
    insurance_amount = models.FloatField(blank=False, null=False, )
    insurance_from = models.DateField(blank=False, null=False)
    insurance_to = models.DateField(blank=True, null=True)
    expire_time = models.TimeField(blank=True, null=True,auto_now=True,editable=True)
    insurance_document = models.FileField(upload_to=get_upload_path, blank=True, null=True)

    def __str__(self):
        return self.insurance_no


@receiver(post_save, sender=Insurance)
def create_notify(sender, instance, created, **kwargs):
    if created:
        if (instance.insurance_to <= datetime.date.today()):
            current_date = datetime.datetime.now()
            current_time = current_date.time().strftime("%H:%M:%S")
            ahead_time = datetime.datetime.strptime(current_time, "%H:%M:%S") + datetime.timedelta(minutes=1)
            #notify model create
            Notify.objects.create(
            message="Insurance of {0} is due for {1}.".format(instance.vehicle.vehicle_no,instance.insurance_to),
            broadcast_on = datetime.datetime.combine(current_date, ahead_time.time()),
            sent = False,
        )
        else:
            date = instance.insurance_to - datetime.timedelta(days=15)
            print(date)
            if (date <= datetime.date.today()):
                current_date = datetime.datetime.now()
                current_time = current_date.time().strftime("%H:%M:%S")
                ahead_time = datetime.datetime.strptime(current_time, "%H:%M:%S") + datetime.timedelta(minutes=1)
                #notify model create
                Notify.objects.create(
                message="Insurance of {0} is due for {1}.".format(instance.vehicle.vehicle_no,instance.insurance_to),
                broadcast_on = datetime.datetime.combine(current_date, ahead_time.time()),
                sent = False,
            )
            else:
                time = instance.expire_time
                Notify.objects.create(
                message="Insurance of {0} will expire {1}.".format(instance.vehicle.vehicle_no,instance.insurance_to),
                broadcast_on = datetime.datetime.combine(date, time),
                sent = False,
            )
 



# Fitness certificate Model
class Fitness(models.Model):
    def get_upload_path(instance, filename): return 'documents/{0}/{1}'.format(instance.vehicle.vehicle_no, filename)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="fitness_objs")
    fc_no = models.CharField(max_length=100, blank=False, null=False, unique=True)
    fc_amount = models.FloatField(blank=False, null=False, )
    fc_from = models.DateField(blank=False, null=False)
    fc_to = models.DateField(blank=True, null=True)
    expire_time = models.TimeField(blank=True, null=True,auto_now=True,editable=True)
    fc_document = models.FileField(upload_to=get_upload_path, blank=True, null=True)

    def __str__(self):
        return self.fc_no


@receiver(post_save, sender=Fitness)
def create_notify(sender, instance, created, **kwargs):
    if created:
        if (instance.fc_to <= datetime.date.today()):
            current_date = datetime.datetime.now()
            current_time = current_date.time().strftime("%H:%M:%S")
            ahead_time = datetime.datetime.strptime(current_time, "%H:%M:%S") + datetime.timedelta(minutes=1)
            #notify model create
            Notify.objects.create(
            message="Fitness certificate of {0} is due for {1}.".format(instance.vehicle.vehicle_no,instance.fc_to),
            broadcast_on = datetime.datetime.combine(current_date, ahead_time.time()),
            sent = False,
        )
        else:
            date = instance.fc_to - datetime.timedelta(days=15)
            if (date <= datetime.date.today()):
                current_date = datetime.datetime.now()
                current_time = current_date.time().strftime("%H:%M:%S")
                ahead_time = datetime.datetime.strptime(current_time, "%H:%M:%S") + datetime.timedelta(minutes=1)
                #notify model create
                Notify.objects.create(
                message="Fitness certificate of {0} is due for {1}.".format(instance.vehicle.vehicle_no,instance.fc_to),
                broadcast_on = datetime.datetime.combine(current_date, ahead_time.time()),
                sent = False,
            )
            else:
                time = instance.expire_time
                Notify.objects.create(
                message="Fitness certificate of {0} will expire {1}.".format(instance.vehicle.vehicle_no,instance.fc_to),
                broadcast_on = datetime.datetime.combine(date, time),
                sent = False,
            )



# permit Model
class Permit(models.Model):
    def get_upload_path(instance, filename): return 'documents/{0}/{1}'.format(instance.vehicle.vehicle_no, filename)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="permits")
    permit_no = models.CharField(max_length=100, blank=False, null=False, unique=True)
    permit_amount = models.FloatField(blank=False, null=False, )
    permit_from = models.DateField(blank=False, null=False)
    permit_to = models.DateField(blank=True, null=True)
    expire_time = models.TimeField(blank=True, null=True,auto_now=True,editable=True)
    permit_document = models.FileField(upload_to=get_upload_path, blank=True, null=True)

    def __str__(self):
        return self.permit_no


@receiver(post_save, sender=Permit)
def create_notify(sender, instance, created, **kwargs):
    if created:
        if (instance.permit_to <= datetime.date.today()):
            current_date = datetime.datetime.now()
            current_time = current_date.time().strftime("%H:%M:%S")
            ahead_time = datetime.datetime.strptime(current_time, "%H:%M:%S") + datetime.timedelta(minutes=1)
            #notify model create
            Notify.objects.create(
            message="Permit of {0} is due for {1}.".format(instance.vehicle.vehicle_no,instance.permit_to),
            broadcast_on = datetime.datetime.combine(current_date, ahead_time.time()),
            sent = False,
        )
        else:
            date = instance.permit_to - datetime.timedelta(days=15)
            if (date <= datetime.date.today()):
                current_date = datetime.datetime.now()
                current_time = current_date.time().strftime("%H:%M:%S")
                ahead_time = datetime.datetime.strptime(current_time, "%H:%M:%S") + datetime.timedelta(minutes=1)
                #notify model create
                Notify.objects.create(
                message="Permit of {0} is due for {1}.".format(instance.vehicle.vehicle_no,instance.permit_to),
                broadcast_on = datetime.datetime.combine(current_date, ahead_time.time()),
                sent = False,
            )
            else:
                time = instance.expire_time
                Notify.objects.create(
                message="Permit of {0} will expire {1}.".format(instance.vehicle.vehicle_no,instance.permit_to),
                broadcast_on = datetime.datetime.combine(date, time),
                sent = False,
            )


# Emmision certificate Model
class Emission(models.Model):
    def get_upload_path(instance, filename): return 'documents/{0}/{1}'.format(instance.vehicle.vehicle_no, filename)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="emissions")
    emission_no = models.CharField(max_length=100, blank=False, null=False, unique=True)
    emission_amount = models.FloatField(blank=False, null=False)
    emission_from = models.DateField(blank=False, null=False)
    emission_to = models.DateField(blank=True, null=True)
    expire_time = models.TimeField(blank=True, null=True,auto_now=True,editable=True)
    emission_document = models.FileField(upload_to=get_upload_path, blank=True, null=True)

    def __str__(self):
        return self.emission_no


@receiver(post_save, sender=Emission)
def create_notify(sender, instance, created, **kwargs):
    if created:
        if (instance.emission_to <= datetime.date.today()):
            current_date = datetime.datetime.now()
            current_time = current_date.time().strftime("%H:%M:%S")
            ahead_time = datetime.datetime.strptime(current_time, "%H:%M:%S") + datetime.timedelta(minutes=1)
            #notify model create
            Notify.objects.create(
            message="Emission certificate of {0} is due for {1}.".format(instance.vehicle.vehicle_no,instance.emission_to),
            broadcast_on = datetime.datetime.combine(current_date, ahead_time.time()),
            sent = False,
        )
        else:
            date = instance.emission_to - datetime.timedelta(days=15)
            if (date <= datetime.date.today()):
                current_date = datetime.datetime.now()
                current_time = current_date.time().strftime("%H:%M:%S")
                ahead_time = datetime.datetime.strptime(current_time, "%H:%M:%S") + datetime.timedelta(minutes=1)
                #notify model create
                Notify.objects.create(
                message="Emission certificate of {0} is due for {1}.".format(instance.vehicle.vehicle_no,instance.emission_to),
                broadcast_on = datetime.datetime.combine(current_date, ahead_time.time()),
                sent = False,
            )
            else:
                time = instance.expire_time
                Notify.objects.create(
                message="Emission certificate of {0} will expire {1}.".format(instance.vehicle.vehicle_no,instance.emission_to),
                broadcast_on = datetime.datetime.combine(date, time),
                sent = False,
            )


# Major Repair Model
class Repair(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="repairs")
    repair_type = models.CharField(max_length=100, blank=False, null=False)
    vendor_name = models.CharField(max_length=100, blank=False, null=False)
    bill_no = models.CharField(max_length=100, blank=True, null=True)
    amount = models.FloatField(blank=False, null=False, )
    date = models.DateField(blank=False, null=False)
    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.vehicle.vehicle_no


# Spare Model
class Spare(models.Model):
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name='spares')
    vendor_name = models.CharField(max_length=100, blank=True, null=True)
    bill_no = models.CharField(max_length=100, blank=True, null=True)
    cause_of_removal = models.TextField(blank=True, null=True)
    oval = models.TextField(blank=True, null=True)
    date = models.DateField(blank=False, null=False)
    token_no = models.CharField(max_length=100, blank=True, null=True)

    @property
    def total(self):
        total_value = self.spare_parts.all().aggregate(Sum("amount"))[
            "amount__sum"] or 0
        return total_value

    def __str__(self):
        return self.vehicle.vehicle_no


class SpareParts(models.Model):
    spare = models.ForeignKey(Spare, on_delete=models.CASCADE, related_name="spare_parts")
    sl_no = models.CharField(max_length=100, blank=False, null=False)
    product_name = models.CharField(max_length=100, blank=False, null=False)
    quantity = models.IntegerField(blank=False, null=False)
    cost = models.FloatField(blank=False, null=False, )
    amount = models.FloatField(blank=False, null=False, )

    @property
    def sparepart_amount(self):
        return self.quantity * self.cost

    def __str__(self):
        return self.product_name


# Other Expenses Model
class Other(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=100, blank=True, null=True)
    bill_no = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(blank=False, null=False)

    @property
    def total(self):
        total_value = self.other_expenses.all().aggregate(Sum("amount"))["amount__sum"] or 0
        return total_value


class OtherExpense(models.Model):
    other = models.ForeignKey(
        Other, on_delete=models.CASCADE, related_name="other_expenses")
    sl_no = models.CharField(max_length=100, blank=False, null=False)
    product_name = models.CharField(max_length=100, blank=False, null=False)
    quantity = models.IntegerField(blank=False, null=False)
    cost = models.FloatField(blank=False, null=False, )
    amount = models.FloatField(blank=False, null=False, )

    @property
    def other_amount(self):
        return self.quantity * self.cost

    def __str__(self) -> str:
        return self.product_name


# Scrap models
class Scrap(models.Model):
    def get_upload_path(instance, filename): return 'scrap/{0}/{1}'.format(instance.vehicle.vehicle_no, filename)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=100, blank=True, null=True)
    bill_no = models.CharField(max_length=100, blank=False, null=False)
    cause_of_scrap = models.TextField(blank=False, null=False)
    amount = models.FloatField(blank=False, null=False, )
    date = models.DateField(blank=False, null=False)
    document = models.FileField(
        upload_to=get_upload_path, blank=True, null=True)

    def __str__(self):
        return self.vehicle.vehicle_no
    

    @property
    def total(self):
        return Scrap.objects.filter(vehicle=self.vehicle).aggregate(Sum("amount"))["amount__sum"] or 0
    


# Student Model
class Student(models.Model):
    def get_upload_path(
        instance, filename): return 'student/{0}/{1}'.format(instance.name, filename)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False, null=False)
    usn = models.CharField(max_length=100, blank=False, null=False)
    bus_name = models.CharField(max_length=100, blank=False, null=False)

    address = models.CharField(max_length=100, blank=False, null=False)
    phone_regex = RegexValidator(r'^[0-9]{10}$', 'Phone number must be 10 digits')
    contact = models.CharField(validators=[phone_regex], max_length=10, blank=False, null=False)
    semester = models.CharField(max_length=100, blank=False, null=False)
    department = models.CharField(max_length=100, blank=False, null=False)
    destination = models.CharField(max_length=100, blank=False, null=False)
    route_code = models.CharField(max_length=100, blank=False, null=False)

    total_amount = models.FloatField(blank=False, null=False, )
    paid_amount = models.FloatField(blank=True, null=True, )
    
    enroll_date = models.DateField(blank=False, null=False)
    releaving_date = models.DateField(blank=True, null=True)
    document = models.FileField(upload_to=get_upload_path, blank=False, null=False)

    @property
    def due_amount(self):
        return self.total_amount - self.paid_amount

    def __str__(self):
        return self.name


# faculty
class Faculty(models.Model):
    def get_upload_path(instance, filename):
        return 'faculty/{0}/{1}'.format(instance.name, filename)

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    bus_name = models.CharField(max_length=100, blank=False, null=False)
    name = models.CharField(max_length=100, blank=False, null=False)
    phone_regex = RegexValidator(r'^[0-9]{10}$', 'Phone number must be 10 digits')
    contact = models.CharField(validators=[phone_regex], max_length=10, blank=False, null=False)
    address = models.CharField(max_length=100, blank=False, null=False)
    department = models.CharField(max_length=100, blank=False, null=False)
    route_code = models.CharField(max_length=100, blank=False, null=False)
    destination = models.CharField(max_length=100, blank=False, null=False)
    document = models.FileField(
        upload_to=get_upload_path, blank=True, null=True)

    def __str__(self):
        return self.name


# Principal Signatures Model
class Signature(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    signature = models.ImageField(upload_to='signature/', null=True)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return self.user.username
