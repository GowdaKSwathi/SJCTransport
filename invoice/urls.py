from django.urls import path
from invoice import views
from django.conf.urls import handler404, handler500

urlpatterns = [
    path('', views.home, name='home'),

    path('create_vehicle', views.create_vehicle, name='create_vehicle'),
    path('view_vehicle', views.view_vehicle, name='view_vehicle'),
    path('detail_vehicle/<int:id>', views.detail_vehicle, name='detail_vehicle'),


    path('create_driver', views.create_driver, name='create_driver'),
    path('driver_list', views.view_driver, name='driver_list'),
    path('detail_driver/<int:id>', views.detail_driver, name='detail_driver'),
    path('driver_edit/<int:id>', views.update_driver, name='driver_edit'),
    path('driver_delete/<int:id>', views.delete_driver, name='driver_delete'),

    path('create_staff', views.create_staff, name='create_staff'),
    path('staff_list', views.view_staff, name='staff_list'),
    path('detail_staff/<int:id>', views.detail_staff, name='detail_staff'),
    path('staff_edit/<int:id>', views.update_staff, name='staff_edit'),
    path('staff_delete/<int:id>', views.delete_staff, name='staff_delete'),

    path('create_logsheet', views.create_logsheet, name='create_logsheet'),
    # ajax url
    path('get_logsheet_distance_to/<int:id>',
         views.get_logsheet_distance_to, name='get_logsheet_distance_to'),
    path('logsheet_list', views.view_logsheet, name='logsheet_list'),
    path('update_logsheet/<int:id>', views.update_logsheet, name='update_logsheet'),
    path('delete_logsheet/<int:id>', views.delete_logsheet, name='delete_logsheet'),
    path('logsheet_other', views.logsheet_other, name='logsheet_other'),

    path('create_fuel', views.create_fuel, name='create_fuel'),
    path('get-vehicle/<int:id>/', views.get_vehicle_progressive_km,
         name='get-vehicle'),  # ajax
    path('fuel_list', views.view_fuel, name='fuel_list'),
    path('detail_fuel/<int:id>', views.detail_fuel, name='detail_fuel'),
    path('fuel_edit/<int:id>', views.update_fuel, name='fuel_edit'),
    path('fuel_delete/<int:id>', views.delete_fuel, name='fuel_delete'),

    path('create_lubricant', views.create_lubricant, name='create_lubricant'),
    path('get-oilchange/<int:id>/', views.get_oilchange,
         name='get-oilchange'),  # ajax
    path('view_lubricant', views.view_lubricant, name='lubricant_list'),
    path('detail_lubricant/<int:id>',
         views.detail_lubricant, name='detail_lubricant'),
    path('lubricant_edit/<int:id>', views.update_lubricant, name='lubricant_edit'),
    path('lubricant_delete/<int:id>',
         views.delete_lubricant, name='lubricant_delete'),


    path('create_tyre', views.create_tyre, name='create_tyre'),
    path('get-tyre/<str:tyre_no>/', views.get_tyre, name='get-tyre'),  # ajax
    path('tyre_list', views.view_tyre, name='tyre_list'),
    path('detail_tyre/<int:id>', views.detail_tyre, name='detail_tyre'),
    path('tyre_edit/<int:id>', views.update_tyre, name='tyre_edit'),
    path('tyre_delete/<int:id>', views.delete_tyre, name='tyre_delete'),


    path('create_battery', views.create_battery, name='create_battery'),
    path('get-battery/<str:battery_no>/', views.get_battery, name='get-battery'),  # ajax
    path('battery_list', views.view_battery, name='battery_list'),
    path('detail_battery/<int:id>', views.detail_battery, name='detail_battery'),
    path('battery_edit/<int:id>', views.update_battery, name='battery_edit'),
    path('battery_delete/<int:id>', views.delete_battery, name='battery_delete'),

     # Start of Vehicle Taxation part
    path('create_tax', views.create_tax, name='create_tax'),
    path('tax_list', views.tax_list, name='tax_list'),
    path('update_tax/<int:id>', views.update_tax, name='update_tax'),
    path('delete_tax/<int:id>', views.delete_tax, name='delete_tax'),

     path('create_insurance', views.create_insurance, name='create_insurance'),
     path('insurance_list', views.insurance_list, name='insurance_list'),
     path('update_insurance/<int:id>', views.update_insurance, name='update_insurance'),
     path('delete_insurance/<int:id>', views.delete_insurance, name='delete_insurance'),


     path('create_permit', views.create_permit, name='create_permit'),
     path('permit_list', views.permit_list, name='permit_list'),
     path('update_permit/<int:id>', views.update_permit, name='update_permit'),
     path('delete_permit/<int:id>', views.delete_permit, name='delete_permit'),

     
     path('create_emission', views.create_emission, name='create_emission'),
     path('emission_list', views.emission_list, name='emission_list'),
     path('update_emission/<int:id>', views.update_emission, name='update_emission'),
     path('delete_emission/<int:id>', views.delete_emission, name='delete_emission'),


     path('create_fitness', views.create_fitness, name='create_fitness'),
     path('fitness_list', views.fitness_list, name='fitness_list'),
     path('update_fitness/<int:id>', views.update_fitness, name='update_fitness'),
     path('delete_fitness/<int:id>', views.delete_fitness, name='delete_fitness'),

     # End of Vehicle Taxation part
     path('create_repair', views.create_repair, name='create_repair'),
     path('repair_list', views.view_repair, name='repair_list'),
     path('detail_repair/<int:id>', views.detail_repair, name='detail_repair'),

     path('create_service', views.create_spare, name='create_service'),
     path('service_list', views.view_spare, name='service_list'),
     path('create_other', views.create_other, name='create_other'),
     path('other_list', views.view_other, name='other_list'),

     path('create_scrap', views.create_scrap, name='create_scrap'),
     path('scrap_list', views.view_scrap, name='scrap_list'),


     path('create_student', views.create_student, name='create_student'),
     path('student_list', views.student_list, name='student_list'),
     path('detail_student/<int:id>', views.student_detail, name='detail_student'),
     path('student_update/<int:id>', views.student_update, name='student_update'),
     path('student_delete/<int:id>', views.student_delete, name='student_delete'),


     path('create_faculty', views.create_faculty, name='create_faculty'),
     path('faculty_list', views.faculty_list, name='faculty_list'),
     path('detail_faculty/<int:id>', views.detail_faculty, name='detail_faculty'),
     path('faculty_delete/<int:id>', views.faculty_delete, name='faculty_delete'),

     # report urls
     path('year_report', views.year_report, name='year_report'),
     path('full_details', views.full_details, name='full_details'),
     path('invoice', views.invoice, name='invoice'),

     # principal urls
     path('principal_page', views.principal_page, name='principal_page'),
]

handler404 = 'invoice.views.error_404_view'
