import requests as req

from bs4 import BeautifulSoup


class PortosRio:
    def get_data_from_date(self, date):
        url = "http://www.portosrio.gov.br/prognav"
        body = {"data": date, "submit": "enviar"}

        response = req.post(url, body)
        soup = BeautifulSoup(response.text)
        data = []

        table = soup.find_all("table")[0]

        for tr in table.find_all("tbody")[0].find_all("tr"):
            tds = tr.find_all("td")

            data.append(
                {
                    "terminal": tds[0].text,
                    "local": tds[1].text,
                    "procedence": tds[2].text,
                    "atrac": tds[3].text,
                    "agops": tds[4].text,
                    "vessel": tds[5].text,
                    "daytime_terno": tds[6].text,
                    "daytime_equip": tds[7].text,
                    "daytime_operation": tds[8].text,
                    "nocturnal_terno": tds[9].text,
                    "nocturnal_operation": tds[10].text,
                    "nocturnal_equip": tds[11].text,
                    "cabeco_start": tds[12].text,
                    "cabeco_end": tds[13].text,
                    "start": tds[14].text,
                    "cargo": tds[15].text,
                    "weight": tds[16].text,
                }
            )

        return data
