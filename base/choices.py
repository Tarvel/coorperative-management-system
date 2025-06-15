from django.db import models


class MemberStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"


class TransactionType(models.TextChoices):
    DEPOSIT = "deposit", "Deposit"
    WITHDRAWAL = "withdrawal", "Withdrawal"


class TransactionStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    COMPLETED = "completed", "Completed"


class LoanStatus(models.TextChoices):
    APPLIED = "applied", "Applied"
    ACTIVE = "active", "Active"
    REPAID = "repaid", "Repaid"
