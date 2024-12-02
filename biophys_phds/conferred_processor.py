import pandas as pd
import re


def parse_phd_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = []
    current_year = None
    current_institution = None
    index = 0  # To track the current line index
    expecting_title = False  # Flag to indicate if we expect a dissertation title

    while index < len(lines):
        line = lines[index].strip()
        
        if not line:  # Skip empty lines
            index += 1
            continue
        
        if line.isdigit():  # Year line
            current_year = int(line)
            index += 1  # Move to the next line
            continue
        
        if current_institution is None:  # First non-empty line after year
            current_institution = line
            index += 1  # Move to the next line
            continue
        
        # Check if we are expecting a dissertation title
        if expecting_title:
            dissertation_title = line
            expecting_title = False  # Reset the flag
            # Append the data
            data.append({
                'student_name': student_name,
                'institution': current_institution,
                'year': current_year,
                'dissertation_title': dissertation_title,
                'advisors': advisors
            })
            # current_institution = None  # Reset institution for the next entry
            index += 1  # Move to the next line
            continue
        
        # Student entry
        if '(' in line:  # Line with student and advisor(s)
            student_info = line.split('(')
            student_name = student_info[0].strip()
            if len(student_info) > 1 and student_info[1].strip() == '':  # Check for empty parentheses
                advisors = 'unknown'
            elif student_info[1].strip() == ')':
                advisors = 'unknown'
            else:
                advisors = student_info[1].strip(') ').replace(',', ' | ') if len(student_info) > 1 else ''
                
            expecting_title = True  # Set the flag to expect a dissertation title
        else:  # Line without parentheses
            # If we are not expecting a title, treat it as an institution
            current_institution = line

        index += 1  # Move to the next line

    # Create DataFrame
    df = pd.DataFrame(data)
    return df

# Example usage
file_path = 'biophys_phds/conferred_phds.txt'  # Replace with your file path
df = parse_phd_data(file_path)
print(df)
df.to_csv('conferred-dat.csv')