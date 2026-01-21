import re


def split_into_clauses(text: str) -> list[str]:
    """
    Split contract text into logical clauses using
    numbered sections and headings.
    """

    if not text:
        return []

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Pattern for numbered clauses like "1.", "2.", "3.1"
    clause_pattern = re.compile(
        r"(?:^|\s)(\d+\.\s+)",
        re.MULTILINE
    )

    splits = clause_pattern.split(text)

    clauses = []
    current_clause = ""

    for part in splits:
        if re.match(r"\d+\.\s+", part):
            if current_clause:
                clauses.append(current_clause.strip())
            current_clause = part
        else:
            current_clause += " " + part

    if current_clause:
        clauses.append(current_clause.strip())

    # Filter out very small fragments
    cleaned_clauses = [
        c for c in clauses if len(c) > 100
    ]

    return cleaned_clauses
