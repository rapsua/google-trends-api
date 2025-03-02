from fastapi import FastAPI
from pytrends.request import TrendReq
import pandas as pd

app = FastAPI()
pytrends = TrendReq(hl="es-ES", tz=360)

@app.get("/")
def home():
    return {"message": "API de Google Trends funcionando correctamente"}

@app.get("/trends/")
def get_trends(keyword: str, geo: str = "ES", timeframe: str = "today 12-m"):
    """
    Obtiene datos de tendencia de Google Trends para una palabra clave.
    Parámetros:
      - keyword: Término de búsqueda
      - geo: Región (por defecto "ES" para España)
      - timeframe: Período de búsqueda (por defecto "today 12-m" para el último año)
    """
    pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo=geo, gprop="")
    data = pytrends.interest_over_time()

    if data.empty:
        return {"error": "No hay datos disponibles para esta consulta"}

    return data.drop(columns=["isPartial"]).to_dict()
