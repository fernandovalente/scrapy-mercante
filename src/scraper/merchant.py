import requests as req

from bs4 import BeautifulSoup


class MerchantScraper:
    def __init__(self, cookie):
        self.cookie = cookie

    def get_data_from_portcall_id(self, portcall_id):
        json = {}
        link = "http://www.mercante.transportes.gov.br/g36127/servlet/serpro.siscomex.mercante.servlet.cadastro.EscalaSvlet"
        response = req.post(
            link,
            {"pagina": "ConsultaEscala", "NumEscala": portcall_id},
            headers={
                "Cookie": self.cookie,
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )

        soup = BeautifulSoup(response.text)
        tables = soup.find_all("table")

        def get_form_data(table, tr, td=1):
            return tables[table].find_all("tr")[tr].find_all("td")[td].text.strip()

        def quick_get_first_table(obj, fields):
            for i, f in enumerate(fields):
                obj[f] = get_form_data(1, i)

        quick_get_first_table(
            json,
            [
                "agency",
                "port",
                "vessel",
                "shipowner_trip_number",
                "operation_type",
                "flag",
                "responsible",
                "navigation_company",
                "transporter_nationality",
            ],
        )

        return json


scraper = MerchantScraper(
    "JSESSIONID=0000OB05qFFSdBttob-DhO2DZDb:CA0395646190A33600000A8C0000003E00000008"
)
data = scraper.get_data_from_portcall_id("20000350812")
print(data)