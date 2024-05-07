import json

# Read the JSON file
with open('/home/guest/polaris-dev.Tenants.json') as file:
    data = json.load(file)

# Convert the JSON data to a string
data_str = json.dumps(data)

# Write the string back to the same file
with open('polaris-dev.Tenantsstring.json', 'w') as file:
    file.write(data_str)
