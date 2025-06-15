from django.contrib import admin
from .models import Member, Transaction, Loan, Dividend

admin.site.register(Member)
admin.site.register(Transaction)
admin.site.register(Loan)
admin.site.register(Dividend)
