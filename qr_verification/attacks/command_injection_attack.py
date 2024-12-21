import subprocess
import shlex

def execute_command(user_input):
    """
    Executes a command securely by validating and sanitizing the input.
    """
    try:
        # Whitelist of allowed commands
        allowed_commands = ["ls", "ping", "echo"]

        # Tokenize the input to prevent injection
        user_input = shlex.split(user_input)

        # Ensure the command is in the allowed list
        if user_input[0] not in allowed_commands:
            raise ValueError("Command not allowed.")

        # Use subprocess.run with a list of arguments
        result = subprocess.run(user_input, capture_output=True, text=True, check=True)

        return f"Command Output:\n{result.stdout}"

    except ValueError as ve:
        return f"Input Error: {ve}"
    except subprocess.CalledProcessError as e:
        return f"Command Execution Failed: {e}"
    except Exception as ex:
        return f"Unexpected Error: {ex}"

# Example usage
user_command = input("Enter a command: ")  # Example: 'ls -l'
print(execute_command(user_command))