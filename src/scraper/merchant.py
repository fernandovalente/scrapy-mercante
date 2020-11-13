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

        def get_summary(obj, fields):
            for i, f in enumerate(fields):
                obj[f] = get_form_data(1, i)

        def get_partners(obj):
            obj["partners"] = []
            for tr in tables[2].find_all("tr")[1:]:
                tds = tr.find_all("td")
                obj["partners"].append((tds[0].text.strip(), tds[1].text.strip()))

        def get_procedent_ports(obj):
            obj["proceeding_ports"] = []
            for tr in tables[3].find_all("tr")[1:]:
                tds = tr.find_all("td")
                obj["proceeding_ports"].append(
                    (tds[0].text.strip(), tds[1].text.strip())
                )

        def get_subsequent_ports(obj):
            obj["subsequent_ports"] = []
            for tr in tables[4].find_all("tr")[1:]:
                tds = tr.find_all("td")
                obj["subsequent_ports"].append(
                    (tds[0].text.strip(), tds[1].text.strip())
                )

        get_summary(
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

        get_partners(json)
        get_procedent_ports(json)
        get_subsequent_ports(json)

        return json


if __name__ == "__main__":
    # Example for using Scraper
    scraper = MerchantScraper(
        "JSESSIONID=0000OB05qFFSdBttob-DhO2DZDb:CA0395646190A33600000A8C0000003E00000008"
    )
    data = scraper.get_data_from_portcall_id("20000350812")
    print(data)