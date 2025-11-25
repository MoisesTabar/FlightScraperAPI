from scraper.types import SearchParamsType

def ensure_list_with_min_len(value: SearchParamsType, field_name: str) -> None:
    if not isinstance(value, list) or len(value) < 2:
        raise ValueError(
            f"A {field_name} must be a list with at least two elements for multi-city tickets"
        )
