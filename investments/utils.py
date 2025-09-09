import requests
from bcb import sgs


def get_selic_rate():
    url = (
        "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados?formato=json")
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        latest_rate = data[-1]["valor"]
        return float(latest_rate)
    else:
        return None


def get_cdi_rate():
    cdi_data = sgs.get({"cdi": 4389})
    if not cdi_data.empty:
        return cdi_data.iloc[-1]["cdi"]
    return None


def get_tjlp_rate():
    tjlp_data = sgs.get({"tjlp": 256})
    if not tjlp_data.empty:
        return tjlp_data.iloc[-1]["tjlp"]
    return None
