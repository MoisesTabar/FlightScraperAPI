from scraper.scraper import search_flights
from scraper.models import SearchParams, Flight
from fastapi import APIRouter, HTTPException


router = APIRouter()


@router.post("/search", response_model=list[Flight])
async def search_flight(params: SearchParams) -> list[Flight]:
    return await search_flights(params)
