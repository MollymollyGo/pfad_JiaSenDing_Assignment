from http.client import responses

from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import xlabel

#Create list
BookList=[]
RatingList=[]

#Get information by be identified as users.
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}
#Get URL
contents=requests.get('https://book.douban.com/top250?start=25',headers=headers)
#Get data
html=contents.text

#Analyze data by Beautiful Soup
soup = BeautifulSoup(html, "html.parser")
#Find book titles by same function name
BookTitles1=soup.findAll("div",attrs={"class":"pl2"})
for title1 in BookTitles1:
    title1_string = title1.text
    if title1_string:
        #Store data into the BookList list
        title1_string=title1_string.replace("\n","") #Delete Enter in data
        title1_string = title1_string.replace(" ", "") #Delete Space in data
        print(title1_string)
        BookList.append(title1_string)
print(BookList)
#Find Rating data
RatingNum=soup.findAll("span",attrs={"class":"rating_nums"})
for Rating in RatingNum:
    RatingList.append(Rating.string)

#Using library to store 2 lists
data = {
    'Book Name': BookList,
    'Rating': RatingList,
}
df = pd.DataFrame(data) #Transfer 2 lists into pandas DataFrame
df.to_excel('Book Rating.xlsx') #Save to excel

#Draw Picture
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']#Set fonts

fig = plt.figure()#Drawing
plt.figure(figsize=(25,15))#figsize
plt.title(u'DouBan Books Rating')#Chart Title
plt.xlabel('Rating', size=20)#Name of X
plt.ylabel(u'Book Name')#Name of Y
plt.barh(BookList, width=RatingList)#Drawing bar chart based on the data
plt.show()