import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time

url = "https://www.ptt.cc/bbs/NBA/index.html"  


def fetch_data(url):
    global data_list, num_page, max_page
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    # 檢查 HTTP 請求是否成功
    if response.status_code == 200:
        print("Page fetched successfully!")
    else:
        print(f"Failed to fetch page. Status code: {response.status_code}")
        
    # 檢查網頁內容是否存在
    if response.content:
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all("div",class_="r-ent")
        

        for a in articles:
            data = {}
            title = a.find("div", class_="title")
            if title and title.a:
                link = title.find('a', href=True)
                href = link['href']
                title = link.get_text().strip()
                
            else:
                title= "No title found."
                href= "No url"
            data["title"] = title
            data["url"] = href
            

            popular = a.find("div", class_="nrec")
            if popular and popular.span:
                popular = popular.span.text
            else:
                popular = "N/A"
            data["popular"] = popular
            

            date = a.find("div", class_="date")
            if date:
                date = date.text
            else:
                date = "N/A"
            data["date"] = date

            data_list.append(data)

            print(f"{title}, Popular={popular}, ,Date={date} URL: {href}")


        #自動換頁
        page = soup.find("div", class_ = "btn-group btn-group-paging")
        next_page = page.find_all("a")[1] #上一頁
        print(next_page)
        if next_page:
            next_url = "https://www.ptt.cc" + next_page.get("href")
            num_page+=1
            if num_page < max_page: #爬取頁數
                time.sleep(1)  
                fetch_data(next_url)
            else:
                print("Reached maximum page limit.")
                return
            
def save_data():
    with open("ptt_nba_data.json", "w", encoding="utf-8") as jsonfile:
        json.dump(data_list, jsonfile, ensure_ascii= False, indent=4)
    print("data save to json")

    df = pd.DataFrame(data_list)
    df.to_excel("ptt_nba.xlsx", index= False, engine= "openpyxl")
    print("Data saved to Excel.")



data_list = []
num_page = 0
max_page = 5  #爬取頁數
fetch_data(url)
save_data()


"""
    with open('ptt_nba_data.csv', 'w', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Title', 'Popular', 'Date', 'URL'])  # 寫入表頭

        # 寫入每一個連結
        for data in data_list:
            title = data["title"]
            popular = data["popular"]
            date = data["date"]
            url = data['url']
            writer.writerow([title, popular, date , url])

    print("Data saved to data.csv")
"""
