import re

## Data preparation

content = open('./test.txt', 'r').read().split('\n\n')

list = []

for record in content:
    parsed_record = {}
    split_record = record.split('\n')

    for line in split_record:
        # Checking if the line begins with the "TITLE: " pattern.
        if re.match(r'(^[\w]+[-]?[\w]+?):(\s)', line):
            key, value = line.split(": ")
            key = key.strip() # unnecessary, but just in case
            value = value.strip()
            parsed_record.update({key: value})

        # Skipping empty lines with dots in 'Descriptions'.
        elif re.match(r'(^[ ]+[.])', line):
            continue
        
        # Joining 'Descriptions' together. Lines that don't begin with the pattern above are a continuation of a previous line
        # and are added to the last key's value in the dict. I'm using Python 3.12 where dicts are ordered.
        else:
            first, *_, last = parsed_record.items()
            parsed_record[last[0]] += line
    
    list.append(parsed_record)

for record in list:
    print("Package: ", record["Package"], "Version: ", record["Version"])
