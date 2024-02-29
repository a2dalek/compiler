import re

def categorize_word(word, previous_word=None):
    # Check if the word is an individual keyword
    individual_keywords = ["if", "then", "else"]
    if word in individual_keywords:
        return word.upper()  # Uppercase the word itself as the token

    # Check if the word is a number
    if re.match(r'^[0-9]+$', word):
        return "UNKNOWN" if word.startswith('-') else "NUMBER"

    # Check if the word is a variable
    if re.match(r'^[a-zA-Z][0-9][a-zA-Z0-9]*$', word):
        return "VARIABLE"

    # Check if the word is an operator
    operators = ["=", ">"]
    if (word.count("=") + word.count(">")) > 1:
        # If the condition is true, return 'UNKNOWN'
        return "UNKNOWN"
    
    if (word in operators):
        return "OPERATOR"

    # If the condition is false, divide the word based on '=' or '>'
    if ('=' in word):
        divided_elements = re.split(r'([=])', word)
        # Find the type of each element in the divided word
        types = [(element, categorize_word(element)) for element in divided_elements if element]

        # Check if all elements are not 'UNKNOWN'
        if all(element[1] != "UNKNOWN" for element in types):
            return "STMT", word, types

        # Return the types of each element
        return "UNKNOWN", word, types
    
    if ('>' in word):
        divided_elements = re.split(r'([>])', word)
        # Find the type of each element in the divided word
        types = [(element, categorize_word(element)) for element in divided_elements if element]

        # Check if all elements are not 'UNKNOWN'
        if all(element[1] != "UNKNOWN" for element in types):
            return "COND", word, types

        # Return the types of each element
        return "UNKNOWN", word, types

    return "UNKNOWN"

    

# Open the file in read mode
with open("input", "r") as file:
    # Read the entire contents of the file
    file_content = file.read()

# Split the content into words
words = file_content.split()

# Initialize an empty list to store tokens
tokens = []

# Categorize each word and store the result in the tokens list
for word in words:
    category = categorize_word(word)
    tokens.append((word, category))

# Display the categorized types for each word
print("Tokens:\n")
for token, category in tokens:
    if isinstance(category, tuple):
        types, word, elements = category
        print(f"{word}: {types}")
        for element, element_type in elements:
            print(f"  * {element}: {element_type}")
    else:
        print(f"{token}: {category}")
    print("")
