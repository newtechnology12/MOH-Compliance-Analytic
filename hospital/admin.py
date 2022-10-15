from import_export.admin import ImportExportModelAdmin

from django.contrib import admin
from .models import *
# Register your models here.
# class MainInstitutionRequirementsAdmin(admin.ModelAdmin):

@admin.register(MainInstitutionRequirements)
class MainInstitutionRequirementsAdmin(ImportExportModelAdmin):
    list_display = ('CRITERESType', 'OrganizationCategory', 'CRITERESName', 'date')


@admin.register(Organization)
class OrganizationAdmin(ImportExportModelAdmin):
    list_display = ('photo', 'organizationName', 'organizationcategory', 'location', 'readerName','email','startdate','organization_discription','mobile', 'status')


@admin.register(Period)
class PeriodAdmin(ImportExportModelAdmin):
    list_display = ('year', 'startDate', 'endDate', 'nameOfperiod', 'description', 'status')


@admin.register(Assigne_Organization_To_Requirements)
class Assigne_Organization_To_RequirementsAdmin(ImportExportModelAdmin):
    list_display = ('period','organizatonName', 'mobile', 'email', 'admitDate', 'status')


class OrderAdmin(admin.ModelAdmin):
    pass
admin.site.register(Order, OrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    pass
admin.site.register( OrderItem, OrderItemAdmin)


class MohCommentAdmin(admin.ModelAdmin):
    pass
admin.site.register(MohComment, MohCommentAdmin)


@admin.register(OrganizationFeedBack)
class OrganizationFeedBackAdmin(ImportExportModelAdmin):
    list_display = ('nameofOrganization','message','time')


# class Vice_MayorOfSocialAffairsOftheHeadPHF_MOHAdmin(admin.ModelAdmin):
#     pass
# admin.site.register( Vice_MayorOfSocialAffairsOftheHeadPHF_MOH, Vice_MayorOfSocialAffairsOftheHeadPHF_MOHAdmin)

@admin.register(Vice_MayorOfSocialAffairsOftheHeadPHF_MOH)
class Vice_MayorOfSocialAffairsOftheHeadPHF_MOHAdmin(ImportExportModelAdmin):
    list_display = ('user','address','mobile','department','status')


admin.site.site_header = 'ADM Page Of MOH-Compliance Analytic.'
admin.site.site_title = 'Welcome To MOH-Compliance Analytic.'
admin.site.index_title = 'Welcome To MOH-Compliance Analytic.'