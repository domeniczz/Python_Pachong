import json

with open("read_json.json", mode='r', encoding='utf-8') as f:
    json_data = json.load(f)

print(json_data["data"]["list"])

print(json_data["data"]["list"][0])

print(json_data["data"]["list"][int(input(": "))])

f.close()
