from datetime import datetime
import pandas as pd
import numpy as np
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .resource import DHISAPI
from .models import (
    OrganisatinalUnit, DataSet, DataElement, OptionSet, OptionSetOption
)
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def str_value(v):
    rv = ""
    if isinstance(v, str):
        rv = v
    elif isinstance(v, int) or isinstance(v, float):
        rv = str(v)
    elif v in ["", None, np.nan] or not v:
        rv = ""
    else:
        rv = v
    if rv == 'nan':
        return ""
    return rv


@login_required
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
    pay_1 = api.send(url, data=works_values)
    
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
    
    return JsonResponse({
        "data": pay_1
    })
    
    
def upload_file(request):
    this_year = str(datetime.now().year)
    org_units = OrganisatinalUnit.objects.all()
    org_units_names = [o.name.lower().strip() for o in org_units]
    data_elems = DataElement.objects.exclude(name__iendswith="c").exclude(name__icontains="cch").all()
    payload = None
    api = DHISAPI()
    url = api.make_url(settings.DATA_VALUE_SETS, dryRun="false", importStrategy="CREATE_AND_UPDATE", force="false")
    print(url)
    
    datums = {"dataValues": []}
    x_info = {}
        
    if request.method == "POST":
        file = request.FILES['file']
        file_type = file.name.split(".")[-1] # file.name.endswith('.csv')
        if file_type == "csv":
            df = pd.read_csv(file)
            df_cols = df.columns.tolist()
            _all = []
            for col in ["DataSet", "DataElement", "Period", "OrgUnit", "Value", "Comment"]:
                if col in df_cols:
                    _all.append(True)
                else:
                    _all.append(False)
            if all(_all):
                for _, row in df.iterrows():
                    datums["dataValues"].append({
                        "dataSet": str_value(row["DataSet"]),
                        "completeDate": "",
                        "dataElement": str_value(row["DataElement"]),
                        "period": str_value(row["Period"]),
                        "orgUnit": str_value(row["OrgUnit"]),
                        "value": str_value(row["Value"]),
                        "comment": str_value(row["Comment"])
                    })
                
        elif file_type in ["xlsx", "xls"]:
            
            # df = pd.read_excel(file, sheet_name=sheets_subset, usecols=column_subset)
            dfs = pd.read_excel(file, sheet_name=None)
            unique_time_periods = []
            indicators = {}
            for sheet_name, sheet_goal in dfs.items():
                if not sheet_name.lower().startswith("goal"):
                    continue
                
                print(f"Processing sheet: {sheet_name}")
                
                for tp in sheet_goal['TimePeriod'].unique():
                    if tp not in unique_time_periods:
                        unique_time_periods.append(tp)
                
                sheet_goal = sheet_goal.sort_values(by=['GeoAreaName', 'TimePeriod'], ascending=False)
                for _, sh_row in sheet_goal.iterrows():
                    # if sh_row.GeoAreaName.lower().strip() in org_units_names and sh_row.TimePeriod == 2022:
                    if sh_row.GeoAreaName.lower().strip() in org_units_names:
                        exists = list(filter(lambda de: str(sh_row.Indicator).strip() in de.name, data_elems))
                        if exists:
                            if sh_row.Indicator not in indicators:
                                indicators[sh_row.Indicator] = []
                                
                            old = dict(sh_row)
                            for k, v in sh_row.items():
                                old[k] = str_value(v)
                                
                            indicators[sh_row.Indicator].append(old)
                            
            # for k, v in indicators.items():
            #     delem = data_elems.filter(name__icontains=str(k)).first()
            #     if len(v) > 0:
            #         print(f"{k} : {len(v)}")
            #         for ou in org_units_names:
            #             selected = list(filter(lambda x: x["GeoAreaName"].lower().strip() == ou, v))
            #             _xsel = [_x['SeriesDescription'] for _x in selected]
            #             _xsel.insert(0, delem.name)
            #             if len(selected) > 0:
            #                 print(f"{ou} : {len(selected)}")
            #                 vectorizer = TfidfVectorizer()
            #                 vectors = vectorizer.fit_transform(_xsel)
            #                 similarity = cosine_similarity(vectors[0], vectors[1:])
            #                 most_similar_index = similarity.argmax()
            #                 perc = similarity[0, most_similar_index]
                            
            #                 _xsel = _xsel[1:]
            #                 desc = _xsel[most_similar_index]
            #                 print("--------------------------------------------")
            #                 print("--------------------------------------------")
            #                 print(delem.name)
            #                 print(f"Best - {perc} - {desc}")
            #                 print("--------------------------------------------")
            #                 for index, _xs in enumerate(_xsel):
            #                    print(f"{similarity[0, index]} : {_xs}") 
            #                 print("\n")
                 
            print(f"Indicator keys {len(indicators.keys())}")
            for k, v in indicators.items():
                tracked_indicator = data_elems.filter(name__icontains=str(k)).first()
                if len(v) > 0 and tracked_indicator:
                    print(f"\n\nIndicator {k} : All Possible mappings fr all time periods --> {len(v)}")
                    for ou in org_units_names:
                        for tp in unique_time_periods:
                            # filter those that belong to this org unit and time period
                            filtrate = list(
                                filter(
                                    lambda x: x["GeoAreaName"].lower().strip() == ou and str(x["TimePeriod"]) == str(tp), 
                                    v
                                )
                            )
                            if len(filtrate) > 0: 
                                org_unit = org_units.filter(name__iexact=ou).first()
                                print(f"**{tp} Mappings for [{ou}] --> {len(filtrate)}  --> picking first ")
                                
                                if k not in x_info:
                                    x_info[k] = {} 
                                if ou not in x_info[k]:
                                    x_info[k][ou] = {}
                                    
                                x_info[k][ou]["possibles"] = filtrate
                                _maybe = filtrate[0]
                                x_info[k][ou]["selected"] = _maybe
                                
                                datums["dataValues"].append({
                                    "dataSet": tracked_indicator.dataset.dhis_id,
                                    "completeDate": "",
                                    "dataElement": tracked_indicator.dhis_id,
                                    "period": str_value(_maybe["TimePeriod"]),
                                    "orgUnit": org_unit.dhis_id,
                                    "value": str_value(_maybe["Value"]),
                                    "comment": ""
                                })
        ld = len(datums['dataValues'])
        print(f"Datums: {ld}")
        if ld <= 0:
            payload = {
                "success": False,
                'error': "No data to send"
            }
        else:
            try:
                payload = api.send(url, data=datums)
                payload = {
                    "success": True,
                    **payload,
                }
            except Exception as e:
                payload = {
                    "success": False,
                    'error': e
                }
            
    print(url)
                          
    return JsonResponse({
        **payload,
        "extra": x_info,
        "datums": datums
    })
