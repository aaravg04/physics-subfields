import numpy as np
import pandas as pd

def partition_file(file_path):
    df = pd.DataFrame()

    with open(file_path, 'r') as file:
        current_institution = ""
        for line in file:
            line = line.strip()
            if line:
                if '(' not in line:
                    current_institution = line
                else:
                    name, ranges = line.split('(', 1)
                    name = name.strip()
                    ranges = ranges.strip()[:-1]  # Remove the trailing ')'
                    # print(ranges)
                    for range_str in ranges.split(','):
                        # print(range_str)
                        start, end = parse_range(range_str.strip())
                        df = pd.concat([df, pd.DataFrame({
                            'name': [name],
                            'start': [start],
                            'end': [end],
                            'institution': [current_institution]
                        })], ignore_index=True)

    return df

def parse_range(range_str):
    # print(range_str)
    start, end = range_str.split('-')
    start = int(start.strip())
    end = 2024 if end.strip() == 'present' else int(end.strip())
    return start, end
# Usage
file_path = 'biophys_in_dept.txt'
partitioned_blocks = partition_file(file_path)
# print(partitioned_blocks)
# Print the blocks (or do something else with them)
# for i, block in enumerate(partitioned_blocks, 1):
#     print(f"Block {i}:")
#     print(block)
#     print("\n" + "-"*50 + "\n")  # Separator between blocks

partitioned_blocks.to_csv("parsed_biophys_researchers.csv")