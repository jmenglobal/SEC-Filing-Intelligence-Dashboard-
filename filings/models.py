from django.db import models
from django.forms import DateTimeField

class Company(models.Model):
  cik = models.CharField(max_length=10, primary_key=True, db_index=True)
  name = models.CharField(max_length=255)
  ticker = models.CharField(max_length=10, blank=True, null=True, db_index=True)
  sic_code = models.CharField(max_length=4)
  industry = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)  

class Filing(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    form_type = models.CharField(max_length=10) # 10-K, 10-Q, 8-K
    filing_date = models.DateField()
    accession_number = models.CharField(max_length=20, unique=True)
    document_url = models.URLField()
    raw_text = models.TextField()
    processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class FilingSection(models.Model):
    id = models.AutoField(primary_key=True)
    filing = models.ForeignKey(Filing, on_delete=models.CASCADE)
    section_type = models.CharField(max_length=255) # "Risk Factors", "MD&A", etc.
    content = models.TextField()
    word_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class KeywordAlert(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=255)
    section = models.CharField(max_length=255)
    filing = models.ForeignKey(Filing, on_delete=models.CASCADE)
    context_snippet = models.TextField()
    detected_at = models.DateTimeField()

class ChangeDetection(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    section_type = models.CharField(max_length=255)
    previous_filing = models.ForeignKey(Filing, on_delete=models.CASCADE, related_name='previous_filing')
    current_filing = models.ForeignKey(Filing, on_delete=models.CASCADE, related_name='current_filing')
    similarity_score = models.FloatField()
    key_differences = models.JSONField()
    detected_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.company.name} - {self.section_type}"
