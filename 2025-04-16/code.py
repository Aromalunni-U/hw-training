import json
import csv


csv_file = "2025-04-16/Iris.csv"
json_file = "2025-04-16/first.json"
csv_file2 = "2025-04-16/restored_Iris.csv"


with open(csv_file,"r") as file:
    data = csv.DictReader(file)
    data = list(data)

    with open(json_file,"w") as f:
        data = json.dump(data,f,indent=4)

print("CSV to JSON completed")
   
with open(json_file, "r") as f:
    data = json.load(f)

with open(csv_file2, "w", newline='') as f:
    writer = csv.DictWriter(f, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)

print("JSON to CSV completed")