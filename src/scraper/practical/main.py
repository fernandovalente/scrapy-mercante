import requests as req
from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup

import re


class PracticalScraper:
    def __init__(self):
        print("hi")

    def get_data_from_pratical_rj_history(self, date):
        date = date.replace("-", "%2F")
        link = f"http://praticagem-rj.com.br/?act=MAN&cmd=&cpx=10&dti={date}&dtf={date}&btSel="
        response = req.get(link)

        soup = BeautifulSoup(response.text, features="lxml")

        table = soup.find_all("table")[0].find_all("table")[12].find_all("table")[5]

        json = []

        for tr in table.find_all("tr")[1:]:
            tds = tr.find_all("td")

            json.append(
                {
                    "vessel": tds[1].text,
                    "start": tds[2].text,
                    "end": tds[3].text,
                    "maneuver": tds[4].text,
                    "from": tds[5].text,
                    "to": tds[6].text,
                }
            )

        return json

    async def get_data_from_practical_rj(self):
        json_practical = {}
        ports = {}
        port_guanabara = []
        port_sepetiba = []
        link = "http://www.praticagem-rj.com.br/"
        response = req.get(link)

        session = AsyncHTMLSession()
        r = await session.get(link)
        await r.html.arender()
        js_soup = BeautifulSoup(r.html.html)

        soup = BeautifulSoup(response.text)

        def get_imo(a):
            text = a["onmouseover"]

            result = re.findall(r"myHint.show\((.*)\)", str(text))
            modal = js_soup.find("div", {"id": f"TTip{result[0]}"})

            print(modal.find_all("tr")[4].find_all("td")[0])

            return modal.find_all("tr")[4].find_all("td")[0].text

        def get_guanabara_port_data(soup):
            port = []
            table_0 = soup.find_all("table")[0]  # big block table
            table_1 = table_0.find_all("table")[3]  # table block without navbar
            table_2 = table_1.find_all("table")[8]  # list the guanabara port table
            table_3 = table_2.find_all("table")[2]  # table content

            for tr in table_3.find_all("tr")[1:]:
                tds = tr.find_all("td")
                json_practical = {
                    "POB": tds[0].text,
                    "vessel": tds[1].find_all("a")[0].text,
                    "draft": tds[2].text,
                    "LOA": tds[3].text,
                    "beam": tds[4].text,
                    "imo": get_imo(tds[1].find_all("a")[0]),
                    "GT": tds[5].text,
                    "DWT": tds[6].text,  # probably deadweight_tonnage
                    "maneuver": tds[7].text,  # probably deadweight_tonnage
                    "from": tds[8].text,
                    "to": tds[9].text,
                    "BRD": tds[10].text,
                }
                port.append(json_practical)
            return port

        def get_sepetiba_port_data(soup):
            port = []
            table_0 = soup.find_all("table")[0]  # big block table
            table_1 = table_0.find_all("table")[3]  # table block without navbar
            table_2 = table_1.find_all("table")[13]  # list the sepetiba port table
            table_3 = table_2.find_all("table")[2]  # table content

            for tr in table_3.find_all("tr")[1:]:
                tds = tr.find_all("td")
                json_practical = {
                    "POB": tds[0].text,
                    "vessel": tds[1].find_all("a")[0].text,
                    "draft": tds[2].text,
                    "LOA": tds[3].text,
                    "beam": tds[4].text,
                    "GT": tds[5].text,
                    "DWT": tds[6].text,  # probably deadweight_tonnage
                    "maneuver": tds[7].text,  # probably deadweight_tonnage
                    "from": tds[8].text,
                    "to": tds[8].text,
                    "BRD": tds[9].text,
                }
                port.append(json_practical)
            return port

        def get_acu_port_data(soup):
            port = []
            table_0 = soup.find_all("table")[0]  # big block table
            table_1 = table_0.find_all("table")[3]  # table block without navbar
            # tables delta = 5, (8, 13, 18)
            table_2 = table_1.find_all("table")[18]  # list the sepetiba port table
            table_3 = table_2.find_all("table")[2]  # table content

            for tr in table_3.find_all("tr")[1:]:
                tds = tr.find_all("td")
                json_practical = {
                    "POB": tds[0].text,
                    "vessel": tds[1].find_all("a")[0].text,
                    "draft": tds[2].text,
                    "LOA": tds[3].text,
                    "beam": tds[4].text,
                    "GT": tds[5].text,
                    "DWT": tds[6].text,  # probably deadweight_tonnage
                    "maneuver": tds[7].text,  # probably deadweight_tonnage
                    "from": tds[8].text,
                    "to": tds[9].text,
                    "BRD": tds[10].text,
                }
                port.append(json_practical)
            return port

        # table_port_sepetiba = table.find_all("table")[2]
        # table_port_acu = table.find_all("table")[4]

        port_guanabara = get_guanabara_port_data(soup)
        port_sepetiba = get_sepetiba_port_data(soup)
        port_acu = get_acu_port_data(soup)
        ports = {
            "guanabara": port_guanabara,
            "sepetiba": port_sepetiba,
            "acu": port_acu,
        }
        return ports
