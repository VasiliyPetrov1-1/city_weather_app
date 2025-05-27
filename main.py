import uuid
from fastapi import FastAPI, Request, Response, Cookie
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from core.facade import WeatherFacade
from services.geocoding import OpenStreetMapGeocoder
from services.weather import OpenMeteoWeatherProvider

app = FastAPI()
user_search_history = {}
city_search_counts = {}
templates = Jinja2Templates(directory="templates")
index_file = "index.html"


facade = WeatherFacade(
    geocoder=OpenStreetMapGeocoder(),
    weather_provider=OpenMeteoWeatherProvider()
)


def get_user_id(user_id: str = Cookie(default=None)):
    if user_id is None:
        user_id = str(uuid.uuid4())
    return user_id


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, user_id: str = Cookie(default=None)):
    if user_id is None:
        user_id = str(uuid.uuid4())

    last_city = None
    if user_id in user_search_history and user_search_history[user_id]:
        last_city = user_search_history[user_id][-1]

    template_response = templates.TemplateResponse(
        index_file,
        {"request": request, "last_city": last_city}
    )

    if user_id is not None:
        template_response.set_cookie(key="user_id", value=user_id)

    return template_response


@app.get("/weather", response_class=HTMLResponse)
async def get_weather(request: Request, city: str, user_id: str = Cookie(default=None)):
    if user_id is None:
        user_id = str(uuid.uuid4())

    coords = await facade.geocode(city)
    if coords is None:
        template_response = templates.TemplateResponse(
            index_file, {"request": request, "error": "City not found"}
        )
        template_response.set_cookie(key="user_id", value=user_id)
        return template_response

    forecast = await facade.get_weather(coords)

    user_search_history.setdefault(user_id, [])
    if city not in user_search_history[user_id]:
        user_search_history[user_id].append(city)

    city_search_counts[city] = city_search_counts.get(city, 0) + 1

    template_response = templates.TemplateResponse(
        index_file,
        {
            "request": request,
            "city": city,
            "forecast": forecast
        }
    )
    template_response.set_cookie(key="user_id", value=user_id)

    return template_response


@app.get("/autocomplete")
async def autocomplete(city: str):
    results = await facade.geocode_suggestions(city)
    return JSONResponse(content=results)


@app.get("/user_history", response_class=HTMLResponse)
async def get_user_history(request: Request, user_id: str = Cookie(default=None)):
    history = user_search_history.get(user_id, [])
    return templates.TemplateResponse("user_history.html", {
        "request": request,
        "history": history
    })


@app.get("/stats", response_class=HTMLResponse)
async def get_stats(request: Request):
    return templates.TemplateResponse("stats.html", {
        "request": request,
        "stats": city_search_counts
    })
