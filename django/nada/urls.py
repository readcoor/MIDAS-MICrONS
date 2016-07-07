from django.conf.urls import url
import views

CREATE_VIEWS = { 'post': 'create'}
LIST_VIEWS = { 'get': 'list'}
DETAIL_VIEWS = { 'get': 'retrieve', 'put':'update', 'delete':'destroy'}

collection_create = views.CollectionsViewSet.as_view(CREATE_VIEWS)
collection_list = views.CollectionsViewSet.as_view(LIST_VIEWS)
collection_detail = views.CollectionViewSet.as_view(DETAIL_VIEWS)

coordinateframe_create = views.CoordinateFramesViewSet.as_view(CREATE_VIEWS)
coordinateframe_list = views.CoordinateFramesViewSet.as_view(LIST_VIEWS)
coordinateframe_detail = views.CoordinateFrameViewSet.as_view(DETAIL_VIEWS)

experiment_create = views.ExperimentsViewSet.as_view(CREATE_VIEWS)
experiment_list = views.ExperimentsViewSet.as_view(LIST_VIEWS)
experiment_detail = views.ExperimentViewSet.as_view(DETAIL_VIEWS)

layer_create = views.LayersViewSet.as_view(CREATE_VIEWS)
layer_list = views.LayersViewSet.as_view(LIST_VIEWS)
layer_detail = views.LayerViewSet.as_view(DETAIL_VIEWS)

urlpatterns = [ 
    url(r'^collection/$', collection_create, name='collection-create'),
    url(r'^collections/$', collection_list, name='collection-list'),
    url(r'^collection/(?P<name>[\w_-]+)/?$', collection_detail, name='collection-detail'),

    url(r'^coordinateframe/$', coordinateframe_create, name='coordinateframe-create'),
    url(r'^coordinateframes/$', coordinateframe_list, name='coordinateframe-list'),
    url(r'^coordinateframe/(?P<name>[\w_-]+)/?$', coordinateframe_detail, name='coordinateframe-detail'),

    url(r'^experiment/$', experiment_create, name='experiment-create'),
    url(r'^experiments/$', experiment_list, name='experiment-list'),
    url(r'^experiment/(?P<collection>[\w_-]+)/(?P<name>[\w_-]+)/?$', experiment_detail, name='experiment-detail'),

    url(r'^layer/$', layer_create, name='layer-create'),
    url(r'^layers/$', layer_list, name='layer-list'),
    url(r'^layer/(?P<collection>[\w_-]+)/(?P<experiment>[\w_-]+)/(?P<name>[\w_-]+)/?$', layer_detail, name='layer-detail'),
]
