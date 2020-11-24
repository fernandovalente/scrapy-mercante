import requests as req

from bs4 import BeautifulSoup


class PortosRio:
<<<<<<< HEAD
    def get_data_from_date(date):
=======
    def get_data_from_date(self, date):
>>>>>>> 9726979200e7753c9d395cd0b6de36f4de628cb8
        url = "http://www.portosrio.gov.br/prognav"
        body = {"data": date, "submit": "enviar"}

        response = req.post(url, body)
        soup = BeautifulSoup(response.text)
        data = []

<<<<<<< HEAD
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
=======
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
>>>>>>> 9726979200e7753c9d395cd0b6de36f4de628cb8
                }
            )

        return data
