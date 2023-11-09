from django import forms
from invoice.models import *
from accounts.models import *
from django.forms import ClearableFileInput
from django.contrib.admin import widgets 

class DateInput(forms.DateInput):
    input_type = "date"


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = "__all__"
        exclude = ["user"]
        error_messages = {
        'vehicle_no': {'required': 'Please enter vehicle number', 'unique': 'Vehicle number already exists'},
        'engine_no': {'required': 'Please enter engine number', 'unique': 'Engine number already exists'},
        'chasis_no': {'required': 'Please enter chasis number', 'unique': 'Chasis number already exists'},
        }
        widgets = {
            "user": forms.HiddenInput(),
            "vehicle_no": forms.TextInput(attrs={"class": "form-control",}),
            "type": forms.TextInput(attrs={"class": "form-control",}),
            "owner_name": forms.TextInput(attrs={"class": "form-control",}),
            "wheel_base": forms.TextInput(attrs={"class": "form-control",}),
            
            "engine_no": forms.TextInput(attrs={"class": "form-control", }),
            "chasis_no": forms.TextInput(attrs={"class": "form-control",}),
            "body_type": forms.TextInput(attrs={"class": "form-control",}),
            "fuel_type": forms.TextInput(attrs={"class": "form-control",}),
            "fuel_capacity": forms.widgets.NumberInput(attrs={"class": "form-control", }),
            'make': forms.TextInput(attrs={"class": "form-control", }),
            
            "seating_capacity" : forms.NumberInput(attrs={"class": "form-control",}),
            "unloaden_weight": forms.NumberInput(attrs={"class": "form-control",}),
            "loaden_weight": forms.NumberInput(attrs={"class": "form-control",}),

            "tyre_size": forms.TextInput(attrs={"class": "form-control", }),
            "target_kmpl": forms.widgets.NumberInput(attrs={"class": "form-control", }),
            "registration_date": DateInput(attrs={"class": "form-control",}),
        }


# Driver form
class DriverForm(forms.ModelForm):
    # document = forms.FileField(widget=forms.ClearableFileInput(attrs={"class": "form-control","name": "document", 'multiple': True}))
    class Meta:
        model = Driver
        fields = "__all__"
        widgets = {
           'employee_id': forms.TextInput(attrs={"class": "form-control","employee_id":"employee_id" }),
           'name': forms.TextInput(attrs={"class": "form-control","name": "name", }),
           'phone': forms.TextInput(attrs={"class": "form-control","name": "phone", }),
           'adhar': forms.TextInput(attrs={"class": "form-control", "name": "adhar" }),
           'pan': forms.TextInput(attrs={"class": "form-control", "name": "pan" }),
           'address': forms.TextInput(attrs={"class": "form-control","name": "address" }),
           'join_date': DateInput(attrs={"class": "form-control","name": "join_date"  }),
           'resign_date': DateInput(attrs={"class": "form-control","name": "resign_date"  }),
           'dl_no': forms.TextInput(attrs={"class": "form-control","name": "dl_no"  }),
           'dl_from':DateInput(attrs={"class": "form-control","name": "dl_from" }),
           'dl_to':DateInput(attrs={"class": "form-control","name": "dl_to" }),
           'document': forms.FileInput(attrs={"class": "form-control", "name": "document", 'multiple': True , "required": True}),
        }

class UpdateDriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = "__all__"
        widgets = {
           'employee_id': forms.TextInput(attrs={"class": "form-control","employee_id":"employee_id",'readonly': 'readonly' }),
           'name': forms.TextInput(attrs={"class": "form-control","name": "name", 'readonly': 'readonly' }),
           'phone': forms.TextInput(attrs={"class": "form-control","name": "phone",'readonly': 'readonly' }),
           'adhar': forms.TextInput(attrs={"class": "form-control", "name": "adhar",'readonly': 'readonly'}),
           'pan': forms.TextInput(attrs={"class": "form-control", "name": "pan",'readonly': 'readonly' }),
           'address': forms.TextInput(attrs={"class": "form-control","name": "address",'readonly': 'readonly' }),
           'join_date': DateInput(attrs={"class": "form-control","name": "join_date",'readonly': 'readonly'  }),
           'resign_date': DateInput(attrs={"class": "form-control","name": "resign_date",}),
           'dl_no': forms.TextInput(attrs={"class": "form-control","name": "dl_no",'readonly': 'readonly'  }),
           'dl_from':DateInput(attrs={"class": "form-control","name": "dl_from",'readonly': 'readonly' }),
           'dl_to':DateInput(attrs={"class": "form-control","name": "dl_to",'readonly': 'readonly' }),
           'document': forms.FileInput(attrs={"class": "form-control", "name": "document", 'multiple': True,'readonly':'readonly' ,"disabled":True}),
        }



# Staff Form
class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = "__all__"
        widgets = {
            'designation': forms.Select(attrs={"class": "form-control","name": "designation", }),
            'employee_id': forms.TextInput(attrs={"class": "form-control","employee_id":"employee_id" }),
            'name': forms.TextInput(attrs={"class": "form-control","name": "name",}),
            'phone': forms.TextInput(attrs={"class": "form-control","name": "phone", }),
            'adhar': forms.TextInput(attrs={"class": "form-control","name": "adhar",}),
            'pan': forms.TextInput(attrs={"class": "form-control","name": "pan",}),
            
            'address': forms.TextInput(attrs={"class": "form-control","name": "address", }),
            'join_date': DateInput(attrs={"class": "form-control","name": "join_date", }),
            'resign_date': DateInput(attrs={"class": "form-control","name": "resign_date", }),
            'document': forms.FileInput(attrs={"class": "form-control", "name": "document", 'multiple': True }),
        }

class UpdateStaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = "__all__"
        widgets = {
            'designation': forms.Select(attrs={"class": "form-control","name": "designation", 'readonly':'readonly'}),
            'employee_id': forms.TextInput(attrs={"class": "form-control","employee_id":"employee_id",'readonly':'readonly' }),
            'name': forms.TextInput(attrs={"class": "form-control","name": "name",'readonly':'readonly'}),
            'phone': forms.TextInput(attrs={"class": "form-control","name": "phone",'readonly':'readonly' }),
            'adhar': forms.TextInput(attrs={"class": "form-control","name": "adhar", 'readonly':'readonly'}),
            'pan': forms.TextInput(attrs={"class": "form-control","name": "pan",'readonly':'readonly'}),
            'address': forms.TextInput(attrs={"class": "form-control","name": "address",'readonly':'readonly' }),
            'join_date': DateInput(attrs={"class": "form-control","name": "join_date",'readonly':'readonly' }),
            'resign_date': DateInput(attrs={"class": "form-control","name": "resign_date", }),
            'document': forms.FileInput(attrs={"class": "form-control", "name": "document", 'multiple': True,'readonly':'readonly' ,"disabled":True}),
        }


# Taxation Form
class TaxationForm(forms.ModelForm):
    class Meta:
        model = Tax
        fields = "__all__"
        widgets = {
            'vehicle': forms.Select(attrs={"class": "form-control","name": "vehicle", }),
            'tax_no': forms.TextInput(attrs={"class": "form-control","name": "tax_no", }),
            'tax_amount': forms.widgets.NumberInput(attrs={"class": "form-control", "name": "tax_amount", }),
            'tax_from': DateInput(attrs={"class": "form-control","name": "tax_from", }),
            'tax_to': DateInput(attrs={"class": "form-control","name": "tax_to", }),
            'tax_document': forms.FileInput(attrs={"class": "form-control", "name": "tax_document", 'multiple': True }),
        }

        
# Insurance Form       
class InsuranceForm(forms.ModelForm):
    class Meta:
        model = Insurance
        fields = "__all__"
        error_messages = {'insurance_no': {'required': 'Insurance Number is required','unique':'Insurance number already exist'},}
        widgets = {
            'vehicle': forms.Select(attrs={"class": "form-control","name": "vehicle", }),
            'insurance_no': forms.TextInput(attrs={"class": "form-control","name": "insurance_no", }),
            'company_name': forms.TextInput(attrs={"class": "form-control","name": "company_name", }),
            'insurance_amount': forms.widgets.NumberInput(attrs={"class": "form-control", "name": "insurance_amount", }),
            'insurance_from': DateInput(attrs={"class": "form-control","name": "insurance_from", }),
            'insurance_to': DateInput(attrs={"class": "form-control","name": "insurance_to", }),
            'insurance_document': forms.FileInput(attrs={"class": "form-control", "name": "insurance_document", 'multiple': True }),
        }
      

# Permit Form      
class PermitForm(forms.ModelForm):
    class Meta:
        model = Permit
        fields = "__all__"
        widgets = {
            'vehicle': forms.Select(attrs={"class": "form-control","name": "vehicle", }),
            'permit_no': forms.TextInput(attrs={"class": "form-control","name": "permit_no", }),
            'permit_amount': forms.widgets.NumberInput(attrs={"class": "form-control", "name": "permit_amount", }),
            'permit_from': DateInput(attrs={"class": "form-control","name": "permit_from", }),
            'permit_to': DateInput(attrs={"class": "form-control","name": "permit_to", }),
            'permit_document': forms.FileInput(attrs={"class": "form-control", "name": "permit_document", 'multiple': True }),
        }

        
# Emission Form
class EmissionForm(forms.ModelForm):
    class Meta:
        model = Emission
        fields = "__all__"
        widgets = {
            'vehicle': forms.Select(attrs={"class": "form-control","name": "vehicle", }),
            'emission_no': forms.TextInput(attrs={"class": "form-control","name": "emission_no", }),
            'emission_amount': forms.widgets.NumberInput(attrs={"class": "form-control", "name": "emission_amount", }),
            'emission_from': DateInput(attrs={"class": "form-control","name": "emission_from", }),
            'emission_to': DateInput(attrs={"class": "form-control","name": "emission_to", }),
            'emission_document': forms.FileInput(attrs={"class": "form-control", "name": "emission_document", 'multiple': True }),
        }
    

# Fitness Form
class FitnessForm(forms.ModelForm):
    class Meta:
        model = Fitness
        fields = "__all__"
        widgets = {
            'vehicle': forms.Select(attrs={"class": "form-control","name": "vehicle", }),
            'fc_no': forms.TextInput(attrs={"class": "form-control","name": "fitness_no", }),
            'fc_amount': forms.widgets.NumberInput(attrs={"class": "form-control", "name": "fitness_amount", }),
            'fc_from': DateInput(attrs={"class": "form-control","name": "fitness_from", }),
            'fc_to': DateInput(attrs={"class": "form-control","name": "fitness_to", }),
            'fc_document': forms.FileInput(attrs={"class": "form-control", "name": "fitness_document", 'multiple': True }),
        }


# Repair form
class RepairForm(forms.ModelForm):
    class Meta:
        model = Repair
        fields = "__all__"
        widgets = {
            'vehicle': forms.Select(attrs={"class": "form-control", }),
            'repair_type': forms.TextInput(attrs={"class": "form-control", }),
            'vendor_name': forms.TextInput(attrs={"class": "form-control", }),
            'bill_no': forms.TextInput(attrs={"class": "form-control", }),
            'amount': forms.widgets.NumberInput(attrs={"class": "form-control", }),
            'reason': forms.Textarea(attrs={"class": "form-control","style": "height: 93px; width: 100%;" ,}),
            'date': DateInput(attrs={"class": "form-control", }),
        }
            
  
# scrap form
class ScrapForm(forms.ModelForm):
    class Meta:
        model = Scrap
        fields = "__all__"
        widgets = {
            'vehicle': forms.Select(attrs={"class": "form-control", "required":True }),
            'vendor_name': forms.TextInput(attrs={"class": "form-control", "required":True }),
            'bill_no': forms.TextInput(attrs={"class": "form-control", "required":True}),
            'cause_of_scrap': forms.Textarea(attrs={"class": "form-control","style": "height: 93px; width: 100%;","required":True}),
            'amount': forms.widgets.NumberInput(attrs={"class": "form-control", "required":True }),
            'date': DateInput(attrs={"class": "form-control", "required":True}),
            'document' : forms.FileInput(attrs={"class": "form-control","required":True,"multiple": True}),
        }

                
# student form
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"
        widgets = {
            'vehicle': forms.Select(attrs={"class": "form-control", }),
            'name': forms.TextInput(attrs={"class": "form-control", }),
            'usn': forms.TextInput(attrs={"class": "form-control", }),
            'bus_name': forms.TextInput(attrs={"class": "form-control", }),
            
            'address': forms.TextInput(attrs={"class": "form-control", }),
            'contact': forms.TextInput(attrs={"class": "form-control", }),
            'semester': forms.TextInput(attrs={"class": "form-control", }),
            'department': forms.TextInput(attrs={"class": "form-control", }),
            'destination': forms.TextInput(attrs={"class": "form-control", }),
            
            'route_code': forms.TextInput(attrs={"class": "form-control", }),
            'enroll_date': DateInput(attrs={"class": "form-control", }),
            'releaving_date': DateInput(attrs={"class": "form-control", }),
            
            'total_amount': forms.widgets.NumberInput(attrs={"class": "form-control", }),
            'paid_amount': forms.widgets.NumberInput(attrs={"class": "form-control", }),
            'document' : forms.FileInput(attrs={"class": "form-control","multiple": True, "required":True}),
        }


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"
        widgets = {
            'vehicle': forms.Select(attrs={"class": "form-control", "readonly":"readonly" }),
            'name': forms.TextInput(attrs={"class": "form-control","readonly":"readonly" }),
            'usn': forms.TextInput(attrs={"class": "form-control","readonly":"readonly" }),
            'bus_name': forms.TextInput(attrs={"class": "form-control", "readonly":"readonly"}),
            
            'address': forms.TextInput(attrs={"class": "form-control","readonly":"readonly" }),
            'contact': forms.TextInput(attrs={"class": "form-control","readonly":"readonly" }),
            'semester': forms.TextInput(attrs={"class": "form-control","readonly":"readonly" }),
            'department': forms.TextInput(attrs={"class": "form-control","readonly":"readonly" }),
            'destination': forms.TextInput(attrs={"class": "form-control","readonly":"readonly" }),
            
            'route_code': forms.TextInput(attrs={"class": "form-control", "readonly":"readonly"}),
            'enroll_date': DateInput(attrs={"class": "form-control","readonly":"readonly" }),
            'releaving_date': DateInput(attrs={"class": "form-control", }),
            
            'total_amount': forms.widgets.NumberInput(attrs={"class": "form-control","readonly":"readonly" }),
            'paid_amount': forms.widgets.NumberInput(attrs={"class": "form-control", }),
            'document' : forms.FileInput(attrs={"class": "form-control","multiple": True,'readonly':'readonly' ,"disabled":True}),
        }
        




        
# Faculity form
class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = "__all__"
        widgets = {
            'vehicle': forms.Select(attrs={"class": "form-control", }),
            "bus_name": forms.TextInput(attrs={"class": "form-control", }),
            'name': forms.TextInput(attrs={"class": "form-control", }),
            'contact': forms.TextInput(attrs={"class": "form-control", }),
            'address': forms.TextInput(attrs={"class": "form-control", }),
            'department': forms.TextInput(attrs={"class": "form-control", }),
            'route_code': forms.TextInput(attrs={"class": "form-control", }),
            'destination': forms.TextInput(attrs={"class": "form-control", }),
            'document' : forms.FileInput(attrs={"class": "form-control","multiple": True,"required":True}),
        }


# Signature form
class SignatureForm(forms.ModelForm):
    class Meta:
        model = Signature
        fields = ['signature']
        exclude = ['user']
        widgets = {
            'signature': forms.FileInput(attrs={"class": "form-control", }),
        }
