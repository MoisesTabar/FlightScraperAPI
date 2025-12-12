from .constants.selectors import (
    RESULTS_SELECTORS,
    ADD_FLIGHT_BUTTON_SELECTOR,
    ADULT_PER_INFANTS_ON_LAP_ERROR_SELECTOR,
    NO_FLIGHTS_ERROR_SELECTOR,
    FLIGHTS_SELECTOR
)

from playwright.async_api import Page, ElementHandle, Locator
from .errors import AdultPerInfantsOnLapError, NoFlightsFoundError

from asyncio import create_task, wait, FIRST_COMPLETED


async def process_flight(page: ElementHandle) -> dict:
    flight_info = {}

    for key, selector in RESULTS_SELECTORS.items():
        element = await page.query_selector(selector)
        flight_info[key] = await element.text_content() if element else None

    return flight_info


async def process_date_selectors(page: Page, date_selector_type: str, date: str) -> None:
    date_input = page.locator(date_selector_type).first
    await date_input.fill(date)
    await date_input.press("Enter")


async def process_flight_selectors(page: Page, flight_selector: str, value: str) -> None:
    flight_input = page.locator(flight_selector).first
    await flight_input.fill(value)
    await page.locator("li").filter(has_text=value).nth(0).click()


async def process_multi_city_selectors(locator: Locator, value: str) -> None:
    await locator.scroll_into_view_if_needed()
    await locator.focus()
    await locator.fill(value)
    

async def spawn_multi_city_selectors(page: Page, city_amount: int) -> None:
    await page.locator(ADD_FLIGHT_BUTTON_SELECTOR).first.wait_for(state='visible', timeout=800)
    await page.locator(ADD_FLIGHT_BUTTON_SELECTOR).first.click(click_count=city_amount)
    await page.wait_for_timeout(500)


async def ensure_popover_is_closed(page: Page) -> None:
    try:
        await page.keyboard.press("Escape")
        await page.get_by_role("dialog").first.wait_for(state='hidden', timeout=1000)
    except Exception:
        pass


async def show_adult_per_infants_on_lap_error(page: Page) -> None:
    error_message = await page.locator(
        ADULT_PER_INFANTS_ON_LAP_ERROR_SELECTOR
    ).first.text_content()
    if error_message:
        raise AdultPerInfantsOnLapError(error_message)


async def _wait_for_no_flights_error(page: Page) -> str:
    error_element = page.locator(NO_FLIGHTS_ERROR_SELECTOR).first
    await error_element.wait_for(state='visible', timeout=0)
    return await error_element.text_content()


async def _wait_for_flights(page: Page) -> None:
    flights_element = page.locator(FLIGHTS_SELECTOR).first
    await flights_element.wait_for(state='visible', timeout=0)


async def show_no_flights_found_error(page: Page) -> None:
    error_task = create_task(_wait_for_no_flights_error(page))
    flights_task = create_task(_wait_for_flights(page))
    
    done, pending = await wait(
        [error_task, flights_task],
        return_when=FIRST_COMPLETED
    )
    
    for task in pending:
        task.cancel()
    
    if error_task in done:
        error_message = error_task.result()
        if error_message:
            raise NoFlightsFoundError(error_message)
