from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutPage, name="logout"),
    path("register/", views.registerPage, name="register"),
    path("dashboard/", views.memberDashboard, name="dashboard"),

    path("transaction/", views.makeTransaction, name="transaction"),
    path("transaction-history/", views.transactionHistory, name="transaction-history"),

    path("loan-application/", views.loadApplication, name="loan-application"),

    # Admin
    path("admin-register/", views.adminRegisterPage, name="admin-register"),
    path("admin-dashboard/", views.adminDashboard, name="admin_dashboard"),
    path("admin-management/", views.adminManagement, name="admin_management"),
]
