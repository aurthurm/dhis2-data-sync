from django.contrib import admin
from .models import (
    OrganisatinalUnit,
    DataSet,
    DataElement,
    DataImport,
    OptionSetOption,
    OptionSet
)


class OrganisatinalUnitAdmin(admin.ModelAdmin):
    list_display = ['dhis_id', 'name']
    search_fields = ['dhis_id', 'name']
admin.site.register(OrganisatinalUnit, OrganisatinalUnitAdmin)

class DataSetAdmin(admin.ModelAdmin):
    list_display = ['dhis_id', 'name']
    search_fields = ['dhis_id', 'name']
admin.site.register(DataSet, DataSetAdmin)

class DataElementAdmin(admin.ModelAdmin):
    list_display = ['dhis_id', 'name', 'dataset']
    search_fields = ['dhis_id', 'name', "dataset__dhis_id", "dataset__name"]
    def regroup_by(self):
        return 'dataset__name'
admin.site.register(DataElement, DataElementAdmin)

class DataImportAdmin(admin.ModelAdmin):
    list_display = ['ornanisationunit', 'dataset', 'dataelement', 'value', 'comment', 'followup', 'deleted']
    search_fields = ['period', 'value']
admin.site.register(DataImport, DataImportAdmin)

class OptionSetAdmin(admin.ModelAdmin):
    list_display = ['dhis_id', 'name']
    search_fields = ['dhis_id', 'name']
admin.site.register(OptionSet, OptionSetAdmin)

class OptionSetOptionAdmin(admin.ModelAdmin):
    list_display = ['optionset', 'dhis_id', 'name']
    search_fields = ['optionset', 'name', 'name']
admin.site.register(OptionSetOption, OptionSetOptionAdmin)
