Columns_to_remove
A Python CLI tool to transform tabular data by removing specified columns, reordering output columns, and saving results in CSV, TXT, or Excel formats. Configuration is driven by a simple config.txt file.

Features
* Remove unwanted columns from input files
* Select and reorder output columns
* Support for multiple delimiters (comma, tab, space)
* Output to CSV, TXT, or Excel
* Verbose mode for debugging transformations
* Short and long CLI flags (-i / --input_path, etc.)
* Config-driven workflow for flexibility

Installation
* Clone or download this repository.
* Install dependencies:
pip install pandas click openpyxl



Usage
Run the script from the command line:
python Columns_to_remove.py -i <input_file> -o <output_file> -c <config_file> [--verbose]

Options
|  |  |  | 
| -i | --input_path |  | 
| -o | --output_path |  | 
| -c | --config_path |  | 
| -v | --verbose |  | 
| -h | --help |  | 



Config File Format (config.txt)
Example:
remove_columns=email,remarks
output_columns=id,name,city,salary,department
output_delimiter=\t
output_type=csv


* remove_columns → Comma-separated list of columns to drop
* output_columns → Comma-separated list of columns to keep and reorder
* output_delimiter → , (comma), \t (tab), or space
* output_type → csv, txt, or excel

 
Examples
Example 1: CSV Input → TXT Output
python Columns_to_remove.py -i input.csv -o output.txt -c config.txt --verbose

Example 2: Excel Input → CSV Output
python Columns_to_remove.py -i data.xlsx -o result.csv -c config.txt -v

Example 3: Using Long Flags
python Columns_to_remove.py --input_path input.csv --output_path output.csv --config_path config.txt --verbose


Debugging with Verbose Mode
When --verbose is enabled, you’ll see detailed logs:
[DEBUG] Input file: input.csv
[DEBUG] Output file: output.txt
[DEBUG] Config file: config.txt
[DEBUG] Loaded config: {...}
[DEBUG] Columns before transform: [...]
[DEBUG] Removing columns: [...]
[DEBUG] Columns after transform: [...]
Output saved to: output.txt



Notes
* Always provide a valid output filename with extension (.csv, .txt, .xlsx).
* Ensure openpyxl is installed if working with Excel files.
* Large datasets are supported; performance depends on system memory.
