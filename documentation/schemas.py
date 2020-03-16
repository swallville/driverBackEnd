from drf_yasg import openapi


def get_query_params(query_parameters):
    return [openapi.Parameter(param['name'],
            openapi.IN_QUERY,
            description=param['description'],
            required=param.get('required', None),
            type=param['type']) for param in query_parameters]


def override_path_params(path_parameters):
    return [openapi.Parameter(param['name'],
            openapi.IN_PATH,
            description=param['description'],
            required=True,
            type=openapi.TYPE_STRING) for param in path_parameters]
