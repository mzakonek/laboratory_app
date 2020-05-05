from django.urls import include, path

from .views import laboratory, specialists, patients
from cart.views import CartItemDeleteView, cart_details_view, CartItemUpdateView
from orders.views import order_checkout, UserOrdersListView, OrdersListView, edit_order_items, OrdersDetailView


from decorator_include import decorator_include
from django.contrib.auth.decorators import login_required
from users.decorators import specialist_required, patient_required


urlpatterns = [
    path('', laboratory.home, name='home'),

    path('specialists/', decorator_include(
        (login_required, specialist_required), include(
            (
                [
                    path('surveys/', specialists.SurveyListView.as_view(), name='survey_list'),
                    path('surveys/add/', specialists.SurveyCreateView.as_view(), name='survey_add'),
                    path('surveys/<int:pk>/update/', specialists.AssignParamsToSurveyView.as_view(),
                       name='survey_update'),
                    path('surveys/<int:pk>/delete/', specialists.SurveyDeleteView.as_view(),
                       name='survey_delete'),
                    path('parameters/add/', specialists.ParameterCreateView.as_view(),
                       name='parameter_add'),

                    path('orders/', OrdersListView.as_view(), name='orders_list'),
                    path('orders/<int:pk>/', OrdersDetailView.as_view(), name='orders_detail'),
                    path('orders/orderitem/<int:pk>/', CartItemUpdateView.as_view(), name='orders_items_update'),

                ],
                'laboratory'
            ),
            namespace='specialists'
        )
    )),


    path('patients/', decorator_include(
        (login_required, patient_required), include(([
            path('surveys/', patients.SurveyListView.as_view(), name='survey_list'),
            path('surveys/<int:pk>/', patients.OrderSurveyWithParams.as_view(), name='survey_order'),
            path('cart/', cart_details_view, name='cart_details'),
            path('cart/delete_item/<int:pk>/', CartItemDeleteView.as_view(), name='cart_item_delete'),
            path('order/checkout/', order_checkout, name='order_checkout'),
            path('order/history/', UserOrdersListView.as_view(), name='order_list')
        ], 'laboratory'), namespace='patients'))),

]
