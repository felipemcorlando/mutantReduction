import filecmp
import difflib
from pathlib import Path
import os

def compare_files(file1_path: str, file2_path: str, show_differences: bool = True) -> bool:
    """
    Compare two files and optionally show their differences.
    
    Args:
        file1_path: Path to first file
        file2_path: Path to second file
        show_differences: If True, prints the differences between files
    
    Returns:
        bool: True if files are identical, False otherwise
    """
    # Convert to Path objects
    path1 = Path(file1_path)
    path2 = Path(file2_path)
    
    # Check if both files exist
    if not path1.exists():
        raise FileNotFoundError(f"First file not found: {file1_path}")
    if not path2.exists():
        raise FileNotFoundError(f"Second file not found: {file2_path}")
    
    # Quick comparison using filecmp
    are_identical = filecmp.cmp(file1_path, file2_path, shallow=False)
    
    # If files are different and differences should be shown
    if not are_identical and show_differences:
        # Read the files
        with open(file1_path, 'r') as f1, open(file2_path, 'r') as f2:
            file1_lines = f1.readlines()
            file2_lines = f2.readlines()
        
        # Generate differences
        differ = difflib.Differ()
        diff = list(differ.compare(file1_lines, file2_lines))
        
        # Print differences
        print("\nDifferences found:")
        print("Legend: '+' new line, '-' deleted line, '?' modified line\n")
        for line in diff:
            if line.startswith(('+ ', '- ', '? ')):
                print(line.rstrip())
    
    return are_identical

if __name__ == '__main__':
    

    directory = './data/output/' 


    for i in range(0, 30):
        file2 = os.path.join(directory, f"mutant_{i}.py")

        try:

            file1 = "./data/output/mutant_0.py"
            
            result = compare_files(file1, file2)
            if result:
                print("Files are identical")
            else:
                print("Files are different")
                
        except Exception as e:
            print(f"Error: {e}")