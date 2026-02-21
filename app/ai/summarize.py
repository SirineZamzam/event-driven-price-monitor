def summarize_price_change(source, item, old_price, new_price, currency):

    if old_price is None:
        summary = f"{item} was first observed at {new_price} {currency}."
    else:
        change = new_price - old_price

        if change > 0:
            summary = f"{item} increased by {change:.2f} {currency}."
        elif change < 0:
            summary = f"{item} decreased by {abs(change):.2f} {currency}."
        else:
            summary = f"{item} price unchanged."

    prompt = "MOCK_SMART_SUMMARIZER"
    model = "local-rule-v2"

    return summary, prompt, model