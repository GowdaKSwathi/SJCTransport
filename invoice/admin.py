from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import *
# Register your models here.


admin.site.register(Vehicle)
admin.site.register(Driver)
admin.site.register(Staff)


admin.site.register(Log)
admin.site.register(Logsheet)

admin.site.register(Fuel)
admin.site.register(Lubricant)


admin.site.register(Tyre)
admin.site.register(Battery)
admin.site.register(Spare)
admin.site.register(Other)

admin.site.register(Tax)
admin.site.register(Insurance)
admin.site.register(Fitness)
admin.site.register(Permit)
admin.site.register(Emission)


admin.site.register(Repair)
admin.site.register(Scrap)
admin.site.register(Notify)
admin.site.register(Signature)

# import export for student
class StudentResource(resources.ModelResource):
    class Meta:
        model = Student
        
class StudentAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('vehicle','bus_name','name','usn','department','route_code','destination','total_amount','paid_amount',)
    resource_class = StudentResource
    
admin.site.register(Student,StudentAdmin)


# import export fauclity
class FacultyResource(resources.ModelResource):
    class Meta:
        model = Faculty
    
    
class FacultyAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('vehicle','bus_name','name','department','route_code','destination')
    resource_class = FacultyResource
    
admin.site.register(Faculty,FacultyAdmin)
    
