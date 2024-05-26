import os
import sys
import argparse
from datetime import datetime

def is_valid_file_extension(filename):
    """Check if the file has a valid text-based extension."""
    valid_extensions = ['.py', '.js', '.jsx', '.html', '.css', '.go', '.yaml', '.yml', '.sh', '.tf', '.tfvars', '.tpl']
    return any(filename.endswith(ext) for ext in valid_extensions)

def is_hidden(filepath):
    """Check if the file or directory is hidden."""
    return any(part.startswith('.') for part in filepath.split(os.sep))

def get_files_from_directory(directory_path, include_hidden):
    """Recursively collect all valid files from the given directory, excluding hidden files unless specified."""
    for root, dirs, files in os.walk(directory_path):
        if not include_hidden:
            files = [f for f in files if not f.startswith('.')]
            dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if is_valid_file_extension(file):
                yield os.path.join(root, file)

def aggregate_contents(paths, outfile, is_output_file):
    """Aggregate the contents of given files and output to a file or print to console."""
    out = open(outfile, 'w') if is_output_file else sys.stdout
    try:
        for path in paths:
            if not is_valid_file_extension(path):
                continue
            try:
                with open(path, 'r') as infile:
                    content = infile.read()
                    out.write(f'{path}:\n```\n{content}\n```\n\n')
            except Exception as e:
                print(f"Error processing file {path}: {e}", file=sys.stderr)
    finally:
        if is_output_file:
            out.close()

def main():
    parser = argparse.ArgumentParser(description='Aggregate code files into a single output. Outputs to console by default, or to a file if specified.')
    parser.add_argument('-o', '--output', action='store_true', help='Write output to a file in the outputs directory instead of the console.')
    parser.add_argument('-d', '--directory', action='append', type=str, help='Directory paths to aggregate files from. Handles both absolute and relative paths.')
    parser.add_argument('-f', '--files', nargs='+', action='append', help='Individual file paths to aggregate. Handles both absolute and relative paths.')
    parser.add_argument('-s', '--show-hidden', action='store_true', help='Include hidden files and directories in the aggregation.')

    args = parser.parse_args()

    # Outputs directory setup
    if args.output:
        outputs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'outputs')
        if not os.path.exists(outputs_dir):
            os.makedirs(outputs_dir)
        timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        output_file = os.path.join(outputs_dir, f'gpt-prompt-code-{timestamp}.txt')
    else:
        output_file = None

    file_paths = []
    if args.directory:
        for directory in args.directory:
            directory = os.path.abspath(directory)  # Convert to absolute if not already
            file_paths.extend(get_files_from_directory(directory, args.show_hidden))
    if args.files:
        for files_list in args.files:
            for file in files_list:
                file = os.path.abspath(file)  # Convert to absolute if not already
                if os.path.exists(file) and is_valid_file_extension(file):
                    file_paths.append(file)
                else:
                    print(f"Error: File does not exist or is not a valid code file: {file}", file=sys.stderr)

    aggregate_contents(file_paths, output_file, args.output)

if __name__ == '__main__':
    main()
