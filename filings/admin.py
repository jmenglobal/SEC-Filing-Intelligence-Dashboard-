from django.contrib import admin

# Register your models here.
from .models import Company, Filing, FilingSection


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['cik', 'name', 'ticker', 'industry']
    search_fields = ['name', 'ticker', 'cik']

@admin.register(Filing)
class FilingAdmin(admin.ModelAdmin):
    list_display = ['company', 'form_type', 'filing_date', 'processed']
    list_filter = ['form_type', 'processed', 'filing_date']
    search_fields = ['company__name', 'accession_number']