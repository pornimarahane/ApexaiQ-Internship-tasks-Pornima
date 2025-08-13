#This program demonstrates file handling.

filename = "Notes.txt"

try:
    with open(filename, "w") as f:
        f.write("First line of file/n")
        f.write("Second line of file/n")
except Exception as e:
    print("Error while writing:", e)
else:
    print("File written successfully.")
finally:
    print("Information written succesfully")


try:
    with open(filename, "a") as f:
        f.write("Third line of file/n")
except Exception as e:
    print("Error while appending:", e)
else:
    print("Data appended successfully")
finally:
    print("Finished append operation.\n")


try:
    with open(filename, "r") as f:
        content = f.read()
except FileNotFoundError as fe:
    print("FileNotFoundError:", fe)
except Exception as e:
    print("Some other error while reading:", e)
else:
    print("File content:\n", content)
finally:
    print("Finished read operation\n")
