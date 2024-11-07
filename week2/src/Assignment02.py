import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

url = 'https://www.hko.gov.hk/tide/eCCHtext2024.html'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find('table')

if table is None:
    print("No table found on the page.")
else:
    rows = table.find_all('tr')

    headers = ['Month', 'Day', 'Time1', 'Height1', 'Time2', 'Height2', 'Time3', 'Height3', 'Time4', 'Height4']

    data = []
    for row in rows[1:]:
        cells = row.find_all('td')
        data.append([cell.text.strip() for cell in cells])

    df = pd.DataFrame(data, columns=headers)

    print(df.head())

    for col in ['Height1', 'Height2', 'Height3', 'Height4']:
        df[col] = pd.to_numeric(df[col], errors='coerce')


    if not df.empty:
        plt.figure(figsize=(10, 5))
        plt.plot(df['Time1'], df['Height1'], marker='o')
        plt.title('Tide Heights on Different Days (Time1 vs Height1)')
        plt.xlabel('Time1')
        plt.ylabel('Height1 (m)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print("No data available for plotting.")
