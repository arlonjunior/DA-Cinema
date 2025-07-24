# nls_utils.py

import re
import streamlit as st
from collections import defaultdict
from rapidfuzz import process, fuzz

@st.cache_data
def parse_entity(
    query: str,
    candidates: list[str],
    full_cutoff: int = 60,
    token_cutoff: int = 80
) -> str | None:
    """
    1) Exact substring match
    2) Fuzzy-partial match on whole query
    3) Token-level fuzzy: match each word in query against
       each actor name component.
    """
    if not query or not candidates:
        return None

    q = query.lower()

    # 1) exact substring
    for cand in candidates:
        if cand.lower() in q:
            return cand

    # 2) fuzzy-partial on full query
    match = process.extractOne(q, candidates, scorer=fuzz.partial_ratio)
    if match and match[1] >= full_cutoff:
        return match[0]

    # 3) build a map of each name-token → full candidate
    token_map: dict[str, list[str]] = defaultdict(list)
    for cand in candidates:
        for part in re.findall(r"\w+", cand.lower()):
            token_map[part].append(cand)

    # try token-level matches
    best_candidate, best_score = None, token_cutoff
    for token in re.findall(r"\w+", q):
        if len(token) < 2:
            continue
        # 3a) direct token hit
        if token in token_map:
            return token_map[token][0]
        # 3b) fuzzy over token_map keys
        m = process.extractOne(token, list(token_map.keys()), scorer=fuzz.ratio)
        if m and m[1] > best_score:
            best_candidate = token_map[m[0]][0]
            best_score = m[1]

    return best_candidate

