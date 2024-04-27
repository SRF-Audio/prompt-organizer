import os
import sys
import argparse
from datetime import datetime

# Define the path for the outputs directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUTS_DIR = os.path.join(SCRIPT_DIR, 'outputs')

def ensure_outputs_dir():
    """Ensure the 'outputs' directory exists next to the script's directory."""
    if not os.path.exists(OUTPUTS_DIR):
        os.makedirs(OUTPUTS_DIR)

def create_aggregate_file():
    """Create a new .txt file in 'outputs' with a timestamp."""
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    filename = os.path.join(OUTPUTS_DIR, f'gpt-prompt-code-{timestamp}.txt')
    return filename

def is_valid_file_extension(filename):
    """Check if the file has a valid text-based extension."""
    valid_extensions = ['.py', '.js', '.jsx', '.html', '.css', '.go', '.yaml', '.yml', '.sh', '.tf', '.tfvars']
    return any(filename.endswith(ext) for ext in valid_extensions)

def get_files_from_directory(directory_path):
    """Recursively collect all valid files from the given directory."""
    for root, _, files in os.walk(directory_path):
        for file in files:
            if is_valid_file_extension(file):
                yield os.path.join(root, file)

def aggregate_contents(paths, output_file):
    """Aggregate the contents of given files into the output file, only if they have valid extensions."""
    with open(output_file, 'w') as outfile:
        for path in paths:
            if not is_valid_file_extension(path):
                print(f"Skipping non-code file: {path}")
                continue

            try:
                with open(path, 'r') as infile:
                    outfile.write(f'{path}:\n```\n{infile.read()}\n```\n\n')
            except UnicodeDecodeError:
                print(f"Error reading file (possible binary): {path}")
            except Exception as e:
                print(f"Error processing file {path}: {e}")

def main():
    parser = argparse.ArgumentParser(description='Aggregate code files into a single .txt file for use during LLM prompts.')
    parser.add_argument('-d', '--directory', action='append', type=str, help='Specify directories containing the files to aggregate. Paths must be absolute. Multiple directories can be specified.')
    parser.add_argument('-f', '--files', nargs='+', action='append', help='Specify individual file paths to aggregate. Paths must be absolute. Multiple file sets can be specified.')
    
    args = parser.parse_args()
    
    file_paths = []
    if args.directory:
        for directory in args.directory:
            file_paths.extend(get_files_from_directory(directory))
    if args.files:
        for files_list in args.files:
            file_paths.extend(files_list)
    
    ensure_outputs_dir()
    output_file = create_aggregate_file()
    aggregate_contents(file_paths, output_file)

    print(f'Aggregated content written to {output_file}')

if __name__ == '__main__':
    main()
