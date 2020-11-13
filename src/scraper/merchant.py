import requests as req

from bs4 import BeautifulSoup


def get_data():
    json = {}
    link = "http://www.mercante.transportes.gov.br/g36127/servlet/serpro.siscomex.mercante.servlet.cadastro.EscalaSvlet"
    response = req.post(
        link,
        {"pagina": "ConsultaEscala", "NumEscala": "20000350812"},
        headers={
            "Cookie": "JSESSIONID=0000OB05qFFSdBttob-DhO2DZDb:CA0395646190A33600000A8C0000003E00000008",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    soup = BeautifulSoup(response.text)
    tables = soup.find_all("table")

    def get_form_data(table, tr, td=1):
        return tables[table].find_all("tr")[tr].find_all("td")[td].text

    agency = get_form_data(1, 1)
    port = get_form_data(1, 2)
    vessel = get_form_data(1, 3)
    shipowner_trip_number = get_form_data(1, 4)
    operation_type = get_form_data(1, 5)

    print(operation_type)


get_data()