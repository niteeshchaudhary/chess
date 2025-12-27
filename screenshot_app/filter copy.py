import re

def reorganize_text(input_text):
    # Regex pattern: Name (optional) followed by Time
    pattern = r"(?:(?P<name>[A-Z][a-z]*)\s+)?(?P<time>(yesterday|now|monday|tuesday|wednesday|thursday|friday|saturday|sunday)(?:\s+\d{1,2}:\d{2})?)"
    
    result = {}
    current_key = "ME"
    last_position = 0

    # Iterate over matches in the input text
    for match in re.finditer(pattern, input_text):
        name = match.group("name")
        time = match.group("time")
        start, end = match.span()
        
        # Assign the text before this match to the current key
        if last_position != start:
            segment = input_text[last_position:start].strip()
            if segment:  # Avoid empty or whitespace-only segments
                result[current_key] = result.get(current_key, "") + " " + segment
        
        # Update the current key: Use the name if present, otherwise "ME"
        current_key = name if name else "ME"
        last_position = end
    
    # Add the remaining text after the last match
    if last_position < len(input_text):
        segment = input_text[last_position:].strip()
        if segment:
            result[current_key] = result.get(current_key, "") + " " + segment

    # Clean up whitespace around the values
    result = {key: value.strip() for key, value in result.items()}
    
    return result

# Example usage
input_text = """
09.Graphcude senvice @e Monday; Aug 26, 3.09PM @Puneet Bisht what is the full name of santosh Puneet Bisht  Aug 26, 3.14PM Bharthi On leave today Yesterday Puneet Bisht 
  Yesterday 4:16 PM 10078 ka cluster kyu stopped h?? Yesterday 7.33PM Puneet Bisht 10078 ka cluster kyu stopped h?? Qa h na weekends pr stop hi rehta h Aug
"""
print(reorganize_text(input_text))
