import click
import pandas as pd
import os

def read_config(config_path):
    config = {}
    try:
        with open(config_path, 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    config[key.strip()] = value.strip()
    except FileNotFoundError:
        raise FileNotFoundError("Config file not found.")
    return config

def detect_delimiter(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.csv':
        return ','
    elif ext == '.tsv':
        return '\t'
    elif ext == '.txt':
        return None
    else:
        return None

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.command(context_settings=CONTEXT_SETTINGS,
               help="Transform data by removing specified columns and selecting output columns based on a config file.")
@click.option('-i','--input_path', prompt='Input file path', help='Path to the input file')
@click.option('-o','--output_path', prompt='Output file path', help='Path to save the transformed output')
@click.option('-c','--config_path', prompt='Config file path', help='Path to config.txt')
@click.option('-v','--verbose', is_flag=True, help='Enable verbose output for debugging')
def transform_data(input_path, output_path, config_path, verbose):
    if verbose:
        click.echo("[DEBUG] Starting transformation...")
        click.echo(f"[DEBUG] Input file: {input_path}")
        click.echo(f"[DEBUG] Output file: {output_path}")
        click.echo(f"[DEBUG] Config file: {config_path}")

    try:
        config = read_config(config_path)
        if verbose:
            click.echo(f"[DEBUG] Loaded config: {config}")

        remove_cols = [col.strip() for col in config.get('remove_columns', '').split(',') if col]
        output_cols = [col.strip() for col in config.get('output_columns', '').split(',') if col]
        output_delim = config.get('output_delimiter', ',')
        output_type = config.get('output_type', 'csv')

        delim_map = {'\\t': '\t', 'space': ' ', ',': ','}
        final_delim = delim_map.get(output_delim, output_delim)

        # Read input
        if input_path.endswith('.csv') or input_path.endswith('.txt'):
            df = pd.read_csv(input_path, sep=detect_delimiter(input_path),
                             engine='python', quoting=3, keep_default_na=False)
        elif input_path.endswith('.xlsx') or input_path.endswith('.xls'):
            df = pd.read_excel(input_path, engine='openpyxl')
        else:
            raise ValueError("Unsupported input format")

        if verbose:
            click.echo(f"[DEBUG] Columns before transform: {list(df.columns)}")
            click.echo(f"[DEBUG] Removing columns: {remove_cols}")
            click.echo(f"[DEBUG] Reordering columns to: {output_cols}")

        # Transform
        df.drop(columns=remove_cols, errors='ignore', inplace=True)
        df = df[output_cols]

        if verbose:
            click.echo(f"[DEBUG] Columns after transform: {list(df.columns)}")
            click.echo(f"[DEBUG] Writing output as {output_type} with delimiter '{final_delim}'")

        # Write output
        if output_type == 'csv' or output_type == 'txt':
            df.to_csv(output_path, sep=final_delim, index=False, quoting=3)
        elif output_type == 'excel':
            df.to_excel(output_path, index=False, engine='openpyxl')
        else:
            raise ValueError("Unsupported output format")

        click.echo(f"Output saved to: {output_path}")

    except Exception as e:
        click.echo(f"Error: {str(e)}")

if __name__ == '__main__':
    transform_data()