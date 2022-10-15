from dataclasses import fields
from django import forms
from django.contrib.auth.models import User
from . import models
from django.core.exceptions import ValidationError



#for admin signup
class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
        
#for admin signup
class OrganizationSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }


#for student related form
class Vice_MayorOfSocialAffairsOftheHeadPHF_MOHUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class Vice_MayorOfSocialAffairsOftheHeadPHF_MOHForm(forms.ModelForm):
    class Meta:
        model= models.Vice_MayorOfSocialAffairsOftheHeadPHF_MOH
        fields=['address','mobile','department','status','profile_pic']



#for teacher related form
class OrganizationUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
# class OrganizationForm(forms.ModelForm):
#     #this is the extrafield for linking patient and their assigend doctor
#     #this will show dropdown __str__ method doctor model is shown on html so override it
#     #to_field_name this will fetch corresponding value  user_id present in Doctor model and return it
   
#     class Meta:
#         model= models.Organization
#         fields= ['photo','organizationName','organizationcategory','location','readerName', 'email','startdate', 'organization_discription','mobile']

class OrganizationForm (forms.ModelForm):
    photo = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class':'form-control'}))
    readName = forms.CharField(strip=True, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'ReadName'}))
    organizationName = forms.CharField(strip=True, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'organizationName '}))
    location  = forms.CharField(strip=True, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'location '}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Valid Email'}))
    user = forms.ModelChoiceField(User.objects.all(),required=True, empty_label='Select a OrganizationRead',widget=forms.Select(attrs={'class':'form-control'}))
    startdate= forms.CharField(strip=True, widget=forms.DateInput(attrs={'class':'form-control','type':'date'}))
    mobileNumber = forms.CharField(strip=True, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'MobileNumber'}))
    organization_discription = forms.CharField(strip=True, widget=forms.Textarea(attrs={'class':'form-control','placeholder':''}))

    class Meta:
        model = models.Organization
        fields= ['organizationcategory']
        # widgets={
        #     'OrganizationCategory': forms.Select(attrs={'class':'form-control'}),
            
        # }
    

class  Assigne_Organization_To_RequirementsForm(forms.ModelForm):
    
    class Meta:
        model=models.Assigne_Organization_To_Requirements
        fields = '__all__'  

        widgets={
 
            'mobile':forms.TextInput(attrs={'class':'form-control'}),
            'period': forms.Select(attrs={'class':'form-control'}),
            'organizatonName':forms.Select(attrs={'class':'form-control'}),
            'requirementselected':forms.CheckboxSelectMultiple(),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'admitDate':forms.DateInput(attrs={'class':'form-control','type':'date'}),
        }
    


class OrganizationAssigneRequirementsForm(forms.ModelForm):
    # requirementId=forms.ModelChoiceField(queryset=models.MainInstitutionRequirements.objects.all().filter(status=True),empty_label="Requirement Name and Category", to_field_name="user_id")
    class Meta:
        model = models.Assigne_Organization_To_Requirements
        fields = '__all__'
        widgets={
            'organizationId ':forms.TextInput(attrs={'class':'form-control'}),
            'mobile':forms.TextInput(attrs={'class':'form-control'}),
            'period': forms.Select(attrs={'class':'form-control'}),
            'nameofOrganization':forms.Select(attrs={'class':'form-control'}),
            'requirementselected':forms.CheckboxSelectMultiple(),
            ' admitDate':forms.DateInput(attrs={'class':'form-control'}),
        }

        

class PeriodForm(forms.ModelForm):

    class Meta:
        model = models.Period
        fields = '__all__'

class OrderForm(forms.ModelForm):

    class Meta:
        model = models.Order
        fields = '__all__'

class OrderItemForm(forms.ModelForm):

    class Meta:
        model = models.OrderItem
        fields = '__all__'

class MohCommentForm(forms.ModelForm):

    class Meta:
        model = models.Order
        fields = '__all__'

class OrganizationFeedBackForm(forms.ModelForm):

    class Meta:
        model = models.OrganizationFeedBack
        fields = '__all__'
        widgets={
            'nameofOrganization':forms.Select(attrs={'class':'form-control'}),
            'message':forms.Textarea(attrs={'class':'form-control'}),
            'time':forms.DateInput(attrs={'class':'form-control'}),        
        }


#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))



#Developed By : sumit kumar
#facebook : fb.com/sumit.luv
#Youtube :youtube.com/lazycoders
