from enum import StrEnum

type SearchParamsType = list[str] | str

class TicketType(StrEnum):
    one_way = "One Way"
    round_trip = "Round Trip"
    multi_city = "Multi-City"


class FlightType(StrEnum):
    economy = "Economy"
    premium_economy = "Premium Economy"
    business = "Business"
    first = "First"


class PassengerType(StrEnum):
    adult = "Adult"
    children = "Children"
    infant_seat = "Infants In Seat"
    infant_lap = "Infants On Lap"

type PassengersType = dict[PassengerType, int]