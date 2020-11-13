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
    agency = tables[1].find_all("tr")[1].find_all("td")[1].text

    print(agency)


get_data()