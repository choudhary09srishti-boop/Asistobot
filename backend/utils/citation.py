def format_sources(chunks, indices):
    sources = []

    for i in indices[0]:
        if i < len(chunks):
            sources.append(chunks[i])

    return sources