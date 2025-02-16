import shlex

def sanitize_input(input_data):
    # Reject input with suspicious characters
    if any(c in input_data for c in [";", "&", "|", "`", "$"]):
        return False, "Input contains unsafe characters."

    # Tokenize the input safely
    try:
        tokens = shlex.split(input_data)
        if len(tokens) > 10:  # Limit token length
            return False, "Input is too complex."
    except ValueError:
        return False, "Input parsing failed."

    return True, "Input is safe."

# Example potentially malicious QR content
malicious_input = "ls; rm -rf /"

# Sanitize the input
is_safe, message = sanitize_input(malicious_input)
print(message)