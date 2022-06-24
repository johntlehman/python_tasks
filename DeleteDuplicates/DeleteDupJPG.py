# delete a file - os.remove


import os

os.chdir('/Volumes/Extreme SSD/photos/PHOTOS GO HERE/2021')

c = 0
TotalFileSize = 0

# Walks the selected folder returning subfolders (dnames) and filenames (fnames)
for dirpath, dnames, fnames in os.walk("./"):

    print("Now scanning " + dirpath)

    for f in fnames:
        if f.endswith(".RAF"):
            SearchFile = f
            SearchJPG = SearchFile.replace("RAF", "JPG")
            print(SearchFile)

            # Search active directory to see if a JPG exists to match the RAF file
            for f2 in fnames:
                if f2 == SearchJPG:
                    FileSize = os.path.getsize(dirpath + "/" + SearchJPG)
                    TotalFileSize = TotalFileSize + FileSize
                    os.remove(dirpath + "/" + SearchJPG)
                    print(SearchJPG + " deleted")

print(str(TotalFileSize/1000000) + " MB of JPGs deleted")

#                try:
#                    found = fnames.find(SearchJPG)
#                    print(found)
#                    if found != -1:
#                        print()
#                        print(fileName, 'Found\n')
#                        print("i found" + SearchJPG + "!!!")

#                except:
#                    print("couldn't find" + SearchJPG)


#                found = Files.find(SearchJPG)
#                print(found)
#                if found != -1:
#                    print(SearchJPG, 'Found')
#                    break
#            except:
#                next()

#            for dirpath, dnames, fnames in os.walk("./"):
#                for j in fnames:
#                    if j == SearchJPG:
#                        #                        os.remove(j)
#                        c = c + 1
#                       print(j, SearchFile)

#    print(str(c) + " Files Deleted")

#
#            print(i)
#            if Files.find(i.JPG)
#                print(i.JPG)
#                print(os.path.join(dirpath,i))
#               os.remove(i.jpg)
#               os.remove(os.path.join(dirpath,f))
#           elif


#            for j in fnames:
#                if j.endswith("")
#            x(os.path.join(dirpath, f))
#        elif j.endswith(".RAF"):
#            print(j+"Raffle!")
#            xc(os.path.join(dirpath,f))