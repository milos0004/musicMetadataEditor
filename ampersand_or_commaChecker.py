



excluded_artists = [

]

def filter_strings(string_list):
    filtered_list = []
    for s in string_list:
        if ',' in s or '&' in s:
            filtered_list.append(s)  # Keep the string if it contains ',' or '&'
        else:
            print(f"Removed: {s}")   # Print the removed string
    return filtered_list

# Use the imported list
result = filter_strings(excluded_artists)
print("Filtered list:", result)

