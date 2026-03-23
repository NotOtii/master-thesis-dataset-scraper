def validate_book_item(item: dict) -> tuple[bool, list[str]]:
    errors = []

    if not item.get("title"):
        errors.append("Missing title")

    if item.get("price_gbp") is None:
        errors.append("Missing price_gbp")
    elif not isinstance(item.get("price_gbp"), (int, float)):
        errors.append("price_gbp is not numeric")

    if not item.get("product_page_url"):
        errors.append("Missing product_page_url")

    return len(errors) == 0, errors