from django.db import models
from django.contrib.auth.models import User



departments=[
    ('HOSPITAL','hospital'),
    ('CLINIQUE','clinique'),
    ('MEDICAL', 'medical'),
    ('CENTER', 'center'),
    ('DENTAL_CENTER', 'dental_centr'),
    ('RABORATORY', 'raboratory'),
    ('CARAES', 'caraes'),
    ('POLYCLINIC', 'polyclinic'),
    ('OPTIONAL' ,'optional'),
    ('PHARMACY','pharmacy')
]




EVALUATION_CRITERIA_FOR_HEALPHORGANIZATION = [
    {'I.STAFF', 'STAFF'},
    {'II.ORGANIZATIO', 'ORGANIZATIO'},
    {'Equipment', 'EQUIPMENTS'},
     ('III. INFRASTRUCTURE', (
            ('III.1. External environment', 'III.1. External environment'),
            ('III.2. Building', ' III.2. Building'),
            ('III.3. Sufficient hygiene', ' III.3. Sufficient hygiene'),
            ('III.4. Acceptable Space and Bed Management', 'III.4. Acceptable Space and Bed Management'),
            ('III.4.1. Waiting room and reception', ' III.4.1. Waiting room and reception'),
            ('III.4.2. Triage room and taking vital signs', ' III.4.2. Triage room and taking vital signs'),
            ('III.4.3. Consultation room', ' III.4.3. Consultation room'),
            ('III.4.4. Laboratory room', ' III.4.4. Laboratory room'),
            ('III.4.5. Sterilization room', ' III.4.5. Sterilization room'),
            ('III.4.6. Minor surgery room', ' III.4.6. Minor surgery room'),
            ('III.4.7. Nursing room', ' III.4.7. Nursing room'),
            ('III.4.8. Hospitalization: (1/3 of beds: multi-position)', 'III.4.8. Hospitalization: (1/3 of beds: multi-position)'),

        )
    ),
]


class MainInstitutionRequirements(models.Model):
 
    CRITERESType = models.CharField(choices=EVALUATION_CRITERIA_FOR_HEALPHORGANIZATION, max_length=255, blank=False,null= True)
    OrganizationCategory = models.CharField(choices=departments, max_length= 100, blank=False)
    CRITERESName = models.CharField(max_length=100, blank=False, null=True)
    date = models.DateField(auto_created=True)
    # TotalRequirement = models.IntegerField(default=0)
    status=models.BooleanField(default=False)
  
    def __str__(self):
        return "{} ({})".format(self.CRITERESName,self.CRITERESType)
  
class Organization(models.Model):
    # user=models.OneToOneField(User,on_delete=models.CASCADE, blank=True, null=True)
    photo = models.ImageField(upload_to='media/%Y/%m/%d/',max_length=70, blank=False )
    organizationName = models.CharField(max_length=100, blank=False, null=True)
    organizationcategory = models.CharField(choices=departments,max_length=100, null=True, blank=False)
    location = models.CharField(max_length=100, blank=True, null=True)  
    readerName = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    startdate = models.DateField(auto_created=True, blank=False, null=True)
    organization_discription = models.TextField( blank=True, null=True)
    mobile = models.CharField(max_length=20,null=False)
   


    status=models.BooleanField(default=False)
    
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.organizationName+" ("+self.organizationcategory+")"
    # @property
    # def get_name(self):
    #     return self.user.first_name +"" ""+ self.user.last_name

  
        
class Period(models.Model):
    year = models.CharField(max_length=10, null=False, blank=False)
    startDate = models.DateTimeField(auto_created=True)
    endDate = models.DateField(auto_created=True, blank=False, null=True)
    nameOfperiod = models.CharField(max_length=100, blank=False, null=True)
    description = models.TextField(max_length=200, blank=False, null=True)
    status =models.BooleanField(default=False)

    def __str__(self):
        return f"{self.year}: : {self.endDate}: : {self.nameOfperiod}"  


class Assigne_Organization_To_Requirements(models.Model):
    period = models.ForeignKey(Period, max_length=100, related_name='userselectedRequirements', on_delete=models.CASCADE)
    organizatonName = models.ForeignKey(Organization,max_length=100, on_delete=models.CASCADE, blank=False, related_name="organization")
    mobile = models.CharField(max_length=20,null=True)
    email = models.EmailField(max_length=100, blank=False, null=True)
    requirementselected = models.ManyToManyField(MainInstitutionRequirements, related_name='subscriptions')
    admitDate=models.DateField(auto_now_add=True, null=False)
    status =models.BooleanField(default=False)
    # totalRequirement = models.IntegerField(default=0)
   
    def __str__(self):
        return f"{self.organizatonName}: {self.period}: {self.id}"
    

    
class Order(models.Model):
	customer = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)
		
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.mainInstitutionRequirements.status == False:
				shipping = True
		return shipping

	@property
	def get_cart_total(self):
		global total
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 

class OrderItem(models.Model):
	requiements = models.ForeignKey(MainInstitutionRequirements, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)


class MohComment(models.Model):
       
        nameofOrganization = models.ForeignKey(Organization, related_name="mohfeedback", on_delete=models.CASCADE, blank=True, null=True)
        message = models.TextField(max_length=500, blank=True, null=True)
        time = models.DateTimeField(auto_now_add=True, blank=False, null=True)
        status = models.BooleanField(default=False)

        def __str__(self) -> str:
            return f"{self.nameofOrganization}, {self.time}"


class OrganizationFeedBack(models.Model):
        nameofOrganization = models.OneToOneField(Organization, related_name="organizationfeedback", on_delete=models.CASCADE, blank=True, null=True)
        message = models.TextField(max_length=500, blank=True, null=True)
        time = models.DateTimeField(auto_now_add=True, blank=False, null=True)
        status=models.BooleanField(default=False)
        
        def __str__(self) -> str:
            return f"{self.nameofOrganization}, {self.time}"



class Vice_MayorOfSocialAffairsOftheHeadPHF_MOH(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/DoctorProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    department= models.CharField(max_length=50,default='Social Affairs')
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)



# class Patient(models.Model):
#     user=models.OneToOneField(User,on_delete=models.CASCADE)
#     profile_pic= models.ImageField(upload_to='profile_pic/PatientProfilePic/',null=True,blank=True)
#     address = models.CharField(max_length=40)
#     mobile = models.CharField(max_length=20,null=False)
#     symptoms = models.CharField(max_length=100,null=False)
#     assignedDoctorId = models.PositiveIntegerField(null=True)
#     admitDate=models.DateField(auto_now=True)
#     status=models.BooleanField(default=False)
#     @property
#     def get_name(self):
#         return self.user.first_name+" "+self.user.last_name
#     @property
#     def get_id(self):
#         return self.user.id
#     def __str__(self):
#         return self.user.first_name+" ("+self.symptoms+")"


# class Appointment(models.Model):
#     patientId=models.PositiveIntegerField(null=True)
#     doctorId=models.PositiveIntegerField(null=True)
#     patientName=models.CharField(max_length=40,null=True)
#     doctorName=models.CharField(max_length=40,null=True)
#     appointmentDate=models.DateField(auto_now=True)
#     description=models.TextField(max_length=500)
#     status=models.BooleanField(default=False)



# class PatientDischargeDetails(models.Model):
#     patientId=models.PositiveIntegerField(null=True)
#     patientName=models.CharField(max_length=40)
#     assignedDoctorName=models.CharField(max_length=40)
#     address = models.CharField(max_length=40)
#     mobile = models.CharField(max_length=20,null=True)
#     symptoms = models.CharField(max_length=100,null=True)

#     admitDate=models.DateField(null=False)
#     releaseDate=models.DateField(null=False)
#     daySpent=models.PositiveIntegerField(null=False)

#     roomCharge=models.PositiveIntegerField(null=False)
#     medicineCost=models.PositiveIntegerField(null=False)
#     doctorFee=models.PositiveIntegerField(null=False)
#     OtherCharge=models.PositiveIntegerField(null=False)
#     total=models.PositiveIntegerField(null=False)


#Developed By : sumit kumar
#facebook : fb.com/sumit.luv
#Youtube :youtube.com/lazycoders
