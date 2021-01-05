import requests as req
from bs4 import BeautifulSoup
import string
import json as j


class VesselScraper:  # Related to vessel tracker
    def __init__(self):
        print("hi")

    def get_vessel_data(self):
        json = []
        for letter in string.ascii_uppercase:
            page = 1
            print(letter)
            while page < 400:
                link = f"https://www.vesseltracker.com/en/vessels.html?page={str(page)}&search={letter}"  # Gets summarized data from the pagination
                response = req.get(link)
                soup = BeautifulSoup(response.text, features="lxml")
                odds = soup.find_all(class_="row odd")  # Type of line in table
                evens = soup.find_all(class_="row even")  # Type of line in table
                json_row = {}
                if len(odds) == 0 and len(evens) == 0:  # Next iteration if empty page
                    break
                print(str(page))

                for odd in odds:
                    divs = odd.find_all("div")
                    name = divs[3].find_all("a")[0].text
                    imo = divs[4].text
                    AIS_type = ""
                    flag = ""
                    link_inner_data = f"https://www.vesseltracker.com/en/Ships/{name}-{imo}.html"  # Gets a couple of data from inside each ship
                    try:

                        response_inner_data = req.get(link_inner_data)
                        soup_inner_data = BeautifulSoup(
                            response_inner_data.text, features="lxml"
                        )
                        AIS_table = soup_inner_data.find_all(class_="key-value-table")
                        AIS_type = (
                            AIS_table[1].find_all(class_="col-xs-7 value")[0].text
                        )
                        flag = AIS_table[1].find_all(class_="col-xs-7 value")[2].text
                    except:
                        pass
                    print(name)
                    json_row = {
                        "name": name,
                        "description": divs[3].find_all("span")[0].text,
                        "imo": imo,
                        "AIS_type": AIS_type,
                        "flag": flag,  # Possibly translated as nacionality
                        "callsign": divs[5].text,
                        "mmsi": divs[6].text,
                        "len_x_wid_meters": divs[7].text,
                    }
                    json.append(json_row)

                for even in evens:
                    divs = even.find_all("div")
                    name = divs[3].find_all("a")[0].text
                    imo = divs[4].text
                    AIS_type = ""
                    flag = ""
                    link_inner_data = f"https://www.vesseltracker.com/en/Ships/{name}-{imo}.html"  # Gets a couple of data from inside each ship
                    try:

                        response_inner_data = req.get(link_inner_data)
                        soup_inner_data = BeautifulSoup(
                            response_inner_data.text, features="lxml"
                        )
                        AIS_table = soup_inner_data.find_all(class_="key-value-table")
                        AIS_type = (
                            AIS_table[1].find_all(class_="col-xs-7 value")[0].text
                        )
                        flag = AIS_table[1].find_all(class_="col-xs-7 value")[2].text
                    except:
                        pass
                    print(name)
                    json_row = {
                        "name": name,
                        "description": divs[3].find_all("span")[0].text,
                        "imo": imo,
                        "AIS_type": AIS_type,
                        "flag": flag,  # Possibly translated as nacionality
                        "callsign": divs[5].text,
                        "mmsi": divs[6].text,
                        "len_x_wid_meters": divs[7].text,
                    }
                    json.append(json_row)
                page = page + 1

        with open("boats_vesseltracker.json", "w") as outfile:
            j.dump(json, outfile)
            outfile.close()
        return json

    def get_ports_from_vesseltracker(self):
        json = []
        page = 1

        def get_data_from_rows(
            rows,
        ):  # generalization from getting evens and odds. TODO Apply this on getting vessels

            for row in rows:
                divs = row.find_all("div")
                name = divs[2].text
                flag = divs[1].text
                local_code = divs[3].text
                in_port = divs[5].text
                expected = divs[6].text
                json_row = {
                    "name": name,
                    "flag": flag,
                    "local_code": local_code,
                    "in_port": in_port,
                    "expected": expected,  # Possibly translated as nacionality
                }
                json.append(json_row)

        while page < 400:
            link = f"https://www.vesseltracker.com/en/ports.html?page={str(page)}"  # Gets summarized data from the pagination
            response = req.get(link)
            soup = BeautifulSoup(response.text, features="lxml")
            odds = soup.find_all(class_="row odd")  # Type of line in table
            evens = soup.find_all(class_="row even")  # Type of line in table
            json_row = {}
            if len(odds) == 0 and len(evens) == 0:  # Next iteration if empty page
                break
            print(f"Page: {str(page)}")
            get_data_from_rows(odds)
            get_data_from_rows(evens)

            page = page + 1

        with open("ports.json", "w") as outfile:
            j.dump(json, outfile)
            outfile.close()
        return json

    def get_vessels_from_vesselfinder(
        self,
    ):  # this functions is based on the boats_vesseltracker file. Mergin with the vesselfinder
        # Also this writes the data on boat completely, even with checkpoints. Meaning that it will always override.
        json_boats = []
        json_vesseltracker = []  # possible data from vesseltracker

        with open("boats.json", "r") as outfile:
            try:
                json_boats = j.load(outfile)
            except:
                json_boats = []
            outfile.close()

        with open("boats_vesseltracker.json", "r") as outfile:
            json_vesseltracker = j.load(outfile)
            outfile.close()

        i = 0
        updated_vessel = {
            "name": "",
            "description": "",
            "imo": "",
            "AIS_type": "",
            "flag": "",  # Possibly translated as nacionality
            "callsign": "",
            "mmsi": "",
            "len_x_wid_meters": "",
            "len": "",
            "beam": "",
            "ship_type": "",
            "gross_tonnage": "",
            "summer_dwt": "",
            "year_built": "",
        }
        updated_json = []
        i = 0
        vessel_unit = 6001
        for vessel in json_vesseltracker:
            i = i + 1
            if i < vessel_unit:
                continue
            try:
                print(vessel["name"])

                vessel_name = vessel["name"]
                vessel_imo = vessel["imo"]
                vessel_mmsi = vessel["mmsi"]
                headers = {"User-Agent": "Mozilla/5.0"}
                link = f"https://www.vesselfinder.com/vessels/{vessel_name}-IMO-{vessel_imo}-MMSI-0"  # Gets summarized data from the pagination
                response = req.get(link, headers=headers)
                soup = BeautifulSoup(response.text, features="lxml")

                vessel_section = soup.find_all(
                    class_="tparams"
                )  # Type of line in table
                trs_particulars = vessel_section[3].find_all(
                    class_="v3"
                )  # v3 is the value column
                ship_type = trs_particulars[2].text
                gross_tonnage = trs_particulars[5].text
                summer_dwt = trs_particulars[6].text
                vessel_len = trs_particulars[7].text
                beam = trs_particulars[8].text
                year_built = trs_particulars[10].text
                vessel_from_finder = {
                    "len": vessel_len,
                    "beam": beam,
                    "ship_type": ship_type,
                    "gross_tonnage": gross_tonnage,
                    "summer_dwt": summer_dwt,
                    "year_built": year_built,
                }
                updated_vessel = {
                    "name": vessel["name"],
                    "description": vessel["description"],
                    "imo": vessel["imo"],
                    "AIS_type": vessel["AIS_type"],
                    "flag": vessel["flag"],  # Possibly translated as nacionality
                    "callsign": vessel["callsign"],
                    "mmsi": vessel["mmsi"],
                    "len_x_wid_meters": f"{vessel_len} x {beam}",
                    "ship_type": ship_type,
                    "gross_tonnage": gross_tonnage,
                    "summer_dwt": summer_dwt,
                    "year_built": year_built,
                }
                updated_json.append(updated_vessel)
            except Exception as e:
                updated_json.append(
                    {"status": "error", "vessel_name": vessel_name, "imo": vessel_imo}
                )
                continue
            finally:
                checkpoint = i % 1000
                json_boats_complete = []
                json_boats_complete = json_boats + updated_json  # what is on file
                # what was previously on file + what was scrapped
                if checkpoint == 0:
                    print(i)
                    with open("boats.json", "w") as outfile:
                        j.dump(json_boats_complete, outfile)
                        outfile.close()

        with open("boats.json", "w") as outfile:
            j.dump(updated_json, outfile)
            outfile.close()

        return updated_json
