import re
import pandas as pd

#input: check if you want html to excel or viceversa
option = input("Do you want to read an excel or an html file?\n")
while "html" not in option and "excel" not in option:
    option = input("Invalid option. Do you want to read an excel or an html file?\n")
if "html" in option:
    option = "html"
else:
    option = "xlsx"

#input take file
file = input("Read a file\n")
while option not in file:
    file = input("Wrong file type! Read a file\n")

#get filename, useful for creating output file
filename=""
for character in file:
    if character == '.':
        break
    filename+=character

if option == "html":
    #get html code
    with open (file,'r') as data:
        htmlCode=data.read()

    #get html table if there exists
    htmlCode=re.search("<table>(.*\n?)*</table>",htmlCode)
    if (htmlCode == None):
        print("There is no table here")
    else:
        #get data about the html table
        htmlCode=htmlCode.group() #gets string of table
        norows=len(re.findall("<tr>",htmlCode)) 
        nocols=len(re.findall("<td>",htmlCode))//norows
        table=[] #Excel table
        cells=re.findall("<td>(.*)</td>",htmlCode)
        headers=[] #Excel headers

        #put data in table
        for c_id in range (0,nocols):
            headers.append(cells[c_id])
        for r_id in range(1,norows):
            row=[]
            for c_id in range(0,nocols):
                cell=cells[c_id+r_id*nocols]
                row.append(cell)
            table.append(row)

        #table to dataframe to excel table
        df = pd.DataFrame(data=table)
        df.columns=headers
        print(df)
        df.to_excel(filename+".xlsx",index=False)
        print("Done")

else:
    #extract data from excel
    df=pd.read_excel(file)
    table = df.values.tolist()
    norows = len(table)
    nocols = len(table[0])
    headers = df.columns.values.tolist()
    
    #html code to output
    htmlCode = ""
    htmlCode+="<table>\n"
    htmlCode+="\t<tr>\n"
    for i in range (0,nocols):
        htmlCode+="\t\t<td>"+headers[i]+"</td>\n"
    htmlCode+="\t</tr>\n"
    for i in range (0,norows):
        htmlCode+="\t<tr>\n"
        for j in range (0,nocols):
            htmlCode+="\t\t<td>"+str(table[i][j])+"</td>\n"
        htmlCode+="\t</tr>\n"
    htmlCode+="</table>"
    
    #output to file
    webfile=filename+".html"
    with open (webfile,'w') as web:
        web.write(htmlCode)
    print("Done")
