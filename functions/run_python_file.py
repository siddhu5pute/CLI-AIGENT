import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes the specified Python file with optional arguments, relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of arguments to pass to the Python file.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=None):
    if args is None:
        args = []
    try:
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        abs_working_dir = os.path.abspath(working_directory)
    
        if not full_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
        if not os.path.isfile(full_path):
            return f'Error: File "{file_path}" not found.'
    
        if not full_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'

        # Use unittest runner for test files
        if os.path.basename(file_path).startswith('test') or file_path == 'tests.py':
            cmd = ['python3', '-m', 'unittest', file_path] + args
        else:
            cmd = ['python3', full_path] + args
    
        completed_process = subprocess.run(
            cmd,
            timeout=30,
            capture_output=True,
            text=True,
            cwd=abs_working_dir
        )
    
        stdout_output = completed_process.stdout.strip()
        stderr_output = completed_process.stderr.strip()

        output_str = "" 
        
        if stdout_output:
            output_str += f"STDOUT:\n{stdout_output}\n"
        if stderr_output:
            output_str += f"STDERR:\n{stderr_output}\n"
        if completed_process.returncode != 0:
            output_str += f"Process exited with code {completed_process.returncode}\n"
        if not output_str:
            output_str = "No output produced."

        return output_str.strip()

    except Exception as e:
        return f"Error: executing Python file: {e}"
