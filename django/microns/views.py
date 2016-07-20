from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response, schemas
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

@api_view()
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Wyss MICrONS API')
    full_schema = generator.get_schema(request=request)
    uri = request._request.get_raw_uri()
    full_schema._url=uri[:uri.find('/docs/')]
    return response.Response(full_schema.delete('docs'))

