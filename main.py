import os
import hashlib
# folder path
dir_paths = [r'/Volumes/Public/Shared Pictures/',
             r'/Volumes/Public/dante.casanova/',
             r'/Volumes/Public/dantecasanova/',
             r'/Volumes/Public/LCA-3B/']
media_files = {}
flipped = {}
duplicated_media_files = {}
duplicated_checksum_files = {}

def listfiles(dir_path):
    with os.scandir(dir_path) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file() and not (entry.name.endswith('.db') or entry.name == 'Folder.jpg') and (entry.name.endswith('.JPG') or entry.name.endswith('.JPEG') or entry.name.endswith('jpg') or entry.name.endswith('jpeg')):
                full_path = dir_path+entry.name
                media_files[full_path] = entry.name
            if not entry.name.startswith('.') and entry.is_dir():
                new_path = dir_path+entry.name+'/'
                listfiles(new_path)

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def main():
    for dir_path in dir_paths:
        listfiles(dir_path)

    for key, value in media_files.items():
        if value not in flipped:
            flipped[value] = [key]
        else:
            flipped[value].append(key)

    for key, values in flipped.items():
        if len(values) > 1:
            duplicated_media_files[key] = values

    for key, values in duplicated_media_files.items():
        f = open("duplicated_media.txt", "a")
        line = key + ':' + ','.join(values)
        f.write(line+"\n")
        f.close()
        for value in values:
            checksum = md5(value)
            if checksum not in duplicated_checksum_files:
                duplicated_checksum_files[checksum] = [value]
            else:
                duplicated_checksum_files[checksum].append(value)

    for key, values in duplicated_checksum_files.items():
        if len(values) > 1:
            print('Removing file: ', values[-1])
            decision = input("Yes(y) or No(n)?")
            if decision == 'y':
                os.remove(values[-1])
            f = open("duplicated_checksums.txt", "a")
            line = key + ':' + ','.join(values)
            f.write(line+"\n")
            f.close()

#     print("duplicated checksum", str(duplicated_media_files))

if __name__ == "__main__":
    main()