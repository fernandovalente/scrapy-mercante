import requests as req
import time
from bs4 import BeautifulSoup


class MerchantScraper:
    def __init__(self):
        self.get_cookie()

    def get_cookie(self):
        session = req.Session()
        r = session.post(
            "http://www.mercante.transportes.gov.br/g36127/servlet/serpro.siscomex.mercante.servlet.MercanteController",
            {
                "Tipo MIME": "application/x-www-form-urlencoded",
                "cpf": "pmercpr",
                "senha": "publica",
                "sistema": "MERCANTE",
                "acao": "logon",
                "passo": "1",
            },
        )

        cookies = session.cookies.get_dict()

        self.cookie = f"JSESSIONID={cookies['JSESSIONID']}"

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

        try:
            get_summary(
                json,
                [
                    "_id",
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
        except:
            raise Exception(response.text)

        return json

    def list_portcalls_by_date(self, start_date, end_date, port):
        json = {}
        link = "http://www.mercante.transportes.gov.br/g36127/servlet/serpro.siscomex.mercante.servlet.cadastro.EscalaSvlet"
        response = req.post(
            link,
            {
                "pagina": "ConsultaEscala",
                "NumEscala": "",
                "DtInicial": start_date,
                "DtFinal": end_date,
                "IMO": "",
                "Porto": port,
            },
            headers={
                "Cookie": self.cookie,
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        soup = BeautifulSoup(response.text)
        table = soup.find_all("table")[2]
        list_json = []
        for tr in table.find_all("tr")[1:]:
            tds = tr.find_all("td")
            json = {
                "id": tds[0].text.strip(),
                "eta": tds[1].text.strip(),
                "agency": tds[2].text.strip(),
                "vessel": tds[3].text.strip(),
            }
            list_json.append(json)

        return list_json

    def get_data_from_vessel_imo(self, imo):
        json = {}
        link = "http://www.mercante.transportes.gov.br/g36127/servlet/tabelas.embarc.EmbarcSvlet"
        response = req.post(
            link,
            {"pagina": "EmbarcConPub", "coEmbarc": imo, "noEmbarc": ""},
            headers={
                "Cookie": self.cookie,
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )

        soup = BeautifulSoup(response.text)
        table = soup.find_all("table")[0]
        trs = table.find_all("tr")

        json = {
            "imo": trs[0].find_all("td")[1].text.strip(),
            "description": trs[1].find_all("td")[1].text.strip(),
            "irin": trs[2].find_all("td")[1].text.strip(),
            "nacionality": trs[3].find_all("td")[1].text.strip(),
            "shipowner": trs[4].find_all("td")[1].text.strip(),
            "traffic_type": trs[5].find_all("td")[1].text.strip(),
            "vessel_type": trs[6].find_all("td")[1].text.strip(),
            "shipyard": trs[7].find_all("td")[1].text.strip(),
            "build_year": trs[8].find_all("td")[1].text.strip(),
            "vessel_operating": trs[9].find_all("td")[1].text.strip(),
            "carry_containers": trs[10].find_all("td")[1].text.strip(),
            "REB": trs[11].find_all("td")[1].text.strip(),
            "BHP_power": trs[12].find_all("td")[1].text.strip(),
            "container_cap_20_feet": trs[13].find_all("td")[1].text.strip(),
            "gross_tonnage": trs[14].find_all("td")[1].text.strip(),
            "vessel_length": trs[15].find_all("td")[1].text.strip(),
            "vessel_draft": trs[16].find_all("td")[1].text.strip(),
            "hull_number": trs[8].find_all("td")[3].text.strip(),
            "transports_bulk": trs[9].find_all("td")[3].text.strip(),
            "foreign_company_sell": trs[10].find_all("td")[3].text.strip(),
            "deadweight_tonnage": trs[11].find_all("td")[3].text.strip(),
            "cargo_cap": trs[12].find_all("td")[3].text.strip(),
            "net_tonnage": trs[13].find_all("td")[3].text.strip(),
            "knot_speed": trs[14].find_all("td")[3].text.strip(),
            "beam": trs[15].find_all("td")[3].text.strip(),
            "static_traction_tonnage": trs[16].find_all("td")[3].text.strip(),
        }
        return json
