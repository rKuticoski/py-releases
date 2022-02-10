import json
import requests
from bs4 import BeautifulSoup


def scrapper_column(column):
    infos = {}
    for version in column.ul.li.next_siblings:
        if version.get_text() != "\n":
            downloads = []
            for link in version.ul.find_all("a"):
                downloads.append(link['href'])
            
            py_version, date_version = version.a.get_text().replace(" ", "").split("-")  
            infos.update({
                py_version: {
                    "Date": date_version, 
                    "Links": downloads
                }
            })
    
    return infos


def get_releases():
    page = requests.get("https://www.python.org/downloads/source/")
    soup = BeautifulSoup(page.text, 'html.parser')
    columns = soup.find_all("div", class_="column")
    

    with open("sample.json", "w") as outfile:
        output_dict = {
            "Stable Releases": scrapper_column(columns[0]),
            "Pre-releases": scrapper_column(columns[1])
        }
        
        json.dump(output_dict, outfile, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    get_releases()    
