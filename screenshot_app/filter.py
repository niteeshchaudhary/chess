import re

def split_text_day_followed_by_time(input_text):
    # Regex to match day or date followed by time patterns
    pattern = r"(?:yesterday|now|monday|tuesday|wednesday|thursday|friday|saturday|sunday|aug|sep|oct|nov|dec)(?:\s*[,;]?\s*\d{1,2}:\d{2}\s*[AM][PM])?"

    # Initialize variables
    result = []
    last_position = 0

    # Find all matches for day or date followed by time patterns
    for match in re.finditer(pattern, input_text, re.IGNORECASE):
        start = match.start()
        end = match.end()

        # Capture the text before the match
        if last_position != start:
            segment = input_text[last_position:start].strip()
            if segment:
                result.append(segment)

        # Update last position to exclude the matched pattern
        last_position = end

    # Capture any remaining text after the last match
    if last_position < len(input_text):
        segment = input_text[last_position:].strip()
        if segment:
            result.append(segment)

    return result


def split_text_on_time(input_text):
    # Regex to match time patterns
    pattern = r"(?:yesterday|now|monday|tuesday|wednesday|thursday|friday|saturday|sunday|aug|sep|oct|nov|dec)(?:\s+\d{1,2}:\d{2}(?:[APap][Mm])?)?"

    # Initialize variables
    result = []
    last_position = 0

    # Find all matches for time patterns
    for match in re.finditer(pattern, input_text, re.IGNORECASE):
        start = match.start()
        end = match.end()

        # Capture the text before the match
        if last_position != start:
            segment = input_text[last_position:start].strip()
            if segment:
                result.append(segment)

        # Update last position to exclude the time pattern
        last_position = end

    # Capture any remaining text after the last match
    if last_position < len(input_text):
        segment = input_text[last_position:].strip()
        if segment:
            result.append(segment)

    return result

# Example input
input_text = """
09.Graphcude senvice @e Monday; Aug 26, 3.09PM @Puneet Bisht what is the full name of santosh Puneet Bisht  Aug 26, 3.14PM Bharthi On leave today Yesterday Puneet Bisht  
  Yesterday 4:16 PM 10078 ka cluster kyu stopped h?? Yesterday 7.33PM Puneet Bisht 10078 ka cluster kyu stopped h?? Qa h na weekends pr stop hi rehta h Aug
"""

# Splitting the text
output = split_text_day_followed_by_time(input_text)
print(output)
