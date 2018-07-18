
import re
import pprint
import os
import nltk

from collections import defaultdict
from collections import Counter
from pprint      import pprint

list1=[]

for root, dirs, files in os.walk("/Users/rishi/Desktop/NLP_Data/Assignment_2/NSF_abstracts"):  
  for filename in files:
    #print(filename)
    list1.append(filename)
count=len(list1)
number_files=0
list_Filename=[]
list_Awards=[]
list_Organization=[]
list_DateYears=[]
dic1=defaultdict(list)
dic2=defaultdict(list)
dic3={}
text_file = open("Output_part1.txt", "w")
text2_file = open("Output_part2.txt", "w")
text2_file.write('Abstract_ID'+'|'+'Sentence_No'+'|'+'Sentence'+'\n\n')

while(count>0):
    f = open('/Users/rishi/Desktop/NLP_Data/Assignment_2/NSF_abstracts/'+list1[number_files], 'r',encoding = "ISO-8859-1")
    data=f.read()

    File=re.findall('File\s+: a[0-9]*', data)
    if len(File) > 0:
        File_name = re.findall('a[0-9]+', File[0])
        File_name=str(File_name[0])
        #File_name=File_name[2:10]

    NSF_Org=re.findall('NSF Org\s+: [A-Z]{3}',data)
    if len(NSF_Org) > 0:
        NSF_name = re.findall(' [A-Z]{3}', NSF_Org[0])
        NSF_name=str(NSF_name[0])
        #NSF_name=NSF_name[4:7]
    

    total_amt_line=re.findall('Total Amt\.\s+: \$[0-9]*', data)
    if len(total_amt_line) > 0:
        total_amt = re.findall("\$[0-9]+", total_amt_line[0])
        total_amt_int=re.findall("[0-9]+",total_amt_line[0])
        Amount=str(total_amt[0])
        Amount_int=int(total_amt_int[0])
        #Amount=Amount[2:8]

    #Date=re.findall('Date\s+: [A-Z]{1}[a-z]* [0-9]+,\s+[0-9]{4}$', data)
    #if len(Date) > 0:
     #   Date_name = re.findall('[0-9]{4}', Date[0])
      #  Date_name=str(Date_name[0])

    pat_year=re.compile('Date.*File',re.M|re.DOTALL)
    Date_term=pat_year.findall(data)

    ### Converting list to string
    Date_term=''.join(Date_term)

    ### Finding the start year. The result of the findall is a list
    year=re.findall('[1-2][0-9][0-9][0-9]',Date_term)
    if(len(year)>0):
        year_int=int(year[0])
    else:
        year_int=123



    pat_abstract=re.compile('Abstract.*',re.M|re.DOTALL)
    abstract=pat_abstract.findall(data)
    abstract=''.join(abstract)
    abstract=" ".join(abstract.split())
    abstract_content=abstract[11:]

    #print(File_name)
    #print(Date_name)
    list_Filename.append(File_name)
    list_Organization.append(NSF_name)
    list_Awards.append(Amount)
    list_DateYears.append(year_int)

    if dic1.get(NSF_name):
        dic1[NSF_name].append(Amount_int)
    else:
        #dic1[NSF_name]=(Amount)
        dic1.setdefault(NSF_name, []).append(Amount_int) 

    dic2[year_int].append(NSF_name)
    #print(NSF_name)
    #print(Amount)
    #print(abstract_content)





    
    text_file.write(File_name+' '+NSF_name+' '+Amount+' '+abstract_content+'\n\n')
    

    sent_text = nltk.sent_tokenize(abstract_content)
    cnt=len(sent_text)
    num=0
    

    while(cnt>0):

    
        num_str=str(num+1)
        text2_file.write(File_name+'|'+num_str+'|'+sent_text[num]+'\n')
    
        num += 1
        cnt -= 1

    text2_file.write("Number of Lines in file "+File_name+"    is :- "+num_str+'\n')
    text2_file.write("-------------------------------------------------------"+'\n')
    number_files += 1
    count -= 1
    f.close()

print("Dictionary of Organization and its awards")
print(dic1)
print("Frequenct Distribution of Organizations")
print(Counter(list_Organization))
list_k=[]
list_maxv=[]
print("Max value from each key")
for k , v in dic1.items():
    #dic4=dict(k,max(v))
    print (k,max(v))
    list_k.append(k)
    list_maxv.append(max(v))

dic4=dict(zip(list_k,list_maxv))

max_value = max(dic4.values()) 
max_keys = [k for k, v in dic4.items() if v == max_value] # getting all keys containing the `maximum`
print("The maximum amount award got by the organization:- ")
print(max_keys, max_value)
#print(len(list_Filename))
#print("Date Years")
#print(list_DateYears)
print("Year:- NSF_Org ")
for k , v in dic2.items():
    print (k,Counter(v))
#dic3=(zip(dic1,dic2))
#print("Filename: Year :- NSF_ORG :- Amount")
#print(dic3)
#print(len(list_DateYears))
#print("Frequenct Distribution of Awards amount")
#print(Counter(list_Awards))
text_file.close()
text2_file.close()
