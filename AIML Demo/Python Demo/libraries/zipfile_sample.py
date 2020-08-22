import zipfile
z = zipfile.ZipFile("a.zip")
for name in z.namelist():
    print(name)