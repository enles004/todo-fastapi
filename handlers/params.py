

def filtering(data_filter_params):
    filters = {}
    for field in data_filter_params.keys():
        value = data_filter_params[field]
        if isinstance(value, dict):
            if "$contains" in value:
                filters.update({field: {"$regex": "{}".format(value["$contains"]), "$options": "i"}})
            elif "$equal" in value:
                filters.update({field: {"$regex": "/{}/".format(value["$equal"])}})
            else:
                return {"message": "invalid input"}
        else:
            filters.update({field: value})
    return filters

