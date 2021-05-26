import os
import pandas as pd
import csv



for filename in os.listdir('/Users/muratbarlas/Desktop/test2'):
    if filename.endswith(".csv"):

             # making data frame from the csv file
             dataframe = pd.read_csv('/Users/muratbarlas/Desktop/test2/'+filename)

             # using the replace() method
             dataframe.replace(to_replace=200402,
                               value="4/2/2020",
                               inplace=True)
             dataframe.replace(to_replace=200415,
                               value="4/15/2020",
                               inplace=True)
             dataframe.replace(to_replace=200513,
                               value="5/13/2020",
                               inplace=True)
             dataframe.replace(to_replace=200527,
                               value="5/27/2020",
                               inplace=True)
             dataframe.replace(to_replace=200618,
                               value="6/18/2020",
                               inplace=True)
             dataframe.replace(to_replace=200624,
                               value="6/24/2020",
                               inplace=True)
             dataframe.replace(to_replace=200716,
                               value="7/16/2020",
                               inplace=True)

             dataframe.replace(to_replace=200730,
                               value="7/30/2020",
                               inplace=True)
             dataframe.replace(to_replace=200813,
                               value="8/13/2020",
                               inplace=True)
             dataframe.replace(to_replace=200827,
                               value= "8/27/2020",
                               inplace=True)
             dataframe.replace(to_replace=200910,
                               value="9/10/2020",
                               inplace=True)
             dataframe.replace(to_replace=200924,
                               value="9/24/2020",
                               inplace=True)
             dataframe.replace(to_replace=201008,
                               value="10/8/2020",
                               inplace=True)
             dataframe.replace(to_replace=201022,
                               value="10/22/2020",
                               inplace=True)
             dataframe.replace(to_replace=201105,
                               value="11/5/2020",
                               inplace=True)
             dataframe.replace(to_replace=201119,
                               value="11/19/2020",
                               inplace=True)
             dataframe.replace(to_replace=201203,
                               value="12/3/2020",
                               inplace=True)
             dataframe.replace(to_replace=210107,
                               value="1/7/2021",
                               inplace=True)
             dataframe.replace(to_replace=210121,
                               value="1/21/2021",
                               inplace=True)
             dataframe.replace(to_replace=210204,
                               value="2/4/2021",
                               inplace=True)
             dataframe.replace(to_replace=210218,
                               value="2/18/2021",
                               inplace=True)


             # writing  the dataframe to another csv file
             dataframe.to_csv('/Users/muratbarlas/Desktop/test2/corrected/' + 'CORRECTED' + filename,
                              index=False)


    else:
        continue




fout=open("out.csv","a")
writer = csv.writer(fout)
fout.write("Indx,Date,APD,25P,75P,MPD,Adherence12,Adherence6,Adherence3,Location")
fout.write("\n")

for filename in os.listdir('/Users/muratbarlas/Desktop/test2/corrected'):
        if filename.endswith(".csv"):
            f = open('/Users/muratbarlas/Desktop/test2/corrected/'+filename)
            f.__next__()  # skip the header

            for line in f:
                fout.write(line)
            f.close() # not really needed
fout.close()

with open("out.csv", "r") as source:
    reader = csv.reader(source)
    with open("output2.csv", "w") as result:
        writer = csv.writer(result)
        for r in reader:
            writer.writerow((r[1], r[2], r[3], r[4], r[5],r[6],r[7],r[8], r[9]))

os.remove("out.csv")