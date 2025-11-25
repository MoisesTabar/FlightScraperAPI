from typing import Literal


STOP_AFTER_ATTEMPTS: int = 5

RESULTS_SELECTORS: dict[str, str] = {
    "airline": "div.sSHqwe.tPgKwe.ogfYpf",
    "departure_time": 'span[aria-label^="Departure time"]',
    "arrival_time": 'span[aria-label^="Arrival time"]',
    "duration": 'div[aria-label^="Total duration"]',
    "stops": "div.hF6lYb span.rGRiKd",
    "price": "div.FpEdX span",
}

FLIGHTS_PAGE_URL: Literal = "https://www.google.com/flights"
FLIGHTS_AUTOMATIC_MULTI_CITY_SPAWN: int = 2

TICKET_TYPE_SELECTOR: Literal = "div.VfPpkd-TkwUic[jsname='oYxtQd']"
FLIGHT_TYPE_SELECTOR: Literal = "div.TQYpgc[jsname='zkxPxd']"
PASSENGER_BUTTON_SELECTOR: Literal = "div[jsname='QqIbod'] button[jsname='LgbsSe'][aria-haspopup='dialog']"

ADULT_PASSENGERS_SELECTOR: Literal = "div[jsname='mMhAUc']"
CHILDREN_PASSENGERS_SELECTOR: Literal = "div[jsname='LpMIEc']"
INFANTS_SEAT_PASSENGERS_SELECTOR: Literal = "div[jsname='u3Jn2e']"
INFANTS_LAP_PASSENGERS_SELECTOR: Literal = "div[jsname='TwhQhe']"
PASSENGER_INCREMENT_BUTTON: Literal = "button[jsname='TdyTDe']"
PASSENGER_DECREMENT_BUTTON: Literal = "button[jsname='DUGJie']"
PASSENGER_DONE_BUTTON: Literal = "button[jsname='McfNlf']"

FROM_SELECTOR: Literal = "input[aria-label^='Where from?']"
TO_SELECTOR: Literal = "input[aria-label^='Where to?']"
DEPARTURE_DATE_SELECTOR: Literal = "input[aria-label^='Departure']"
RETURN_DATE_SELECTOR: Literal = "input[aria-label^='Return']"

SEARCH_BUTTON_SELECTOR: Literal = "button[aria-label^='Search']"

ADD_FLIGHT_BUTTON_SELECTOR: Literal = "button[jsname='htvI8d']"

BROWSER_ARGS = [
    "--disable-blink-features=AutomationControlled",
    "--disable-dev-shm-usage",
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-web-security",
    "--disable-features=IsolateOrigins,site-per-process",
    "--disable-site-isolation-trials",
    "--disable-accelerated-2d-canvas",
    "--disable-gpu",
    "--disable-extensions",
    "--disable-software-rasterizer",
    "--disable-dev-tools",
    "--disable-browser-side-navigation",
    "--disable-notifications",
    "--disable-popup-blocking",
    "--disable-background-timer-throttling",
    "--disable-backgrounding-occluded-windows",
    "--disable-renderer-backgrounding",
    "--disable-ipc-flooding-protection",
    "--disable-hang-monitor",
    "--disable-sync",
    "--metrics-recording-only",
    "--mute-audio",
    "--no-first-run",
    "--safebrowsing-disable-auto-update",
    "--password-store=basic",
    "--use-mock-keychain",
]

BLOCKED_EXTENSIONS = (
    ".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"
)

BLOCKED_DOMAINS = (
    "analytics", 
    "google-analytics", 
    "googletagmanager", 
    "doubleclick", 
    "facebook", 
    "twitter"
)

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"