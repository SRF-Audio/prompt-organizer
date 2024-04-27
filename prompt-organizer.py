import os
import sys
import argparse
from datetime import datetime

# Define the top-level path as a constant
TOP_LEVEL_PATH = os.path.expanduser('~/GitLab/nexgen/')

def ensure_outputs_dir():
    """Ensure the 'outputs' directory exists."""
    if not os.path.exists('outputs'):
        os.mkdir('outputs')

def create_aggregate_file():
    """Create a new .txt file in 'outputs' with a timestamp."""
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'outputs/gpt-prompt-code-{timestamp}.txt'
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
                # Construct the path relative to the TOP_LEVEL_PATH
                full_path = os.path.join(root, file)
                yield os.path.relpath(full_path, TOP_LEVEL_PATH)

def aggregate_contents(paths, output_file):
    """Aggregate the contents of given files into the output file, only if they have valid extensions."""
    with open(output_file, 'w') as outfile:
        for relative_path in paths:
            if not is_valid_file_extension(relative_path):
                print(f"Skipping non-code file: {relative_path}")
                continue
            
            absolute_path = os.path.join(TOP_LEVEL_PATH, relative_path)
            try:
                with open(absolute_path, 'r') as infile:
                    outfile.write(f'~/{relative_path}:\n```\n{infile.read()}\n```\n\n')
            except UnicodeDecodeError:
                print(f"Error reading file (possible binary): {relative_path}")
            except Exception as e:
                print(f"Error processing file {relative_path}: {e}")

def print_usage():
    """Prints usage instructions."""
    usage_text = """
    This script aggregates the contents of code files into a single .txt file for use during LLM prompts.

    Usage:
      python script.py -d <relative_path_to_directory> : Aggregate all files in the given directory, relative to ~/GitLab/nexgen/.
      python script.py -f <relative_file1> <relative_file2> ... : Aggregate a list of specified files, relative to ~/GitLab/nexgen/.

    Options:
      -d --directory : Specify a directory to aggregate all its files, providing a relative path.
      -f --files     : Specify individual file paths to aggregate, providing relative paths.
      
    Note: This script assumes all paths are relative to the ~/GitLab/nexgen/ directory, 
    so that you can use VS Code's "Copy Relative Path" command. Files not matching the code-related extensions (.py, .js, .jsx, .html, .css, .go, .yaml, .yml, .sh) will be skipped.
    """
    print(usage_text)

def main():
    if len(sys.argv) == 1:
        print_usage()
        sys.exit(1)

    parser = argparse.ArgumentParser(description='Aggregate code files into a single .txt file.', usage=argparse.SUPPRESS)
    parser.add_argument('-d', '--directory', type=str, help='Directory containing the files to aggregate')
    parser.add_argument('-f', '--files', nargs='+', help='A list of file paths to aggregate')
    
    args = parser.parse_args()
    
    file_paths = []
    if args.directory:
        directory_path = os.path.join(TOP_LEVEL_PATH, args.directory)
        file_paths.extend(get_files_from_directory(directory_path))
    elif args.files:
        file_paths.extend(args.files)
    else:
        print_usage()
        sys.exit(1)
    
    ensure_outputs_dir()
    output_file = create_aggregate_file()
    aggregate_contents(file_paths, output_file)

    print(f'Aggregated content written to {output_file}')

if __name__ == '__main__':
    main()
