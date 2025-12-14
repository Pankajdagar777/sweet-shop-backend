from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    SweetListCreateView,
    SweetDetailView,
    PurchaseSweetView,
    RestockSweetView,
    SweetSearchView
)

urlpatterns = [
    # Auth
    path('auth/register/', RegisterView.as_view(), name="register"),
    path('auth/login/', LoginView.as_view()),

    # Sweets
    path('sweets/', SweetListCreateView.as_view(), name="sweets"),
    path('sweets/<int:pk>/', SweetDetailView.as_view()),
    path('sweets/<int:pk>/purchase/', PurchaseSweetView.as_view()),
    path('sweets/<int:pk>/restock/', RestockSweetView.as_view()),
    path('sweets/search/', SweetSearchView.as_view()),
]
