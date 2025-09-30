import os
from google.genai import types
from config import MAX_FILE_READ_LENGTH # assuming config.py exists in your project root

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of the specified file relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)
def get_file_content(working_directory, file_path):
    try:
        # Construct absolute file path
        full_path = os.path.abspath(os.path.join(working_directory, file_path))
        abs_working_dir = os.path.abspath(working_directory)

        # Verify file is within working directory boundaries
        if not full_path.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Verify path is a regular file
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read file contents safely with truncation limit
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read(MAX_FILE_READ_LENGTH + 1)  # read one extra char to test length

        if len(content) > MAX_FILE_READ_LENGTH:
            truncated_content = content[:MAX_FILE_READ_LENGTH]
            truncated_content += f'\n[...File "{file_path}" truncated at {MAX_FILE_READ_LENGTH} characters]'
            return truncated_content
        else:
            return content

    except Exception as e:
        return f"Error: {str(e)}"
