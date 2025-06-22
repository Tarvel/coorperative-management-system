from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutPage, name="logout"),
    path("register/", views.registerPage, name="register"),
    path("dashboard/", views.memberDashboard, name="dashboard"),

    path("transaction/", views.makeTransaction, name="transaction"),
    path("transaction-history/", views.transactionHistory, name="transaction-history"),

    path("loan-application/", views.loanApplication, name="loan-application"),

    # Notification
    path("clear_notifications/", views.clear_notifications, name="clear_notifications"),
    path("mark_notification_read/<str:pk>", views.mark_notification_read, name="mark_notification_read"),

    # Admin
    path("admin-register/", views.adminRegisterPage, name="admin_register"),
    path("admin-login/", views.adminLoginPage, name="admin_login"),
    path("admin-dashboard/", views.adminDashboard, name="admin_dashboard"),
    path("admin-management/", views.adminManagement, name="admin_management"),
    path("view-member/<str:username>", views.viewMember, name="view_member"),
    path("approve_transaction/<str:username>/<str:pk>", views.approve_transaction, name="approve_transaction"),
    path("reject_transaction/<str:username>/<str:pk>", views.reject_transaction, name="reject_transaction"),
    path("manage-transactions", views.transactionManagement, name="admin_transaction_management"),
    path("cooperative_report/", views.coorperativeReport, name="cooperative_report"),
]
