# Teamcenter Data Validator

A Python utility to validate data before migrating it to Siemens Teamcenter.  
This tool detects:
- Missing mandatory fields
- Invalid date formats
- Duplicate records (keeps one, flags the rest)

## Features

✅ Command-line interface using Click  
✅ Cleaned valid data saved as `clean_data.csv`  
✅ Invalid data logged to `validation_log.txt`  
✅ Easy to customize and extend

## Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
