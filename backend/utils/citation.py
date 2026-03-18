def format_citation(chunk):
    source = chunk.get("source", "unknown")
    page   = chunk.get("page", "?")
    para   = chunk.get("para", "?")

    # Get just the filename from full path
    if "/" in source:
        source = source.split("/")[-1]
    if "\\" in source:
        source = source.split("\\")[-1]

    return {
        "source": source,
        "page": page,
        "para": para,
        "text": chunk.get("text", ""),
        "label": f"{source} · p.{page} ¶{para}"
    }


def format_all_citations(chunks):
    return [format_citation(chunk) for chunk in chunks]
