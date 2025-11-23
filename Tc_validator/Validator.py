import pandas as pd
import os
import click

def validate_data(df):
    errors = pd.DataFrame()
    error_indices = set()

    # 1. Missing Name
    missing_name = df[df["Name"].isnull()]
    if not missing_name.empty:
        missing_name = missing_name.copy()
        missing_name.loc[:, "Error"] = "Missing Name"
        errors = pd.concat([errors, missing_name])
        error_indices.update(missing_name.index)

    # 2. Invalid StartDate
    invalid_dates = df[~df["StartDate"].str.match(r"\d{4}-\d{2}-\d{2}", na=False)]
    if not invalid_dates.empty:
        invalid_dates = invalid_dates.copy()
        invalid_dates = invalid_dates[~invalid_dates.index.isin(error_indices)]
        invalid_dates.loc[:, "Error"] = "Invalid StartDate Format"
        errors = pd.concat([errors, invalid_dates])
        error_indices.update(invalid_dates.index)

    # 3. Duplicate Rows
    duplicates = df[df.duplicated(keep=False)]
    duplicate_errors = df[df.duplicated(keep='first')]  # Only keep non-first as errors
    duplicate_errors = duplicate_errors[~duplicate_errors.index.isin(error_indices)]
    if not duplicate_errors.empty:
        duplicate_errors = duplicate_errors.copy()
        duplicate_errors.loc[:, "Error"] = "Duplicate Row"
        errors = pd.concat([errors, duplicate_errors])
        error_indices.update(duplicate_errors.index)

    return errors

@click.command()
@click.option('--input', '-i', required=True, type=click.Path(exists=True), help='Path to input CSV file')
@click.option('--output', '-o', required=True, type=click.Path(), help='Path to save error report CSV')
@click.option('--log', '-l', default='logs/validation_log.txt', show_default=True, help='Path to save validation log')
def main(input, output, log):
    """Validate Teamcenter migration data. Output errors to CSV and optional log."""
    try:
        df = pd.read_csv(input)
        errors = validate_data(df)

        if os.path.isdir(output):
            cleaned_file = os.path.join(output, "clean_data.csv")
        else:
            base = os.path.splitext(output)[0]
            cleaned_file = base + "_clean.csv"

        # Create clean data
        valid_data = df.drop(errors.index)

        # Save clean data
        os.makedirs(os.path.dirname(cleaned_file), exist_ok=True)
        valid_data.to_csv(cleaned_file, index=False)

        # Save error log with full invalid records
        if not errors.empty:
            os.makedirs(os.path.dirname(log), exist_ok=True)
            with open(log, "w") as f:
                f.write("Validation Errors Found:\n\n")
                f.write(errors.to_string(index=False))
            click.echo(f"⚠️  {len(errors)} invalid records logged to: {log}")

        click.echo(f"✅ {len(valid_data)} valid records saved to: {cleaned_file}")

    except Exception as e:
        click.echo(f"❌ Error during validation: {e}")

if __name__ == "__main__":
    main()
