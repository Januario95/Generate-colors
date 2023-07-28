from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    register_employee , search_collaborator,
    view_all_collaborators, confirm_identity,
    collaborators_api, collaborator_api,
    binary_search, sort_array, login,
    things_to_by, things_to_by_filter,
    all_things_to_buy_by_category,
    all_things_to_buy_by_priority,
    get_categories, get_all_items,
    delete_item, get_item_by_pk,
    update_item, login, all_items_order_by,
    selenium_practie, calculate,
    distance_between_two_places,
    distance_between_two_places_api,
    color_picker, color_picker_api,
    color_search, total_colors,
    file_information,

    fraction_calculator,
    calculate_fractions,
)
from .api_views import (
    CollaboratorViewSet,
    ItemToBuyViewSet,
    CollaboratorView,
    ItemToBuyView,
    CalculatorView,
    CalculatorViewSet,
    MovieViewSet,
    ResourceViewSet,
    UserProfileViewSet,
    UserReadWriteViewSet,
    AccountViewSet,
    CommentViewSet,
)


app_name = 'portal'

router = DefaultRouter()
router.register('collaborators', CollaboratorViewSet)
router.register('items', ItemToBuyViewSet)
router.register('calculations', CalculatorViewSet)
router.register('movie', MovieViewSet)
router.register('resource', ResourceViewSet)
router.register('user', UserProfileViewSet)
router.register('user-2', UserReadWriteViewSet)
router.register('account', AccountViewSet)
router.register('comment', CommentViewSet)


urlpatterns = [
    path('calculate_fractions/<str:nume1>/<str:deno1>/<str:nume2>/<str:deno2>/<str:operator>/',
         calculate_fractions),
    path('fraction_calculator/', fraction_calculator,
         name='fraction_calculator'),
    path('file_information/', file_information,
         name='file_information'),
    path('total_colors/', total_colors),
    path('color_search/<int:limit>/', color_search),
    path('color_picker/', color_picker),
    path('color_picker_api/', color_picker_api),
    path('distance_between_two_places/',
         distance_between_two_places,
         name='distance_between_two_places'),
    path('distance_between_two_places_api/',
         distance_between_two_places_api),
    path('selenium_practice/', selenium_practie,
         name='selenium_practice'),
    path('calculate/<str:first_number>/<str:second_number>/<str:operator>/',
         calculate),
    path('login/', login, name='login'),
    path('register/', register_employee, name='register'),
    path('things_to_buy/', things_to_by, name='things_to_by'),
    path('all_items_order_by/<str:colname>/', all_items_order_by),
    
    path('search/<str:username>/', search_collaborator,
         name='search'),
    path('collaborators/', view_all_collaborators,
         name='all_collaborators'),
    path('confirm_identity/<str:username>/', confirm_identity,
         name='confirm_identity'),
    path('binary_search/', binary_search, name='binary_search'),
    path('sort_array/<str:arr>/', sort_array),
    
    path('things_to_by/<str:category>/', things_to_by_filter, name='things_to_by_filter'),
    path('all_things_to_buy_by_category/<str:category>/', all_things_to_buy_by_category),
    path('all_things_to_buy_by_priority/<str:priority>/', all_things_to_buy_by_priority),
    path('get_categories/', get_categories),
    path('get_all_items/', get_all_items),
    path('delete_item/<int:pk>/', delete_item, name='delete_item'),
    path('get_item_by_pk/<int:pk>/', get_item_by_pk),
    path('update_item/', update_item),
    # path('login/', login, name='login'),
    
    # APIs
    # path('api/collaborators/', collaborators_api),
    # path('api/collaborators/<str:first_name>/', collaborator_api),
    
    path('api/', include(router.urls)),
    path('xml/collaborators/', CollaboratorView.as_view()),
    path('xml/items/', ItemToBuyView.as_view()), 
    path('xml/calculations/', CalculatorView.as_view()),
]