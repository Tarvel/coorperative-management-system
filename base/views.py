from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Member, User, Dividend, Transaction, Loan
from .forms import UserCreationForm, TransactionForm, CustomUserCreationForm


def registerPage(request):
    page = "register"
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST, Member)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            member, created = Member.objects.get_or_create(user=request.user)
            next_url = request.GET.get("next") or "dashboard"
            if next_url == "admin_management":
                messages.info(request, f"{user.username} has been added")
            return redirect(next_url)

    context = {"page": page, "form": form}
    return render(request, "base/login.html", context)


def adminRegisterPage(request):
    page = "register"
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            member, created = Member.objects.get_or_create(user=user)

            login(request, user)
            return redirect("dashboard")

    context = {"page": page, "form": form}
    return render(request, "base/login.html", context)


def loginPage(request):
    page = "login"
    if request.method == "POST":
        username = request.POST.get("username")
        username = username.lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Username is not registered")
            return redirect("login")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get("next") or "dashboard"
            return redirect(next_url)
        else:
            messages.error(request, "Incorrect password")
            return redirect("login")

    context = {"page": page}

    return render(request, "base/login.html", context)


def logoutPage(request):
    logout(request)
    return redirect("dashboard")


@login_required(login_url="login")
def memberDashboard(request):
    user = User.objects.get(username=request.user.username)
    member = Member.objects.filter(user=user).first()
    dividends = Dividend.objects.filter(member=member).all()[0:4]
    transactions = Transaction.objects.filter(member=member).all()[0:4]

    pending = ["yes" if "pending" in status.status else "no" for status in transactions]

    context = {
        "member": member,
        "dividends": dividends,
        "transactions": transactions,
        "pending": pending,
    }
    return render(request, "base/member-dashbord.html", context)


@login_required(login_url="login")
def makeTransaction(request):
    form = TransactionForm(instance=request.user)
    member = Member.objects.filter(user=request.user).first()

    if request.method == "POST":
        amount = request.POST.get("amount")
        amount = Decimal(amount)
        transaction_type = request.POST.get("transaction_type")
        if member.loan_balance <= 0.00:
            if transaction_type == "withdrawal":
                if member.savings_balance >= 10:
                    transaction = Transaction.objects.create(
                        member=member,
                        amount=amount,
                        type=transaction_type,
                    )
                    messages.info(
                        request,
                        f"Your {transaction_type} in now pending, please wait while the admin approves it",
                    )
                    return redirect("dashboard")
                else:
                    messages.error(
                        request,
                        f"Your {transaction_type} cannot be processed due to insufficient balance",
                    )
                    return redirect("dashboard")

            else:
                transaction = Transaction.objects.create(
                    member=member,
                    amount=amount,
                    type=transaction_type,
                )
                messages.info(
                    request,
                    f"Your {transaction_type} in now pending, please wait while the admin approves it",
                )
                return redirect("dashboard")

        else:
            if member.savings_balance >= 10 and transaction_type == "deposit":
                transaction = Transaction.objects.create(
                    member=member,
                    amount=amount,
                    type=transaction_type,
                )
                messages.info(
                    request,
                    f"Your {transaction_type} in now pending, please wait while the admin approves it",
                )
                return redirect("dashboard")

            else:
                messages.error(
                    request,
                    f"Your {transaction_type} cannot be processed due to unpaid loan",
                )
            return redirect("dashboard")

    context = {"form": form}
    return render(request, "base/transaction_form.html", context)


@login_required(login_url="login")
def transactionHistory(request):
    selected_type = request.GET.get("type") if request.GET.get("type") != None else ""
    selected_status = (
        request.GET.get("status") if request.GET.get("status") != None else ""
    )
    selected_date = request.GET.get("date") if request.GET.get("date") != None else ""

    member = Member.objects.filter(user=request.user).first()
    transaction = member.transaction_set.all()
    print(
        f"get type: {selected_type}, get status: {selected_status}, get date:{selected_date}"
    )
    filters = Q()

    if selected_type != "all" and selected_type.strip():
        filters &= Q(type__iexact=selected_type)

    if selected_status != "all" and selected_status.strip():
        filters &= Q(status__iexact=selected_status)

    if selected_date.strip():
        filters &= Q(date__date=selected_date)

    transaction_list = transaction.filter(filters).order_by("-date")

    paginator = Paginator(transaction_list, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}
    return render(request, "base/transaction_history.html", context)


@login_required(login_url="login")
def loadApplication(request):
    member = Member.objects.filter(user=request.user).first()
    if member.status == "active":
        if member.loan_balance > 0:
            messages.error(
                request,
                "You are unable to apply for a loan due to outstanding loan balance",
            )
            return redirect("dashboard")

        if member.savings_balance >= 10:
            if request.method == "POST":
                amount = request.POST.get("amount")
                interest_rate = request.POST.get("interest_rate")
                loan = Loan.objects.create(
                    member=member,
                    amount=amount,
                    interest_rate=interest_rate,
                )
                messages.info(
                    request,
                    "You have applied for a loan,  please wait while the admin approves it",
                )
                return redirect("dashboard")
        else:
            messages.error(
                request,
                "You are unable to apply for a loan due to insufficient balance",
            )
            return redirect("dashboard")
    else:
        messages.error(request, "You are unable to apply for a loan due to inactivity")
        return redirect("dashboard")

    return render(request, "base/loan_application_form.html")


@staff_member_required
def adminDashboard(request):
    # current_member = Member.objects.filter(user=request.user).first()
    # if not current_member.user.is_staff:
    #     messages.error(request, "You are not authorized to view this page")
    #     return redirect("dashboard")
    members = Member.objects.all()
    transactions = Transaction.objects.all()
    loans = Loan.objects.all()

    total_savings = sum(Decimal(member.savings_balance) for member in members)
    total_loans_outstanding = sum(Decimal(member.loan_balance) for member in members)
    pending_transactions = sum(
        1 for transaction in transactions if transaction.status == "pending"
    )
    pending_loans = sum(1 for loan in transactions if loan.status == "applied")

    context = {
        "members": members,
        "total_savings": total_savings,
        "total_loans_outstanding": total_loans_outstanding,
        "pending_transactions": pending_transactions,
        "pending_loans": pending_loans,
    }
    return render(request, "base/admin-dashboard.html", context)


@staff_member_required
def adminManagement(request):
    form = UserCreationForm()
    members = Member.objects.all().order_by("-created_at")
    paginator = Paginator(members, 4)
    page_number = request.GET.get("page")
    page_obg = paginator.get_page(page_number)
    password = "default_password"
    context = {
        "password": password,
        "form": form,
        "page_obj": page_obg,
    }
    return render(request, "base/admin_member_management.html", context)
