import json
import re

# Dependencies are formatted quite inconsistently. Most packages are listed in the 'NAME (> VERSION)' format,
# while some can be 'NAMEVERSION', 'NAME--VERSION-dev' etc.
# One package lists 3 python dependencies as "python2.7, python (>= 2.7.1-0ubuntu2), python (<< 2.8)".
# Making a precise parser for these inconsistencies would put this assessment in a scope bigger than what I can do in 8 hours.
# 
# I'm skipping parsing of alternates because I'm hitting the time limit, and I am aware that package Descriptions
# can look rough when concatenated into one string. One possible improvement would be to treat empty lines with dots ' .'
# as new lines.

def status_parser(filepath):
    ## Data preparation
    content = open(filepath, 'r').read().split('\n\n')

    list_of_packages = []

    for record in content:
        parsed_record = {}
        split_record = record.split('\n')
        # current_key is used to access the last key in dict
        current_key = None

        for line in split_record:
            
            # Checking if the line begins with the "TITLE: " pattern. Titles can have alphanumeric symbols and "-".
            if re.match(r'(^[\w]+([-]?[\w]+?)+?):', line):
                key, value = line.split(":", 1)
                key = key.lower().strip() # strip is unnecessary, but just in case
                value = value.strip()
                current_key = key
                parsed_record.update({key: value})

            # Skipping empty lines with dots in 'Descriptions'.
            elif re.match(r'(^[ ]+[.])', line):
                continue
        
            # Joining 'Descriptions' together. Lines that begin with a space without a dot are a continuation of the text above
            # and are added to the last key's value in the dict. I'm using Python 3.10 where dicts are ordered.
            elif re.match(r'(^[ ]+)', line) and current_key:
                parsed_record[current_key] += line

            # Select only the keys required for FE
            filtered_record = {}
            for key in parsed_record.keys() & ['package', 'depends', 'description']:
                filtered_record.update({key: parsed_record[key]})

            unparsed_deps = filtered_record.get('depends')
            
            # Split dependencies into lists, then further split names and versions.
            # A lot could potentially go wrong here considering the inconsistent dependency naming.
            parsed_deps = []
            if unparsed_deps:
                split_deps = unparsed_deps.split(", ")
                for dep in split_deps:
                    split_name_version = dep.split(" ", 1)
                    
                    if len(split_name_version) > 1:
                        parsed_deps.append({ "name": split_name_version[0], "version": split_name_version[1]})
                    else:
                        parsed_deps.append({ "name": split_name_version[0], "version": ""})

                filtered_record['depends'] = parsed_deps
            else:
                filtered_record['depends'] = []

        list_of_packages.append(filtered_record)
    
    # Check if dependency needs a link on FE and creating one if needed
    for record in list_of_packages:
        for dependency in record['depends']:
            dependency['link'] = None
            for package in list_of_packages:
                if dependency['name'] == package['package']:
                    dependency['link'] = "/package/" + package['package']
                else: continue

    # Calculate reverse dependencies
    for record in list_of_packages:
        reverseDepsList = []
        
        for package in list_of_packages:
            for dependency in package['depends']:
                if dependency and dependency['name'] == record['package']:
                    reverseDepsList.append(package['package'])
                else:
                    continue

        reverseDepsList = sorted(set(reverseDepsList))

        record['reverse'] = reverseDepsList

    # Sort package list for FE
    sorted_list = sorted(list_of_packages, key=lambda x: x['package'])
    
    return sorted_list