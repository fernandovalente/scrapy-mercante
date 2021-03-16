import requests as req
import time
from bs4 import BeautifulSoup
from datetime import date
import json as j


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
            try:
                return tables[table].find_all("tr")[tr].find_all("td")[td].text.strip()
            except:
                return ""

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

            json["etb"] = (get_form_data(1, 10) + " " + get_form_data(1, 10, 3)).strip()
            json["atb"] = (get_form_data(1, 11) + " " + get_form_data(1, 11, 3)).strip()
            json["ets"] = (get_form_data(1, 12) + " " + get_form_data(1, 12, 3)).strip()
            json["ats"] = (get_form_data(1, 13) + " " + get_form_data(1, 13, 3)).strip()

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

        today = date.today()
        filename = f"portcalls_{today}.json"
        print(filename)

        return list_json

    def list_portcalls_by_date_on_file_from_port_list(self, start_date, end_date):
        link = "https://ports.s3.amazonaws.com/only_br_ports.json"  # port data to search by their codes
        response = req.get(link)
        br_ports_data = response.json()["database_portdata"]
        list_json = []
        for br_port in br_ports_data:
            try:
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
                        "Porto": br_port["code"],
                    },
                    headers={
                        "Cookie": self.cookie,
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                )
                soup = BeautifulSoup(response.text)
                table = soup.find_all("table")[2]
                for tr in table.find_all("tr")[1:]:
                    tds = tr.find_all("td")
                    json = {
                        "id": tds[0].text.strip(),
                        "eta": tds[1].text.strip(),
                        "agency": tds[2].text.strip(),
                        "vessel": tds[3].text.strip(),
                    }
                    list_json.append(json)

                today = date.today()
                filename = f"portcalls_{today}.json"
                print(filename)

                with open(filename, "w") as outfile:
                    j.dump(list_json, outfile, indent=4, sort_keys=True)
            except:
                continue

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

    def get_merchant_ports_of_country(self, country_code):
        ###
        # TODO: This code is incomplete. It doesn't look through the pages from 2 to n-1.
        ###
        json = {}
        data = []
        link = "https://www.mercante.transportes.gov.br/g36127/servlet/tabelas.porto.PortoSvlet"
        for br_port in br_ports_data:
            response = req.post(
                link,
                {
                    "pagina": "PortoConsul2",
                    "coPais": country_code,
                },
                headers={
                    "Cookie": self.cookie,
                    "Content-Type": "application/x-www-form-urlencoded",
                    "User-Agent": "Mozilla/5.0",
                },
                verify=False,
            )

            soup = BeautifulSoup(response.text)
            tds = soup.find_all(class_="td2")
            tds_iterator = iter(tds)
            for code, name in zip(
                tds_iterator, tds_iterator
            ):  # zips each 2 elements of new_list in a tuple
                code = code.text.strip()
                name = name.text.strip()
                data.append({"code": code, "name": name})

        return data

    def get_merchant_ports_name_by_code(self):
        link = "https://ports.s3.amazonaws.com/only_br_ports.json"  # port data to search by their codes
        response = req.get(link)
        br_ports_data = response.json()["database_portdata"]
        json = {}
        data = []
        link = "http://www.mercante.transportes.gov.br/g36127/servlet/tabelas.porto.PortoSvlet"
        for br_port in br_ports_data:
            try:
                response = req.post(
                    link,
                    {
                        "pagina": "PortoConsul2",
                        "coPorto": br_port["code"],
                    },
                    headers={
                        "Cookie": self.cookie,
                        "Content-Type": "application/x-www-form-urlencoded",
                        "User-Agent": "Mozilla/5.0",
                    },
                )

                soup = BeautifulSoup(response.text, features="lxml")
                tds = soup.find_all(class_="td2")
                code = tds[0].text.strip()
                print(code)
                name = tds[1].text.strip()
                print(name)
                data.append({"code": code, "name": name})

            except Exception as e:
                print(e)
                continue

        return data