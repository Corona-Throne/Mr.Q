
def load_json(filepath: str):
    import json
    try:
        with open(filepath, 'r', encoding="utf-8") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"File not found: {filepath}")
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return {}

def load_txt(filepath: str):
    try:
        with open(filepath, 'r') as file:
            # Read all lines from the file
            lines = file.read()
            return lines
    except FileNotFoundError:
        print(f"File not found: {filepath}")
    except PermissionError:
        print("Permission denied to open the file.")
    except Exception as e:
        print("An error occurred:", e)
