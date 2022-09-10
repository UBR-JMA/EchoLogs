import json

# https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/
# save a provided dictionary as a JSON file with the provided filename.
# filename must include '.json' extension
def DictionaryToFile(dictionary, filename):
    # Serializing json
    json_object = json.dumps(dictionary, indent=4)
    # Writing to sample.json
    with open(filename, "w") as outfile:
        outfile.write(json_object)


# https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/
def DictionaryFromFile(filename):
    # Opening JSON file
    with open(filename, 'r') as openfile:
        # Reading from json file
        return json.load(openfile)