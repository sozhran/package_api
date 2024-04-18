import json
import re

# Dependencies format is quite mess. One package lists 3 python dependencies as
# "python2.7, python (>= 2.7.1-0ubuntu2), python (<< 2.8)"
# Another example: libstdc++6-4.6-dbg as dependency, while libstdc++6-4.6-dev, libstdc++6 are installed.
# Making a precise parser for these discrepancies is beyond this assessment's scope, so I only did simple literal matches.

def parser():
    ## Data preparation
    content = open('./status', 'r').read().split('\n\n')

    list_of_packages = []

    for record in content:
        parsed_record = {}
        split_record = record.split('\n')

        for line in split_record:
            # Checking if the line begins with the "TITLE: " pattern.
            if re.match(r'(^[\w]+[-]?[\w]+?):(\s)', line):
                key, value = line.split(": ", 1)
                key = key.strip() # unnecessary, but just in case
                value = value.strip()
                parsed_record.update({key: value})

            # Skipping empty lines with dots in 'Descriptions'.
            elif re.match(r'(^[ ]+[.])', line):
                continue
        
            # Joining 'Descriptions' together. Lines that don't begin with the pattern above are a continuation of a previous line
            # and are added to the last key's value in the dict. I'm using Python 3.10 where dicts are ordered.
            else:
                first, *_, last = parsed_record.items()
                parsed_record[last[0]] += line

            # Select only the keys required for FE
            filtered_record = {}
            for key in parsed_record.keys() & ['Package', 'Depends', 'Description']:
                filtered_record.update({key: parsed_record[key]})

            unparsed_deps = filtered_record.get('Depends')
            
            # Split dependencies into lists, then further split names and versions.
            # A lot can go wrong here considering how inconsistent dependency naming is.
            parsed_deps = []
            if unparsed_deps:
                split_deps = unparsed_deps.split(", ")
                for dep in split_deps:
                    split_name_version = dep.split(" ", 1)
                    parsed_deps.append({ "Name": split_name_version[0], "Version": split_name_version[1]})
                filtered_record['Depends'] = parsed_deps
            else:
                filtered_record['Depends'] = []

        list_of_packages.append(filtered_record)
    
    # Check if dependency needs a link on FE
    for record in list_of_packages:
        for package in list_of_packages:
            for dependency in package['Depends']:
                if dependency['Name'] in list_of_packages.keys():
                    dependency['Needs_Link'] = True
                else: dependency['Needs_Link'] = False

    # Calculate reverse dependencies
    for record in list_of_packages:
        reverseDepsList = []
        
        for package in list_of_packages:
            for dependency in package['Depends']:
                if dependency and dependency[0] == record['Package']:
                    reverseDepsList.append(package['Package'])
                else:
                    continue

        record['Reverse'] = reverseDepsList

    # Sort package list for FE
    sorted_list = sorted(list_of_packages, key=lambda x: x['Package'])
    
    return sorted_list
    # print(sorted_list)

# parser()


# BATTLEPLAN
# YES    For every Record - Reformat dependencies into list
# YES    For every Record - get a list of reverse Dependencies
# YES    Get Reverse dependencies to FE
# Alternates? No time, explain in a comment
# Comment on my solutions
# Ship it