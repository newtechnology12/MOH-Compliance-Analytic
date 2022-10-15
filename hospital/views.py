from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.views.generic import FormView, CreateView,View,DetailView,TemplateView,ListView,UpdateView
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render,redirect, resolve_url,reverse, get_object_or_404
from django.contrib.auth import logout
from django.contrib import auth


from django.shortcuts import render
from django.http import HttpResponse
from .resources import PersonResource
from tablib import Dataset
from search_views.views import SearchListView
from search_views.filters import BaseFilter
# Create your views here.
def home_view(request):
    # if request.user.is_authenticated:
    #     return HttpResponseRedirect('')
    return render(request,'hospital/index.html')


#for showing signup/login button for admin(by sumit)
def adminclick_view(request):
    # if request.user.is_authenticated:
        # return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/adminclick.html')


#for showing signup/login button for doctor(by sumit)
def doctorclick_view(request):
    # if request.user.is_authenticated:
    #     return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/doctorclick.html')


#for showing signup/login button for patient(by sumit)
def patientclick_view(request):
    # if request.user.is_authenticated:
    #     return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/patientclick.html')


def logout(request):
    auth.logout(request)
    return render(request,'hospital/index.html')

def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request,'hospital/adminsignup.html',{'form':form})




def doctor_signup_view(request):
    userForm=forms.Vice_MayorOfSocialAffairsOftheHeadPHF_MOHUserForm
    doctorForm=forms.Vice_MayorOfSocialAffairsOftheHeadPHF_MOHForm
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.Vice_MayorOfSocialAffairsOftheHeadPHF_MOHUserForm(request.POST)
        doctorForm=forms.Vice_MayorOfSocialAffairsOftheHeadPHF_MOHForm(request.POST,request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor=doctor.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
        return HttpResponseRedirect('doctorlogin')
    return render(request,'hospital/doctorsignup.html',context=mydict)


# def patient_signup_view(request):
#     userForm=forms.OrganizationUserForm
#     patientForm=forms.OrganizationForm
#     mydict={'userForm':userForm,'patientForm':patientForm}
#     if request.method=='POST':
#         userForm=forms.OrganizationUserForm(request.POST)
#         patientForm=forms.OrganizationForm(request.POST,request.FILES)
#         if userForm.is_valid() and patientForm.is_valid():
#             user=userForm.save()
#             user.set_password(user.password)
#             user.save()
#             patient=patientForm.save(commit=False)
#             patient.user=user            
#             patient=patient.save()
#             my_patient_group = Group.objects.get_or_create(name='PATIENT')
#             my_patient_group[0].user_set.add(user)
#         return HttpResponseRedirect('patientlogin')
#     return render(request,'hospital/patientsignup.html',context=mydict)


def patient_signup_view(request):
    form=forms.OrganizationSigupForm()
    if request.method=='POST':
        form=forms.OrganizationSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='PATIENT')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('patientlogin')
    return render(request,'hospital/adminsignup.html',{'form':form})





#-----------for checking user is doctor , patient or admin(by sumit)
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()


#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_doctor(request.user):
        accountapproval=models.Vice_MayorOfSocialAffairsOftheHeadPHF_MOH.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('doctor-dashboard')
        else:
            return render(request,'hospital/doctor_wait_for_approval.html')

    elif is_patient(request.user):
        return redirect('patient-dashboard') 
    
               
    else:
         return render(request,'hospital/patient_wait_for_approval.html')
           
 
         








#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
def admin_dashboard_view(request):
    #for both table in admin dashboard
    doctors=models.Vice_MayorOfSocialAffairsOftheHeadPHF_MOH.objects.all().filter(status = True)
    organization = models.Organization.objects.all().filter(status = True)
    organizations = models.Organization.objects.all().filter(status = False)
    patients=models.Organization.objects.all().order_by('-id')
    #for three cards
    doctorcount=models.Vice_MayorOfSocialAffairsOftheHeadPHF_MOH.objects.all().filter(status=True).count()
    pendingdoctorcount=models.Vice_MayorOfSocialAffairsOftheHeadPHF_MOH.objects.all().filter(status=False).count()

    patientcount=models.Organization.objects.count()
    pendingpatientcount=models.Organization.objects.all().filter(status=False).count()

    appointmentcount=models.Assigne_Organization_To_Requirements.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Assigne_Organization_To_Requirements.objects.all().filter(status=False).count()
    mydict={
    'organizations': organizations,
    'organization':organization,
    'doctors':doctors,
    'patients':patients,
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    }
    return render(request,'hospital/admin_dashboard.html',context=mydict)


# this view for sidebar click on admin page
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_doctor_view(request):
    return render(request,'hospital/admin_doctor.html')



# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
def admin_view_doctor_view(request):
    doctors=models.Vice_MayorOfSocialAffairsOftheHeadPHF_MOH.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_doctor.html',{'doctors':doctors})



# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
def delete_doctor_from_hospital_view(request,pk):
    doctor=models.Vice_MayorOfSocialAffairsOftheHeadPHF_MOH.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-view-doctor')



# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
def update_doctor_view(request,pk):
    doctor=models.Vice_MayorOfSocialAffairsOftheHeadPHF_MOH.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)

    userForm=forms.Vice_MayorOfSocialAffairsOftheHeadPHF_MOHUserForm(instance=user)
    doctorForm=forms.Vice_MayorOfSocialAffairsOftheHeadPHF_MOHForm(request.FILES,instance=doctor)
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.Vice_MayorOfSocialAffairsOftheHeadPHF_MOHUserForm(request.POST,instance=user)
        doctorForm=forms.Vice_MayorOfSocialAffairsOftheHeadPHF_MOHForm(request.POST,request.FILES,instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.status=True
            doctor.save()
            return redirect('admin-view-doctor')
    return render(request,'hospital/admin_update_doctor.html',context=mydict)




# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
def admin_add_doctor_view(request):
    userForm=forms.Vice_MayorOfSocialAffairsOftheHeadPHF_MOHUserForm
    doctorForm=forms.Vice_MayorOfSocialAffairsOftheHeadPHF_MOHForm
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.Vice_MayorOfSocialAffairsOftheHeadPHF_MOHUserForm(request.POST)
        doctorForm=forms.Vice_MayorOfSocialAffairsOftheHeadPHF_MOHForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor.status=True
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-doctor')
    return render(request,'hospital/admin_add_doctor.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_doctor_view(request):
    #those whose approval are needed
    doctors=models.Vice_MayorOfSocialAffairsOftheHeadPHF_MOH.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_doctor.html',{'doctors':doctors})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_doctor_view(request,pk):
    doctor=models.Vice_MayorOfSocialAffairsOftheHeadPHF_MOH.objects.get(id=pk)
    doctor.status=True
    doctor.save()
    return redirect(reverse('admin-approve-doctor'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_doctor_view(request,pk):
    doctor=models.Vice_MayorOfSocialAffairsOftheHeadPHF_MOH.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-approve-doctor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_specialisation_view(request):
    doctors=models.Vice_MayorOfSocialAffairsOftheHeadPHF_MOH.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_doctor_specialisation.html',{'doctors':doctors})



# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
def admin_patient_view(request):
    return render(request,'hospital/admin_patient.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_patient_view(request):
    patients=models.User.objects.all()
    return render(request,'hospital/admin_view_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_patient_from_hospital_view(request,pk):
    patient=models.Organization.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-view-patient')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_patient_view(request,pk):
    patient=models.Organization.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)

    userForm=forms.OrganizationUserForm(instance=user)
    patientForm=forms.OrganizationForm(request.FILES,instance=patient)
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.OrganizationUserForm(request.POST,instance=user)
        patientForm=forms.OrganizationForm(request.POST,request.FILES,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.status=True
            patient. assignedRequirementId=request.POST.get('assignedRequirementId')
            patient.save()
            return redirect('admin-view-patient')
    return render(request,'hospital/admin_update_patient.html',context=mydict)





# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
def admin_add_patient_view(request):
    userForm=forms.OrganizationUserForm
    patientForm=forms.OrganizationForm
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.OrganizationUserForm(request.POST)
        patientForm=forms.OrganizationForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            patient=patientForm.save(commit=False)
            patient.user=user
            patient.status=True
            patient.assignedRequirementId=request.POST.get(' assignedRequirementId')
            patient.save()

            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-patient')
    return render(request,'hospital/admin_add_patient.html',context=mydict)



#--------------for discharge patient bill (pdf) download and printing
#--------------for discharge patient bill (pdf) download and printing
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return





def download_pdf_view(request,pk):
    dischargeDetails=models.Assigne_Organization_To_Requirements.objects.all().filter(id=pk)
    dict={
        'organizatonName':dischargeDetails[0].organizatonName,
        'requirementselected':dischargeDetails[0].requirementselected,
        'period':dischargeDetails[0].period,
        'status':dischargeDetails[0].status,
        'mobile':dischargeDetails[0].mobile,
        'email':dischargeDetails[0].email,
        'admitDate':dischargeDetails[0].admitDate,
  
    }
    return render_to_pdf('hospital/download_bill.html',dict)



#------------------FOR APPROVING PATIENT BY ADMIN----------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_patient_view(request):
    #those whose approval are needed
    patients=models.User.objects.all()
    return render(request,'hospital/admin_approve_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_patient_view(request,pk):
    patient=models.Organization.objects.get(id=pk)
    patient.status=True
    patient.save()
    return redirect(reverse('admin-approve-patient'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_patient_view(request,pk):
    patient=models.Organization.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-approve-patient')



#-----------------APPOINTMENT START--------------------------------------------------------------------
# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
def admin_appointment_view(request):
    return render(request,'hospital/admin_appointment.html')



# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
def admin_view_appointment_view(request):
    appointments=models.Assigne_Organization_To_Requirements.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_appointment.html',{'appointments':appointments})



# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
# def admin_add_appointment_view(request):
class  admin_add_appointment_view (CreateView):
    model = models.Period
    form_class = forms.PeriodForm 
    template_name = 'hospital/admin_add_appointment.html'
    login_url = 'checkingRequirement:login'

    # def get_success_url(self):
    
    #     url = resolve_url('admin-view-appointment')
    #     return url

   

# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    #those whose approval are needed
    appointments=models.Organization.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_appointment.html',{'appointments':appointments})

# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
def mohworker_approve_appointment_view(request):
    #those whose approval are needed
    appointments=models.Organization.objects.all().filter(status=False)
    return render(request,'hospital/doctor_approve_appointment.html',{'appointments':appointments})



# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
def approve_appointment_view(request,pk):
    appointment=models.Organization.objects.get(id=pk)
    appointment.status=True
    appointment.save()
    return redirect(reverse('admin-approve-appointment'))

def mohapprove_appointment_view(pk):
    appointment=models.Organization.objects.get(id=pk)
    appointment.status=True
    appointment.save()
    return redirect(reverse('doctor-approve-appointment'))



# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
def reject_appointment_view(request,pk):
    appointment=models.Organization.objects.get(id=pk)
    appointment.delete()
    return redirect('admin-approve-appointment')

def mohreject_appointment_view(request,pk):
    appointment=models.Organization.objects.get(id=pk)
    appointment.delete()
    return redirect('doctor-approve-appointment')
#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
# @login_required(login_url='doctorlogin')
# @user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    #for three cards
    patientcount=models.Organization.objects.all().filter(status=True).count()
    appointmentcount=models.Assigne_Organization_To_Requirements.objects.all().filter(status=True).count()
   

    #for  table in doctor dashboard
    appointments=models.Assigne_Organization_To_Requirements.objects.all().filter(status=True).order_by('-id')
    patients=models.Organization.objects.all()
    appointments=zip(appointments,patients)
    doctors=models.Vice_MayorOfSocialAffairsOftheHeadPHF_MOH.objects.all().filter(status = True)
    organization = models.Organization.objects.all().filter(status = True)
    organizations = models.Organization.objects.all().filter(status = False)
    patients=models.Organization.objects.all().order_by('-id')
    mydict={
    'doctors':doctors,
    'organization':organization,
    'organization':organization,
    'organizations':organizations,
    'patients':patients,
    'patientcount':patientcount,
    'appointmentcount':appointmentcount,
    # 'patientdischarged':patientdischarged,
    'appointments':appointments,
    'doctor':models.Assigne_Organization_To_Requirements.objects.filter(status =True), #for profile picture of doctor in sidebar
    }
    return render(request,'hospital/doctor_dashboard.html',context=mydict)



# @login_required(login_url='doctorlogin')
# @user_passes_test(is_doctor)
def doctor_patient_view(request):
    mydict={
    'doctor':models.Organization.objects.filter(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'hospital/doctor_patient.html',context=mydict)





# @login_required(login_url='doctorlogin')
# @user_passes_test(is_doctor)
def doctor_view_patient_view(request):
    patients=models.MainInstitutionRequirements.objects.all().filter(status=True)
    doctor=models.Vice_MayorOfSocialAffairsOftheHeadPHF_MOH.objects.filter(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_view_patient.html',{'patients':patients,'doctor':doctor})


# @login_required(login_url='doctorlogin')
# @user_passes_test(is_doctor)
def search_view(request):
    doctor=models.Vice_MayorOfSocialAffairsOftheHeadPHF_MOH.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    # whatever user write in search box we get in query
    query = request.GET['query']
    patients=models.Organization.objects.all().filter(status=True,assignedRequirementId=request.user.id).filter(Q(organizationcategory__icontains=query)|Q(organization__organizationName__icontains=query))
    return render(request,'hospital/doctor_view_patient.html',{'patients':patients,'doctor':doctor})


# @login_required(login_url='doctorlogin')
# @user_passes_test(is_doctor)
def doctor_appointment_view(request):
    doctor=models.Vice_MayorOfSocialAffairsOftheHeadPHF_MOH.objects.filter(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_appointment.html',{'doctor':doctor})



# @login_required(login_url='doctorlogin')
# @user_passes_test(is_doctor)
def doctor_view_appointment_view(request):
    doctor=models.Vice_MayorOfSocialAffairsOftheHeadPHF_MOH.objects.filter(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Assigne_Organization_To_Requirements.objects.all().filter(status=True)

    return render(request,'hospital/doctor_view_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_delete_appointment_view(request):
    doctor=models.Vice_MayorOfSocialAffairsOftheHeadPHF_MOH.objects.filter(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Assigne_Organization_To_Requirements.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Organization.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------




# @login_required(login_url='adminlogin')
# @user_passes_test(is_admin)
def patient_dashboard_view(request):
  
    totalRequirement = models.MainInstitutionRequirements.objects.all().order_by('-id').count
    mohComment=models.MohComment.objects.all().filter(status = True).count()
    # mohcomment = models.MohComment.objects.all().filter(nameofOrganization = 'nameofOrganization')
   
    mydict={
    'mohComment': mohComment,
    'totalRequirement':totalRequirement,
    

    }
    return render(request,'hospital/patient_dashboard.html',context=mydict)



class  Assigne_Organization_To_Requirements_Add (CreateView):
    model = models.Assigne_Organization_To_Requirements 
    form_class = forms.Assigne_Organization_To_RequirementsForm 
    template_name = 'hospital/patient_book_appointment.html'
    login_url = 'checkingRequirement:login'

    def get_success_url(self):
    
        url = resolve_url('patient-dashboard')
        return url



class OrganizationFeedBack_Add (CreateView):
    model = models.OrganizationFeedBack 
    form_class = forms.OrganizationFeedBackForm
    template_name = 'hospital/patient_book_appointments2.html'
    # usermohfeedback 
    login_url = 'checkingRequirement:login'

    def get_success_url(self):
    
        url = resolve_url('patient-dashboard')
        return url


class organizationServices_Add (CreateView):
    model = models.Organization  
    form_class = forms.OrganizationForm
    template_name = 'hospital/patient_book_appointments3.html'
    login_url = 'checkingRequirement:login'

    def get_success_url(self):
    
        url = resolve_url('patient-dashboard')
        return url

 


# @login_required(login_url='patientlogin')
# @user_passes_test(is_patient)
def patient_book_appointment_view(request):
    patient=models.Organization.objects.filter(user_id=request.user.id)
    redirect_field_name = 'patient-view-appointment' #for profile picture of patient in sidebar
    return render(request,'hospital/patient_appointment.html',{'patient':patient})




def patient_view_doctor_view(request):
    doctors=models.Vice_MayorOfSocialAffairsOftheHeadPHF_MOH.objects.all().filter(status=True)
    patient=models.Organization.objects.filter(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'hospital/patient_view_doctor.html',{'patient':patient,'doctors':doctors})



def search_doctor_view(request):
    patient=models.Organization.objects.filter(user_id=request.user.id) #for profile picture of patient in sidebar
    
    # whatever user write in search box we get in query
    query = request.GET['query']
    doctors=models.Vice_MayorOfSocialAffairsOftheHeadPHF_MOH.objects.all().filter(status=True).filter(Q(department__icontains=query)| Q(user__first_name__icontains=query))
    return render(request,'hospital/patient_view_doctor.html',{'patient':patient,'doctors':doctors})




# @login_required(login_url='patientlogin')
# @user_passes_test(is_patient)
def patient_view_appointment_view(request):
    mohFeedBack = models.MohComment.objects.all() #for profile picture of patient in sidebar
    return render(request,'hospital/patient_view_appointment.html',{'patient':mohFeedBack})

#------------------------ PATIENT RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------


#---------------------------------------------------------------------------------
#------------------------ ABOUT US AND CONTACT US VIEWS START ------------------------------
#---------------------------------------------------------------------------------
def aboutus_view(request):
    return render(request,'hospital/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'hospital/contactussuccess.html')
    return render(request, 'hospital/contactus.html', {'form':sub})


def export(request):
    person_resource = PersonResource()
    dataset = person_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="persons.xls"'
    return response


def simple_upload(request):
    if request.method == 'POST':
        person_resource = PersonResource()
        dataset = Dataset()
        new_persons = request.FILES['myfile']

        imported_data = dataset.load(new_persons.read(),format='xlsx')
        #print(imported_data)
        for data in imported_data:
            print(data[1])
        value = models.MainInstitutionRequirements(
        		data[0],
        		data[1],
        		 data[2],
        		 data[3]
        		)
        value.save()

        	       

    return render(request, 'hospital/input.html')
#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------



#Developed By : sumit kumar
#facebook : fb.com/sumit.luv
#Youtube :youtube.com/lazycoders
