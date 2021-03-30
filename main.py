import os
import io
import datetime
from ftplib import FTP
import pandas as pd
ftp = FTP("FTP_IP_ADRESS")
ftp.login(user='USERNAME', passwd='PASSWORD')


def get_all_folder_contents(path):
    
    lines = []
    ftp.dir(path, lines.append)
    folders=[]
    files=[]
    modification_times=[]
    for line in lines:
        line_ = line.split(maxsplit = 3)
        modification_time = datetime.datetime.strptime(line_[0]+" "+line_[1], '%m-%d-%y %H:%M%p')
        if line_[2]=='<DIR>':
            folders.append(line_[3])
        else:
            files.append(line_[3])
            modification_times.append(modification_time)
    return folders,files,modification_times    
  
  
  
  
folder_path_tree=["/"]
for n in get_all_folder_contents("/")[0]:
    #print(n)
    folder_path_tree.append(n)
    if n != []:
        subfolders_1 = get_all_folder_contents(n)[0]
        for m in subfolders_1:
            if m != []:
                #print(n+"/"+m)
                path2=n+"/"+m
                folder_path_tree.append(path2)
                subfolders_2 = get_all_folder_contents(path2)[0]
                for c in subfolders_2:
                    if c != []:
                        #print(n+"/"+m+"/"+c)
                        path3=n+"/"+m+"/"+c
                        folder_path_tree.append(path3)
                        subfolders_3 = get_all_folder_contents(path3)[0]
                        for b in subfolders_3:
                            if b != []:
                                #print(n+"/"+m+"/"+c+"/"+b)
                                path4=n+"/"+m+"/"+c+"/"+b
                                folder_path_tree.append(path4)
                                
                                
list_of_df=[]
for x in folder_path_tree:
    df=pd.merge(pd.DataFrame(get_all_folder_contents(x)[1],columns=["NAME"]),pd.DataFrame(get_all_folder_contents(x)[2],columns=["TIME"]),left_index=True,right_index=True)
    df["PATH"]=x
    list_of_df.append(df)
df_ftp = pd.concat(list_of_df).reset_index().drop(columns=["index"])

#df_ftp is return object for ftp filename, path and modification time. It only reaches up to 3 sub-layers of folders
