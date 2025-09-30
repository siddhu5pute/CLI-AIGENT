import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = function_call_part.args  # dictionary
    
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")
        
    kwargs = dict(function_args)
    kwargs["working_directory"] = os.path.abspath("./calculator")
    
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    try:
        result = function_map[function_name](**kwargs)
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Exception: {str(e)}"},
                )
            ],
        )
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )


def main():
    print("Hello from sidisai!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    if len(sys.argv) < 2:
        print("Error: Please provide a prompt as a command line argument.")
        sys.exit(1)

    verbose = len(sys.argv) > 2 and sys.argv[2] == "--verbose"
    user_prompt = sys.argv[1]

    # Initial message list: start with user input
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    max_iterations = 20

    try:
        for iteration in range(max_iterations):
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt,
                ),
            )
            
            # Add each candidate's content to the message list as 'model' role
            for candidate in response.candidates:
                messages.append(types.Content(role="model", parts=[types.Part(text=str(candidate.content))]))

            
            # Check if a function call is requested
            if response.function_calls:
                function_call_part = response.function_calls[0]
                if verbose:
                    print(f"Iteration {iteration+1}:")
                function_call_result = call_function(function_call_part, verbose)
                
                # Validate function call returned content
                if not hasattr(function_call_result.parts[0], "function_response"):
                    raise RuntimeError("Fatal error: function call result missing function_response")
                
                # Append function response content as a 'user' message, so LLM can see the function result
                messages.append(function_call_result)
                
                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            else:
                # No function calls, final text response received -- print and exit loop
                final_response = response.text
                print("Final response:")
                print(final_response)
                break
        else:
            print("Reached maximum iteration limit without a final response.")
    except Exception as e:
        print(f"Error during agent execution: {e}")


if __name__ == "__main__":
    main()
