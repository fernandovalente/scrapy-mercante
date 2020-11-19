import requests as req

from bs4 import BeautifulSoup


class PortosRio:
    def get_data_from_date(date):
        url = "http://www.portosrio.gov.br/prognav"
        body = {"data": date, "submit": "enviar"}

        response = req.post(url, body)
        soup = BeautifulSoup(response.text)
        data = []

        table = soup.get_all("table")[0]

        for tr in table.get_all("tbody")[0].get_all("tr"):
            tds = table.get_all("td")

            data.append(
                {
                    "terminal": tds[0],
                    "local": tds[1],
                    "procedence": tds[2],
                    "atrac": tds[3],
                    "agops": tds[4],
                    "vessel": tds[5],
                    "daytime_terno": tds[6],
                    "daytime_equip": tds[7],
                    "daytime_operation": tds[8],
                    "nocturnal_terno": tds[9],
                    "nocturnal_operation": tds[10],
                    "nocturnal_equip": tds[11],
                    "cabeco_start": tds[12],
                    "cabeco_end": tds[13],
                    "start": tds[14],
                    "cargo": tds[15],
                    "weight": tds[16],
                }
            )

        return data
