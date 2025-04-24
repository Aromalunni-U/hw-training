

def yield_lines_from_file(file_path):

    try:
        with open(file_path,"r") as file:
            for line in file:
                yield line
    except FileNotFoundError:
        print("File not found")



path = "2025-04-23/cleaned_data.tx"
    
for line in yield_lines_from_file(path):
    print(line)

