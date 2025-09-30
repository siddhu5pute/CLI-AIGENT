from google.genai import types
import os

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        # Create absolute path for the target directory based on working_directory and relative directory
        full_path = os.path.abspath(os.path.join(working_directory, directory))
        abs_working_dir = os.path.abspath(working_directory)

        # Check if full_path stays inside the working_directory boundaries
        if not full_path.startswith(abs_working_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check if the full_path is a directory
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'

        # List all entries inside the directory
        entries = os.listdir(full_path)
        result_lines = []
        
        for entry in entries:
            entry_path = os.path.join(full_path, entry)
            # Get file size in bytes
            file_size = os.path.getsize(entry_path) if os.path.isfile(entry_path) else 0
            # Check if it is a directory
            is_dir = os.path.isdir(entry_path)
            # Format line for this entry
            line = f'- {entry}: file_size={file_size} bytes, is_dir={is_dir}'
            result_lines.append(line)

        # Join all lines into a single string separated by newlines
        return "\n".join(result_lines)

    except Exception as e:
        # Catch any unexpected errors and return as string
        return f"Error: {str(e)}"
