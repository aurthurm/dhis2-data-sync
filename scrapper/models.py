from django.db import models


class OrganisatinalUnit(models.Model):
    dhis_id = models.CharField(max_length=255, blank=False, null=False, unique=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    
    def __str__(self) -> str:
        return f"{self.name}"


class DataSet(models.Model):
    dhis_id = models.CharField(max_length=255, blank=False, null=False, unique=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    
    def __str__(self) -> str:
        return f"{self.name}"


class DataElement(models.Model):
    dataset = models.ForeignKey(DataSet, on_delete=models.PROTECT, null=True, related_name="elements")
    dhis_id = models.CharField(max_length=255, blank=False, null=False, unique=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    
    def __str__(self) -> str:
        return f"{self.name}"

    
class OptionSet(models.Model):
    dhis_id = models.CharField(max_length=255, blank=False, null=False, unique=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    
    
    def __str__(self) -> str:
        return f"{self.name}"


class OptionSetOption(models.Model):
    optionset = models.ForeignKey(OptionSet, on_delete=models.PROTECT, null=True, related_name="options")
    dhis_id = models.CharField(max_length=255, blank=False, null=False, unique=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    
    def __str__(self) -> str:
        return f"{self.name}"

        
class DataImport(models.Model):
    dataset = models.ForeignKey(DataSet, on_delete=models.PROTECT)
    dataelement = models.ForeignKey(DataElement, on_delete=models.PROTECT)
    ornanisationunit = models.ForeignKey(OrganisatinalUnit, on_delete=models.PROTECT)
    period = models.CharField(max_length=20, blank=True)
    value = models.CharField(max_length=255, blank=True)
    comment = models.TextField(blank=True)
    followup = models.CharField(max_length=255, blank=True)
    deleted = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f"{self.period}:{self.value} -> {self.dataset.name[:10]} -> {self.dataelement.name[:10]}"
