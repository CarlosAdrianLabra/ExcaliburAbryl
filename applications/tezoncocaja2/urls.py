from django.urls import path
from . import views

app_name = "tezoncocaja2_app"

urlpatterns = [
    path('punto_de_venta/caja/2/',views.Tezoncocaja2view.as_view(),name='caja2',),
    path('punto_de_venta/caja/2/carshop/update/<pk>/', views.CarShopTezoncocaja2UpdateView.as_view(),name='carshop-update',),
    path('punto_de_venta/caja/2/carshop/update2/<pk>/', views.CarShopTezoncocaja2Update2View.as_view(),name='carshop-update2',),
    path('punto_de_venta/caja/2/carshop/delete/<pk>/', views.CarShopTezoncocaja2DeleteView.as_view(),name='carshop-delete',),
    path('punto_de_venta/caja/2/carshop/delete-all/', views.CarShopTezoncocaja2DeleteAll.as_view(),name='carshop-delete_all',),
    path('punto_de_venta/caja/2/voucher/',views.ProcesoVentaVoucherTezoncoCaja2View.as_view(),name='venta-voucher-caja2',),
    path('punto_de_venta/caja/2/voucher-pdf/<pk>/', views.VentaVoucherPdfTezoncoCaja2.as_view(),name='venta-voucher_pdf',),
    path('punto_de_venta/caja/2/efectivo/', views.Efectivotezoncocaja2View.as_view(),name='efectivo_tezoncocaja2',),
    path('punto_de_venta/caja/2/efectivo/delete-all',views.Efectivotezoncocaja2DeleteAll.as_view(),name='efectivo_tezoncocaja2-delete_all',),
    path('punto_de_venta/caja/2/promocion/familiar/',views.PromocionFamiliarTezoncoCaja2.as_view(),name='promocion_familiar',),
    path('punto_de_venta/caja/2/ventas_del_dia/', views.VentasListaView.as_view(),name='ventas_caja2',),
    path('punto_de_venta/caja/2/cancelar_venta/<pk>/', views.VentasEliminarView.as_view(),name='ventas_eliminar',),
]