from typing import Optional

from fastapi import FastAPI, Response
from scraper.merchant import MerchantScraper
from scraper.merchant.utils import get_cookie

app = FastAPI()


@app.get("/merchant/{portcall_id}")
def read_root(portcall_id: str, response: Response):
    scraper = MerchantScraper()

    try:
        return scraper.get_data_from_portcall_id(portcall_id)
    except Exception as e:
        response.status_code = 400
        return e
