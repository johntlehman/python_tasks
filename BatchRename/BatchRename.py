#os.chdir('/Users/johnlehman/Desktop/2019 Portland')

#for roots,dirs,files in os.walk('/Users/johnlehman/Desktop/2019 Portland'):
#                print(roots,len(dirs),len(files))

#delete a file - os.remove


import os

os.chdir('/Users/johnlehman/Desktop/2019 Portland')

c=0

for dirpath, dnames, fnames in os.walk("./"):

    for i in fnames:
        os.rename(r'file path\OLD file name.file type', r'file path\NEW file name.file type')
        if i.endswith(".RAF"):
            SearchFile = i
            SearchJPG = SearchFile.replace("RAF", "JPG")
#            print(SearchFile)

            for dirpath, dnames, fnames in os.walk("./"):
                for j in fnames:
                    if j == SearchJPG:
                        os.remove(j)
                        c = c+1
                        print(j,SearchFile)

    print(str(c)+"Files Deleted")

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