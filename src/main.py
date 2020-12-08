from typing import Optional

from fastapi import FastAPI, Response
from mangum import Mangum

from .scraper.merchant.main import MerchantScraper
from .scraper.practical.main import PracticalScraper
from .scraper.vessel.main import VesselScraper
from .scraper.portosrio.main import PortosRio

app = FastAPI()


@app.get("/merchant/portcall/{portcall_id}")
def get_merchant(portcall_id: str, response: Response):
    scraper = MerchantScraper()

    try:
        return scraper.get_data_from_portcall_id(portcall_id)
    except Exception as e:
        response.status_code = 400
        return e


@app.get("/merchant/portcalls/{start_date}/{end_date}/{port}")
def get_portcalls(start_date: str, end_date: str, port: str, response: Response):
    scraper = MerchantScraper()

    try:
        return scraper.list_portcalls_by_date(start_date, end_date, port)
    except Exception as e:
        response.status_code = 400
        return e


@app.get("/merchant/vessel/{imo}")
def get_vessel(imo: str, response: Response):
    scraper = MerchantScraper()

    try:
        return scraper.get_data_from_vessel_imo(imo)
    except Exception as e:
        response.status_code = 400
        return e


@app.get("/portosrio/{date}")
def get_portosrio(date: str, response: Response):
    scraper = PortosRio()
    response.headers["Content-Type"] = "application/json; charset=utf-8"

    try:
        return scraper.get_data_from_date(date)
    except Exception as e:
        print(e)
        response.status_code = 400
        return e


@app.get("/practical/rj/history/{date}")
def get_pratical_rj_history(date: str, response: Response):
    scraper = PracticalScraper()
    response.headers["Content-Type"] = "application/json; charset=utf-8"

    try:
        return scraper.get_data_from_pratical_rj_history(date)
    except Exception as e:
        print(e)
        response.status_code = 400
        return e


@app.get("/practical/rj/")
def get_practical_rj(response: Response):
    scraper = PracticalScraper()

    try:
        return scraper.get_data_from_practical_rj()
    except Exception as e:
        response.status_code = 400
        return e


@app.get("/vesseltracker/vessels/")
def get_vessels_from_vt(response: Response):
    scraper = VesselScraper()

    try:
        return scraper.get_vessel_data()
    except Exception as e:
        response.status_code = 400
        return e


@app.get("/vesseltracker/ports/")
def get_vessels_from_vt(response: Response):
    scraper = VesselScraper()

    try:
        return scraper.get_ports_from_vesseltracker()
    except Exception as e:
        response.status_code = 400
        return e


handler = Mangum(app)
