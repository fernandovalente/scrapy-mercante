import requests as req
from bs4 import BeautifulSoup
import string
import json as j


class VesselScraper:
    def __init__(self):
        print("hi")

    def get_vessel_data(self):
        json = []
        for c in ["B"]:
            i = 1
            print(c)
            while i < 6:
                link = f"https://www.vesseltracker.com/en/vessels.html?page={str(i)}&search={c}"  # Gets summarized data from the pagination
                response = req.get(link)
                soup = BeautifulSoup(response.text, features="lxml")
                odds = soup.find_all(class_="row odd")  # Type of line in table
                evens = soup.find_all(class_="row even")  # Type of line in table
                json_row = {}
                if len(odds) == 0 and len(evens) == 0:  # Next iteration if empty page
                    break
                print(str(i))

                for odd in odds:
                    divs = odd.find_all("div")
                    name = divs[3].find_all("a")[0].text
                    imo = divs[4].text
                    AIS_type = ""
                    flag = ""
                    link_inner_data = f"https://www.vesseltracker.com/en/Ships/{name}-{imo}.html"  # Gets a couple of data from inside each ship
                    try:

                        response_inner_data = req.get(link_inner_data)
                        soup_inner_data = BeautifulSoup(
                            response_inner_data.text, features="lxml"
                        )
                        AIS_table = soup_inner_data.find_all(class_="key-value-table")
                        AIS_type = (
                            AIS_table[1].find_all(class_="col-xs-7 value")[0].text
                        )
                        flag = AIS_table[1].find_all(class_="col-xs-7 value")[2].text
                    except:
                        pass
                    print(name)
                    json_row = {
                        "name": name,
                        "description": divs[3].find_all("span")[0].text,
                        "imo": imo,
                        "AIS_type": AIS_type,
                        "flag": flag,  # Possibly translated as nacionality
                        "callsign": divs[5].text,
                        "mmsi": divs[6].text,
                        "len_x_wid_meters": divs[7].text,
                    }
                    json.append(json_row)

                for even in evens:
                    divs = even.find_all("div")
                    name = divs[3].find_all("a")[0].text
                    imo = divs[4].text
                    AIS_type = ""
                    flag = ""
                    link_inner_data = f"https://www.vesseltracker.com/en/Ships/{name}-{imo}.html"  # Gets a couple of data from inside each ship
                    try:

                        response_inner_data = req.get(link_inner_data)
                        soup_inner_data = BeautifulSoup(
                            response_inner_data.text, features="lxml"
                        )
                        AIS_table = soup_inner_data.find_all(class_="key-value-table")
                        AIS_type = (
                            AIS_table[1].find_all(class_="col-xs-7 value")[0].text
                        )
                        flag = AIS_table[1].find_all(class_="col-xs-7 value")[2].text
                    except:
                        pass
                    print(name)
                    json_row = {
                        "name": name,
                        "description": divs[3].find_all("span")[0].text,
                        "imo": imo,
                        "AIS_type": AIS_type,
                        "flag": flag,  # Possibly translated as nacionality
                        "callsign": divs[5].text,
                        "mmsi": divs[6].text,
                        "len_x_wid_meters": divs[7].text,
                    }
                    json.append(json_row)
                i = i + 1

        with open("boats.json", "w") as outfile:
            j.dump(json, outfile)
        return json
