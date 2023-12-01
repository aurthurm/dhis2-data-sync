from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from .resource import DHISAPI
from .models import (
    OrganisatinalUnit, DataSet, DataElement, OptionSet, OptionSetOption
)


def home(request):
    return render(request,'scrapper/home.html', context={})


def update_metadata(request):
    api = DHISAPI()
    
    if request.method == 'POST':
        # target = request.POST.get('target', None)
        # # if target is None:
        # #     return
        
        # if target == settings.ORG_UNITS:
        url = api.make_url(f"{settings.ORG_UNITS}.json", fields=settings.ORG_UNITS_FIELDS, pageSize=100)
        payloads = api.fetch(url, reset_store=True)
        for _payload in payloads:
            data = _payload.get(settings.ORG_UNITS, None)
            for item in data:
                org_unit, _ = OrganisatinalUnit.objects.get_or_create(dhis_id=item.get("id", None))
                org_unit.name = item.get("name", None)
                org_unit.save()
        
        # if target == settings.OPTION_SETS:
        url = api.make_url(f"{settings.OPTION_SETS}.json", fields=settings.OPTION_SETS_FIELDS, pageSize=100)
        payloads = api.fetch(url, reset_store=True)
        for _payload in payloads:
            data = _payload.get(settings.OPTION_SETS, None)
            for item in data:
                optionset, _ = OptionSet.objects.get_or_create(dhis_id=item.get("id", None))
                optionset.name = item.get("name", None)
                optionset.save()
                for opt in item.get("options", []):
                    opsetoption, _ = OptionSetOption.objects.get_or_create(
                        
                        dhis_id=opt.get("id", None)
                    )
                    opsetoption.optionset=optionset
                    opsetoption.name = opt.get("name", None)
                    opsetoption.save()
                    
        # if target == settings.DATA_SETS:
        url = api.make_url(f"{settings.DATA_SETS}.json", fields=settings.DATA_SETS_FIELDS)
        payloads = api.fetch(url)
        for _payload in payloads:
            data = _payload.get(settings.DATA_SETS, None)
            for item in data:
                data_set, _ = DataSet.objects.get_or_create(dhis_id=item.get("id", None))
                data_set.name = item.get("name", None)
                data_set.save()
                
        datasets = DataSet.objects.all()
        dse = []
        for _dataset in datasets:
            _ds = {
                "id": _dataset.dhis_id,
                "name": _dataset.name,
                "elements": []
            }
            url = api.make_url(
                f"{settings.DATA_SETS}/{_dataset.dhis_id}.json", 
                fields=settings.DATA_SET_ELEMENTS_FIELDS
            )
            
            payloads = api.fetch(url)
            for _payload in payloads:
                data = _payload.get(settings.DATA_SET_ELEMENTS, None)
                for item in data:
                    for k, v in item.items():
                        assert k == settings.DATA_ELEMENT
                        data_elen, _ = DataElement.objects.get_or_create(
                            dhis_id=v.get("id", None)
                        )
                        data_elen.dataset=_dataset
                        data_elen.name = v.get("name", None)
                        data_elen.save()
                        _ds["elements"].append({
                            "id": data_elen.dhis_id,
                            "name": data_elen.name,
                        })
            _ds["elements"] = len(_ds["elements"])
            dse.append(_ds)
    

    return JsonResponse({
        "messages": {
            "notification": "Metadata was updated successfully",
            settings.ORG_UNITS: OrganisatinalUnit.objects.count(),
            settings.DATA_SETS: datasets.count(),
            settings.DATA_SET_ELEMENTS: dse
        },
    })


def update_data_value_sets(request):
    api = DHISAPI()

    # parameters
    # dryRun	false | true	Whether to save changes on the server or just return the import summary.
    # importStrategy	CREATE | UPDATE | CREATE_AND_UPDATE | DELETE	Save objects of all, new or update import status on the server.
    # force	false | true	Indicates whether the import should be forced. 
    url = api.make_url(settings.DATA_VALUE_SETS, dryRun="false", importStrategy="CREATE_AND_UPDATE", force="false")
    
    # send a set of related data values sharing the same period and organisation unit
    works_values = {
        "dataSet": "SvvPZlVq8f7",
        "completeDate": "2023-11-11",
        "period": "2023",
        "orgUnit": "y1RAopexuHW",
        "attributeOptionCombo": "",
        "dataValues": [
            { 
                "dataElement": "S6tMEo5S7rH",
                "categoryOptionCombo": "",
                "value": 245,
                "comment": "updated via API"
            },
            {
                "dataElement": "MGo0QB7uHhu",
                "categoryOptionCombo": "",
                "value": "This is very much amazing though",
                "comment": "updated via API"
            },
        ]
    }   
    example_cmb = {
        "dataSet": "SvvPZlVq8f7",
        "completeDate": "2023-11-11",
        "period": "2023",
        "orgUnit": "y1RAopexuHW",
        "attributeOptionCombo": "",
        "dataValues": [
            { 
                "dataElement": "sQtdMWFElAa",
                "categoryOptionCombo": "",
                "optionSet": "oVwTt4sIpbB",
                "value": "FeQvajMbY1L",
                "comment": "updated via API"
            },
            {
                "dataElement": "ySklKcMVkRc",
                "categoryOptionCombo": "",
                "value": "Yay finally got uh",
                "comment": "updated via API"
            },
        ]
    }
    pay_1 = api.send(url, data=example_cmb)
    
    # send large bulks of data values which don't necessarily are logically related.
    # example = {
    #     "dataValues": [
    #         {
    #         "dataElement": "f7n9E0hX8qk",
    #         "period": "201401",
    #         "orgUnit": "DiszpKrYNg8",
    #         "value": "12"
    #         },
    #         {
    #         "dataElement": "f7n9E0hX8qk",
    #         "period": "201401",
    #         "orgUnit": "FNnj3jKGS7i",
    #         "value": "14"
    #         },
    #     ]
    # }
    
    # pay_1 = api.send(url, data=example)
    
    return JsonResponse({
        "data": pay_1
    })