#!/usr/bin/env python3
"""Regression tests for Google Docs UTF-16 index math and link spacing."""

from publish import _to_api_index, _utf16_len, parse_markdown_to_doc_content


def test_emoji_shifts_api_index():
    prefix = "Associates\n🎉 Someone\n\nWeekly Updates\nData Processing\n"
    py_idx = prefix.find("Data Processing") + len("Data Processing") + 1
    api_idx = _to_api_index(prefix, py_idx)
    assert api_idx == py_idx + 1, (py_idx, api_idx)
    assert api_idx == _utf16_len(prefix[:py_idx])


def test_ascii_indices_match():
    text = "Weekly Updates\nData Processing\nhello\nNotebooks\n"
    py_idx = text.find("Data Processing") + len("Data Processing") + 1
    assert _to_api_index(text, py_idx) == py_idx


def test_spaces_preserved_around_links():
    md = (
        "- Completed the [module PR](https://example.com/a) and "
        "[manifest packaging](https://example.com/b) in midstream.\n"
    )
    parsed = parse_markdown_to_doc_content(md)
    text = parsed["text"]
    assert "the module PR and manifest packaging in" in text

    for start, end, _url in parsed["links"]:
        # Walk UTF-16 offsets back to Python slice
        def slice_u16(s, a, b):
            i = 0
            pa = pb = None
            for pi, ch in enumerate(s):
                if i == a:
                    pa = pi
                if i == b:
                    pb = pi
                    break
                i += len(ch.encode("utf-16-le")) // 2
            if pb is None:
                pb = len(s)
            return s[pa:pb], pa, pb

        _linked, pa, pb = slice_u16(text, start, end)
        before = text[pa - 1] if pa else ""
        after = text[pb] if pb < len(text) else ""
        assert before in (" ", "\n"), f"missing space before link: {before!r}"
        assert after in (" ", ",", ".", "\n", "a"), f"unexpected after link: {after!r}"


if __name__ == "__main__":
    test_emoji_shifts_api_index()
    test_ascii_indices_match()
    test_spaces_preserved_around_links()
    print("ok")
