from django.db import models
from django.contrib.auth.models import User
from .choices import MemberStatus, TransactionType, TransactionStatus, LoanStatus


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    savings_balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.000, null=False, blank=False, verbose_name="Initial Savings Balance"
    )
    loan_balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.000, null=False, blank=False
    )
    status = models.CharField(
        max_length=20,
        choices=MemberStatus.choices,
        default=MemberStatus.ACTIVE,
    )
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Transaction(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=False)
    amount = models.DecimalField(
        max_digits=100000, decimal_places=3, default=0.000, null=False, blank=False
    )
    type = models.CharField(
        max_length=10,
        choices=TransactionType.choices,
    )
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=TransactionStatus.choices,
        default=TransactionStatus.PENDING,
    )

    def __str__(self):
        return f"{self.type.title()} of {self.amount} by Member {self.member.user.username} on {self.date.strftime('%Y-%m-%d')}"


class Loan(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(
        max_length=10, choices=LoanStatus.choices, default=LoanStatus.APPLIED
    )
    date_issued = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    balance_remaining = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if self._state.adding and self.balance_remaining is None:
            self.balance_remaining = self.amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Loan #{self.id} - {self.member} - {self.status}"


class Dividend(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, default=0.000, decimal_places=2)
    year = models.IntegerField()
    date_paid = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_paid"]

    def __str__(self):
        return f"Dividend {self.year} - {self.member} - {self.amount}"
