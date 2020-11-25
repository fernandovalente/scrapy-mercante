import requests as req
from bs4 import BeautifulSoup


class VesselScraper:
    def __init__(self):
        print("hi")

    def get_vessel_data(self):
        json_practical = {}
        ports = {}
        port_guanabara = []
        port_sepetiba = []
        link = "https://www.vesseltracker.com/en/vessels.html?page=1&search=A"
        response = req.get(link)
        soup = BeautifulSoup(response.text, features="lxml")
        odds = soup.find_all(class_="row odd")
        evens = soup.find_all(class_="row even")
        json = []
        json_row = {}

        for odd in odds:
            divs = odd.find_all("div")
            col_date = odd.find_all("col-sm-1")

            json_row = {
                "name": divs[3].text,
                "imo": divs[4].text,
                "callsign": divs[5].text,
                "mmsi": divs[6].text,
                "len_x_wid_meters": divs[7].text,
                "area": divs[8].text,
                "last_seen": col_date[0].text,
            }
            json.append(json_row)

        for even in evens:
            divs = even.find_all("div")
            col_date = even.find_all("col-sm-1")
            json_row = {
                "name": divs[3].text,
                "imo": divs[4].text,
                "callsign": divs[5].text,
                "mmsi": divs[6].text,
                "len_x_wid_meters": divs[7].text,
                "area": divs[8].text,
                "last_seen": col_date[0].text,
            }
            json.append(json_row)

        return json
