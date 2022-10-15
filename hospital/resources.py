from import_export import resources
from .models import MainInstitutionRequirements

class PersonResource(resources.ModelResource):
    class Meta:
        model = MainInstitutionRequirements