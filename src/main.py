# imports, like using or import
import shutil
from os import listdir
from os.path import isfile, join, exists
version = "v1.0.0"
print("btelnyy's mc player .dat offline to online converter " + version)
try:
    import requests
except ImportError:
    print("Please install requests to use this script! Command: pip3 install requests")

# get files in current dir
def getFiles() -> list[str]:
    mypath = "./"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles

# get the unformatted UUID, it has no dashes
def getUUID(name) -> str:
    print("Getting UUID. Name: " + name)
    data = requests.get("https://api.mojang.com/users/profiles/minecraft/<username>".replace("<username>", name))
    if(data.status_code != 200):
        print("Error: An error occured while contacting mojang servers: " + str(data.status_code))
        # cracked accounts cannot be converted, so they will stay cracked.
        return name
    data = data.json()
    print("ID: " + data["id"])
    print("UUID: " + getCorrectedUUID(data["id"]))
    return data["id"]

# get formatted UUID, now adds dashes
def getCorrectedUUID(id) -> str:
    chars = []
    for l in id:
        chars.append(l)
    # I have no better way to do this, I thought this was correct
    chars.insert(8, "-")
    chars.insert(13, "-")
    chars.insert(18, "-")
    chars.insert(23, "-")
    uuid = ""
    for c in chars:
        uuid += c
    return uuid

# main function, check files, split and copy
def main():
    # For every file in files
    for file in getFiles():
        # split name and extension
        parts = file.split(".")
        # if the extension is not .dat
        if(parts[1] != 'dat'):
            print(file + " is not a .dat file, ignoring.")
            continue
        # otherwise
        else:
            # get corrected filename
            filename = getCorrectedUUID(getUUID(parts[0]))
            # copy files
            if exists(filename + ".dat"):
                print("File " + filename + ".dat" + " already exists, keeping old version.")
                continue
            # debug logging
            print("Copying file: " + file + " -> " + filename + ".dat")
            shutil.copyfile(file, filename + ".dat")
            

        
# python trickery
if(__name__ == '__main__'):
    main()