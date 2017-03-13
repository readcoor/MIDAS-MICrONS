from rest_framework import response, schemas
from rest_framework.decorators import api_view, renderer_classes
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

from django.db import connection
from django.http import HttpResponse, HttpResponseServerError
from nada.models import Neuron, Synapse


@api_view()
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Wyss MICrONS API')
    full_schema = generator.get_schema(request=request)
    uri = request._request.get_raw_uri()
    full_schema._url=uri[:uri.find('/docs/')]
    return response.Response(full_schema.delete('docs'))


def index(request):
    return HttpResponse('<p>Hello, world.</P> <P>View the API <a href="/docs">here</a></P>')

def health_check(request):
    '''Return 200 to tell Elastic Beanstalk that everything is ok'''
    try: 
        check_table_exists(Neuron)
        check_table_exists(Synapse)
        return HttpResponse('System health appears to be ok')
    except Exception as err:
        return HttpResponseServerError(err)

def check_table_exists(model_class):
    table_name = model_class._meta.db_table
    with connection.cursor() as cursor:
        q = 'SELECT * FROM information_schema.tables WHERE table_name = %s'
        cursor.execute(q, [table_name])
        row = cursor.fetchone()
        if row == None:
            raise Exception('Cannot find table "{}" in database'.format(table_name))
