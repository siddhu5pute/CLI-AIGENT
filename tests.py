from functions.run_python_file import run_python_file


def run_tests():
    print(run_python_file("calculator", "main.py"))           # Should print usage instructions or error if file missing
    print(run_python_file("calculator", "main.py", ["3 + 5"])) # Should run calculator script with argument
    print(run_python_file("calculator", "tests.py"))          # Should print error since tests.py may not be .py file or might not exist
    print(run_python_file("calculator", "../main.py"))        # Should return error for outside permitted directory
    print(run_python_file("calculator", "nonexistent.py"))    # Should return file not found error
    
if __name__ == "__main__":
    run_tests()
