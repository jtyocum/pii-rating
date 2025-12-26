# README

Script to convert identified types of PII into a qualitative rating: HIGH, MEDIUM, LOW.

## Usage

```bash
uv run pii-rating.py <list_file>
```

Where `list_file` is a text file containing a newline‑separated list of files and their associated PII types

### Example

Create a file named `files_to_rate.txt`:

```text
/home/jtyocum/temp_pii_scan/passport.jpg: []
/home/jtyocum/temp_pii_scan/sexual_preferences.docx: []
/home/jtyocum/temp_pii_scan/enron-sample.mbox: ["DATE_TIME", "EMAIL_ADDRESS", "IP_ADDRESS", "LOCATION", "NRP", "PERSON", "PHONE_NUMBER", "UK_NHS", "URL", "US_BANK_NUMBER", "US_DRIVER_LICENSE", "US_PASSPORT", "US_SSN"]
/home/jtyocum/temp_pii_scan/pii--50_names-50_ssns-50_us_drivers_licenses.xlsx: ["DATE_TIME", "LOCATION", "PERSON", "PHONE_NUMBER", "US_BANK_NUMBER", "US_DRIVER_LICENSE", "US_ITIN", "US_PASSPORT", "US_SSN"]
/home/jtyocum/temp_pii_scan/telephone-owned-property.xlsx: ["DATE_TIME", "LOCATION", "PERSON", "PHONE_NUMBER"]
/home/jtyocum/temp_pii_scan/lyrics.txt: ["DATE_TIME"]
/home/jtyocum/temp_pii_scan/pii-support-ticket-us-ssn.txt: ["DATE_TIME", "PERSON", "US_SSN"]
/home/jtyocum/temp_pii_scan/NOT_pii--names-NOT_ssns-NOT_us_drivers_licenses.xlsx: ["DATE_TIME", "LOCATION", "PERSON", "PHONE_NUMBER", "US_BANK_NUMBER", "US_DRIVER_LICENSE", "US_ITIN", "US_PASSPORT", "US_SSN"]
/home/jtyocum/temp_pii_scan/ip-creditcard-email.csv: ["CREDIT_CARD", "DATE_TIME", "EMAIL_ADDRESS", "IP_ADDRESS", "LOCATION", "NRP", "PERSON", "PHONE_NUMBER", "URL", "US_BANK_NUMBER", "US_DRIVER_LICENSE"]
/home/jtyocum/temp_pii_scan/bank_form.pdf: ["DATE_TIME", "IBAN_CODE", "LOCATION", "PERSON", "PHONE_NUMBER"]
/home/jtyocum/temp_pii_scan/pii-test.docx: ["PHONE_NUMBER", "US_SSN"]
/home/jtyocum/temp_pii_scan/health_report.pdf: ["DATE_TIME", "EMAIL_ADDRESS", "LOCATION", "NRP", "PERSON", "PHONE_NUMBER", "UK_NHS", "URL", "US_BANK_NUMBER", "US_DRIVER_LICENSE"]
/path/not/valid: NOTFOUND
```

Run the script:

```bash
uv run pii-rating.py files_to_rate.txt
```

## Ratings

The entity type identifiers the script is looking for, are those used by [Microsoft Presidio](https://microsoft.github.io/presidio/). The rating itself, was generated using Internet sources, and the aid of Microsoft Copilot. These ratings aren't perfect, they are merely guide to help judge the overall risk associated with a collection of files.
