
import os
import re
from typing import List, Tuple


_INT_RE = re.compile(r"[+-]?\d+\Z")


def _normalize_newlines(s: str) -> str:
    # Accept Windows CRLF robustly by normalizing to '\n'
    s = s.replace("\r\n", "\n")
    s = s.replace("\r", "\n")
    return s


def _tokenize_ints(text: str) -> List[int]:
    toks = text.split()
    res: List[int] = []
    for i, tok in enumerate(toks, 1):
        if _INT_RE.fullmatch(tok) is None:
            raise ValueError(f"Input: invalid integer token #{i}: {tok!r}")
        # Python int is unbounded; that's fine.
        res.append(int(tok))
    return res


def _parse_input(input_text: str) -> Tuple[int, int, int, int, List[int], List[int]]:
    input_text = _normalize_newlines(input_text)
    ints = _tokenize_ints(input_text)
    if len(ints) < 4:
        raise ValueError("Input: expected at least 4 integers (n m k t).")
    n, m, k, t = ints[0], ints[1], ints[2], ints[3]

    # Basic sanity per statement constraints (should always hold in official tests).
    if not (1 <= n <= 100000):
        raise ValueError(f"Input: n out of range [1..100000], got n={n}.")
    if not (1 <= m <= 100000):
        raise ValueError(f"Input: m out of range [1..100000], got m={m}.")
    if not (1 <= k <= m):
        raise ValueError(f"Input: k out of range [1..m={m}], got k={k}.")
    if not (1 <= t <= 30):
        raise ValueError(f"Input: t out of range [1..30], got t={t}.")

    need = 4 + n + m
    if len(ints) != need:
        raise ValueError(f"Input: expected exactly {need} integers total, got {len(ints)}.")

    a = ints[4:4 + n]
    b = ints[4 + n:4 + n + m]
    return n, m, k, t, a, b


def _strict_parse_single_int_output(output_text: str) -> int:
    output_text = _normalize_newlines(output_text)

    # Allow exactly one trailing newline at EOF; otherwise be strict.
    if output_text.endswith("\n"):
        body = output_text[:-1]
        if "\n" in body:
            raise ValueError("Output: multiple lines detected; expected exactly one line.")
    else:
        body = output_text
        if "\n" in body:
            raise ValueError("Output: multiple lines detected; expected exactly one line.")

    if body == "":
        raise ValueError("Output: empty; expected one integer.")
    if body != body.strip():
        raise ValueError("Output: leading/trailing whitespace is not allowed.")
    if _INT_RE.fullmatch(body) is None:
        raise ValueError(f"Output: expected one integer token, got {body!r}.")
    return int(body)


def check(input_text: str, output_text: str) -> tuple[bool, str]:
    try:
        n, m, k, t, a, b = _parse_input(input_text)
    except ValueError as e:
        return False, str(e)

    try:
        s = _strict_parse_single_int_output(output_text)
    except ValueError as e:
        return False, str(e)

    if s < 0:
        return False, f"Output: radius s must be >= 0, got {s}."

    # Additional constraint that is derivable without solving:
    # Since k>=1 and t>=1, we can always activate exactly one lantern (one burst of length 1).
    # Therefore, the true minimum radius cannot exceed the best radius achievable by a single lantern:
    # min_j max(|a_min - b_j|, |a_max - b_j|).
    a_min = min(a)
    a_max = max(a)
    upper = None
    for bj in b:
        need = max(abs(a_min - bj), abs(a_max - bj))
        upper = need if upper is None else min(upper, need)

    # m>=1 => upper is set
    if upper is not None and s > upper:
        return (
            False,
            f"Output: s={s} is too large. Activating a single lantern can cover all outposts with "
            f"radius {upper}, so the minimum possible radius cannot exceed {upper}."
        )

    return True, "OK"


if __name__ == "__main__":
    in_path = os.environ.get("INPUT_PATH")
    out_path = os.environ.get("OUTPUT_PATH")
    if not in_path or not out_path:
        raise SystemExit("Missing INPUT_PATH or OUTPUT_PATH environment variables.")
    with open(in_path, "r", encoding="utf-8") as f:
        input_text_ = f.read()
    with open(out_path, "r", encoding="utf-8") as f:
        output_text_ = f.read()
    ok, _reason = check(input_text_, output_text_)
    print("True" if ok else "False")
