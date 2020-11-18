import requests as req
from bs4 import BeautifulSoup


class PracticalScraper:
    def __init__(self):
        print("hi")

    def get_data_from_practical_rj(self):
        json_practical = {}
        ports = {}
        port_guanabara = []
        port_sepetiba = []
        link = "http://www.praticagem-rj.com.br/"
        response = req.get(link)

        soup = BeautifulSoup(response.text)

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
                    "GT": tds[4].text,
                    "beam": tds[5].text,
                    "DWT": tds[6].text,  # probably deadweight_tonnage
                    "from": tds[7].text,
                    "to": tds[8].text,
                    "BRD": tds[9].text,
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
                    "GT": tds[4].text,
                    "beam": tds[5].text,
                    "DWT": tds[6].text,  # probably deadweight_tonnage
                    "from": tds[7].text,
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
                    "GT": tds[4].text,
                    "beam": tds[5].text,
                    "DWT": tds[6].text,  # probably deadweight_tonnage
                    "from": tds[7].text,
                    "to": tds[8].text,
                    "BRD": tds[9].text,
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
