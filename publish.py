#!/usr/bin/env python3
"""
Google Docs Publisher - writes the Data Processing section and any
secondary sections (Risks/Issues, Customers, Associates) to the live
AAET Weekly Pulse doc.

Discovers the target doc by listing the reports folder on Google Drive
(newest doc wins), reads the latest draft, parses markdown into
structured content (text, hyperlinks, bullet ranges), and writes to
the doc with native Google Docs formatting.

Usage:
    python publish.py [--doc-id ID] [--dry-run]

Requires:
    GOOGLE_DOCS_CREDENTIALS env var pointing to a service account JSON key,
    OR GOOGLE_APPLICATION_CREDENTIALS for default auth.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive.readonly",
]

REPORTS_FOLDER_ID = "1Nfir4VgHzPSUGZBJHFRM0GPYj8k5VeHu"

TEAM_SECTION = "Data Processing"
NEXT_SECTION = "Notebooks"

SECONDARY_SECTIONS = {
    "Risks / Issues": {"marker": "Risks / Issues", "draft_label": "Risks/Issues"},
    "Customers": {"marker": "Customers", "draft_label": "Customers"},
    "Associates": {"marker": "Associates", "draft_label": "Associates"},
}

SECTION_ORDER = [
    "Risks / Issues",
    "Customers",
    "Associates",
    "Weekly Updates",
]

GWS_CREDENTIALS_DIR = Path.home() / ".google_workspace_mcp" / "credentials"


# --- Credentials ---

def get_credentials():
    """Build credentials from available sources.

    Priority:
    1. GOOGLE_DOCS_CREDENTIALS env var (explicit path)
    2. GOOGLE_APPLICATION_CREDENTIALS env var
    3. GWS MCP credential store (~/.google_workspace_mcp/credentials/)
    4. gcloud application-default credentials
    """
    creds_path = os.getenv("GOOGLE_DOCS_CREDENTIALS")
    if not creds_path:
        creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    if creds_path:
        return _load_credentials_file(creds_path)

    gws_creds = _try_gws_credentials()
    if gws_creds:
        return gws_creds

    import google.auth
    creds, _ = google.auth.default(scopes=SCOPES)
    return creds


def _load_credentials_file(creds_path: str):
    with open(creds_path) as f:
        info = json.load(f)

    if info.get("type") == "service_account":
        return service_account.Credentials.from_service_account_file(
            creds_path, scopes=SCOPES
        )

    from google.oauth2.credentials import Credentials as UserCredentials
    return UserCredentials(
        token=info.get("token") or info.get("access_token"),
        refresh_token=info.get("refresh_token"),
        token_uri=info.get("token_uri", "https://oauth2.googleapis.com/token"),
        client_id=info.get("client_id"),
        client_secret=info.get("client_secret"),
        scopes=info.get("scopes") or SCOPES,
        quota_project_id=info.get("quota_project_id"),
    )


def _try_gws_credentials():
    if not GWS_CREDENTIALS_DIR.exists():
        return None

    cred_files = sorted(
        GWS_CREDENTIALS_DIR.glob("*.json"),
        key=lambda p: (0 if "redhat.com" in p.name else 1, p.name),
    )
    if not cred_files:
        return None

    chosen = cred_files[0]
    print(f"Using GWS credentials: {chosen.name}")
    return _load_credentials_file(str(chosen))


# --- Doc discovery ---

def find_latest_report_doc(creds, folder_id: str = REPORTS_FOLDER_ID) -> tuple[str, str]:
    drive = build("drive", "v3", credentials=creds)

    results = drive.files().list(
        q=f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.document' and trashed=false",
        orderBy="createdTime desc",
        pageSize=1,
        fields="files(id, name, createdTime)",
        supportsAllDrives=True,
        includeItemsFromAllDrives=True,
    ).execute()

    files = results.get("files", [])
    if not files:
        print(f"Error: no documents found in folder {folder_id}")
        sys.exit(1)

    doc = files[0]
    print(f"Found report: \"{doc['name']}\" (created {doc['createdTime']})")
    return doc["id"], doc["name"]


def resolve_doc_id(cli_override: str | None, creds) -> tuple[str, str | None]:
    doc_id = cli_override or os.getenv("REPORT_DOC_ID")
    if doc_id:
        return doc_id, None
    return find_latest_report_doc(creds)


# --- Markdown to structured content ---

def _utf16_len(s: str) -> int:
    """Return the number of UTF-16 code units in a string.

    Google Docs API uses UTF-16 based indexing. Characters outside the
    Basic Multilingual Plane (like emoji) take 2 code units instead of 1.
    """
    return len(s.encode("utf-16-le")) // 2


def parse_markdown_to_doc_content(markdown: str) -> dict:
    """Parse markdown text into structured content for Google Docs.

    Converts markdown bullets and links into a format that maps to
    native Google Docs formatting (bullet lists, hyperlinks). Uses
    UTF-16 offsets for Google Docs API compatibility.

    Returns:
        {
            "text": "plain text with links resolved to display text\\n",
            "links": [(start_offset, end_offset, url), ...],
            "bullet_range": (start_offset, end_offset) or None,
        }
    """
    lines = markdown.split("\n")
    text = "\n\n"
    utf16_pos = 2
    links = []
    bullet_start = None
    bullet_end = None

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("**"):
            continue
        if stripped == "Highlights:":
            continue

        is_bullet = stripped.startswith("- ")
        if is_bullet:
            stripped = stripped[2:]
            if bullet_start is None:
                bullet_start = utf16_pos

        processed = ""
        for part in re.split(r"(\[[^\]]+\]\([^)]+\))", stripped):
            link_match = re.match(r"\[([^\]]+)\]\(([^)]+)\)", part)
            if link_match:
                display = link_match.group(1)
                url = link_match.group(2)
                start = utf16_pos + _utf16_len(processed)
                processed += display
                end = utf16_pos + _utf16_len(processed)
                links.append((start, end, url))
            else:
                processed += part

        text += processed + "\n"
        utf16_pos += _utf16_len(processed) + 1
        if is_bullet:
            bullet_end = utf16_pos

    bullet_range = (bullet_start, bullet_end) if bullet_start is not None else None
    return {"text": text, "links": links, "bullet_range": bullet_range}


# --- Draft extraction ---

def extract_raw_sections_from_draft(draft_path: Path) -> dict[str, str]:
    """Parse the draft into a dict of raw markdown content per section.

    Returns raw markdown (with [links](urls) and - bullets intact).
    """
    content = draft_path.read_text()
    result = {}

    dp_match = re.search(
        r"## Suggested Section.*?\n\n(.*?)(?=\n---\n|\n## Suggested Addition)",
        content,
        re.DOTALL,
    )
    if not dp_match:
        dp_match = re.search(
            r"## Suggested Section.*?\n\n(.*?)(?=\n## |\Z)",
            content,
            re.DOTALL,
        )
    if not dp_match:
        print(f"Error: could not find 'Suggested Section' in {draft_path}")
        sys.exit(1)

    result["data_processing"] = dp_match.group(1).strip()

    for label_key, cfg in SECONDARY_SECTIONS.items():
        draft_label = cfg["draft_label"]
        pattern = rf"## Suggested Addition to {re.escape(draft_label)} Section\s*\n(.*?)(?=\n## |\n---\n|\Z)"
        match = re.search(pattern, content, re.DOTALL)
        if match:
            raw = match.group(1).strip()
            if raw:
                key = label_key.lower().replace(" ", "").replace("/", "_")
                if key == "associates":
                    raw = _add_associates_flair(raw)
                result[key] = raw

    return result


def _pick_associates_emoji(bullets: list[str]) -> list[str]:
    """Use the LLM to choose a single emoji for each Associates bullet
    based on its sentiment."""
    try:
        from anthropic import AnthropicVertex
    except ImportError:
        return ["🎉"] * len(bullets)

    project = os.getenv("ANTHROPIC_VERTEX_PROJECT_ID", "itpc-gcp-ai-eng-claude")
    region = os.getenv("ANTHROPIC_VERTEX_REGION", "us-east5")

    try:
        client = AnthropicVertex(project_id=project, region=region)
    except Exception:
        return ["🎉"] * len(bullets)

    numbered = "\n".join(f"{i+1}. {b}" for i, b in enumerate(bullets))
    prompt = (
        "For each numbered item below, reply with ONLY a single emoji that "
        "matches the sentiment. Use celebratory emoji (🎉, 🏆, ⭐, 🚀) for "
        "achievements and milestones, somber emoji (🕊️, 💐, 🙏) for loss or "
        "hardship, and neutral emoji (📢, 📌) for announcements. Reply with "
        "one emoji per line, nothing else.\n\n" + numbered
    )

    try:
        resp = client.messages.create(
            model="claude-sonnet-4-5@20250929",
            max_tokens=100,
            messages=[{"role": "user", "content": prompt}],
        )
        emojis = resp.content[0].text.strip().split("\n")
        result = [e.strip() for e in emojis]
        while len(result) < len(bullets):
            result.append("🎉")
        return result[:len(bullets)]
    except Exception:
        return ["🎉"] * len(bullets)


def _add_associates_flair(raw: str) -> str:
    """Add sentiment-appropriate emoji to Associates bullets via LLM."""
    lines = raw.split("\n")
    bullet_texts = []
    bullet_indices = []

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("- "):
            bullet_texts.append(stripped[2:])
            bullet_indices.append(i)

    if not bullet_texts:
        return raw

    emojis = _pick_associates_emoji(bullet_texts)

    result = list(lines)
    for idx, emoji, text in zip(bullet_indices, emojis, bullet_texts):
        result[idx] = f"- {emoji} {text}"

    return "\n".join(result)


def find_latest_draft() -> Path | None:
    output_dir = Path(__file__).parent / "output"
    today = datetime.now().strftime("%Y-%m-%d")

    today_draft = output_dir / today / "draft.md"
    if today_draft.exists():
        return today_draft

    flat_draft = output_dir / f"draft_{today}.md"
    if flat_draft.exists():
        return flat_draft

    date_dirs = sorted(output_dir.glob("20*"), reverse=True)
    for d in date_dirs:
        draft = d / "draft.md"
        if draft.exists():
            return draft

    flat_drafts = sorted(output_dir.glob("draft_*.md"), reverse=True)
    if flat_drafts:
        return flat_drafts[0]

    return None


# --- Doc read/write ---

def read_doc_body(service, doc_id: str) -> tuple[str, dict]:
    doc = service.documents().get(documentId=doc_id).execute()
    body = doc.get("body", {})
    text_parts = []
    for element in body.get("content", []):
        if "paragraph" in element:
            for elem in element["paragraph"].get("elements", []):
                text_parts.append(elem.get("textRun", {}).get("content", ""))
        elif "table" in element:
            for row in element["table"].get("tableRows", []):
                for cell in row.get("tableCells", []):
                    for cell_content in cell.get("content", []):
                        if "paragraph" in cell_content:
                            for elem in cell_content["paragraph"].get("elements", []):
                                text_parts.append(elem.get("textRun", {}).get("content", ""))

    return "".join(text_parts), doc


def find_section_indices(full_text: str, section_name: str, next_section: str,
                         search_after: str = "Weekly Updates"):
    """Find the character range of a team section's content in the doc.

    Searches the raw document text (not headings) for section_name after
    the "Weekly Updates" anchor, returning the start/end offsets of the
    content between section_name and next_section.
    """
    anchor_pos = full_text.find(search_after)
    if anchor_pos == -1:
        return None, None

    section_pos = full_text.find(section_name, anchor_pos)
    if section_pos == -1:
        return None, None

    content_start = section_pos + len(section_name) + 1

    next_pos = full_text.find(next_section, content_start)
    if next_pos == -1:
        return None, None

    return content_start, next_pos


def find_append_point(full_text: str, section_name: str) -> int | None:
    """Find the insertion index for appending content to a shared section.

    Locates section_name in the raw doc text and returns the character
    offset just before the next section heading (or end of content),
    so new bullets can be inserted without overwriting existing content.
    """
    pos = full_text.find(section_name)
    if pos == -1:
        return None

    after_header = pos + len(section_name)
    next_newline = full_text.find("\n", after_header)
    if next_newline == -1:
        return len(full_text)

    content_start = next_newline + 1

    next_section_pos = None
    for candidate in SECTION_ORDER:
        if candidate == section_name:
            continue
        cpos = full_text.find(candidate, content_start)
        if cpos != -1 and (next_section_pos is None or cpos < next_section_pos):
            next_section_pos = cpos

    if next_section_pos is not None:
        return next_section_pos
    return content_start


def build_section_requests(doc_index: int, parsed: dict,
                           delete_range: tuple[int, int] | None = None) -> list[dict]:
    """Build all Google Docs API requests for a section.

    Handles: delete old content (if replacing), insert text, remove
    bold, apply bullet list formatting, and apply hyperlinks.
    """
    text = parsed["text"]
    requests = []

    if delete_range:
        start, end = delete_range
        if start < end:
            requests.append({
                "deleteContentRange": {
                    "range": {"startIndex": start, "endIndex": end}
                }
            })

    requests.append({
        "insertText": {
            "location": {"index": doc_index},
            "text": text,
        }
    })

    text_end = doc_index + _utf16_len(text)

    requests.append({
        "updateTextStyle": {
            "range": {"startIndex": doc_index, "endIndex": text_end},
            "textStyle": {"bold": False},
            "fields": "bold",
        }
    })

    if parsed["bullet_range"]:
        bs, be = parsed["bullet_range"]
        requests.append({
            "createParagraphBullets": {
                "range": {
                    "startIndex": doc_index + bs,
                    "endIndex": doc_index + be,
                },
                "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE",
            }
        })

    for start, end, url in parsed["links"]:
        requests.append({
            "updateTextStyle": {
                "range": {
                    "startIndex": doc_index + start,
                    "endIndex": doc_index + end,
                },
                "textStyle": {"link": {"url": url}},
                "fields": "link",
            }
        })

    return requests


def publish(creds, doc_id: str, raw_sections: dict[str, str],
            dry_run: bool = False):
    """Publish all sections to the Google Doc with native formatting."""
    service = build("docs", "v1", credentials=creds)

    print(f"Reading document {doc_id}...")
    full_text, doc = read_doc_body(service, doc_id)

    all_requests = []
    write_plan = []

    # --- Primary: Data Processing (replace) ---
    dp_raw = raw_sections.get("data_processing", "")
    if dp_raw:
        content_start, content_end = find_section_indices(
            full_text, TEAM_SECTION, NEXT_SECTION
        )
        if content_start is None:
            print(f"Error: could not find '{TEAM_SECTION}' section in the document")
            sys.exit(1)

        parsed = parse_markdown_to_doc_content(dp_raw)
        existing = full_text[content_start:content_end]
        print(f"\nFound '{TEAM_SECTION}' section (chars {content_start}-{content_end})")
        print(f"  Existing: {len(existing)} chars")
        print(f"  New: {len(parsed['text'])} chars, {len(parsed['links'])} links")
        if parsed["bullet_range"]:
            print(f"  Bullets: chars {parsed['bullet_range'][0]}-{parsed['bullet_range'][1]}")

        doc_index = content_start + 1
        delete_range = (doc_index, content_end + 1) if doc_index < content_end + 1 else None
        write_plan.append(("Data Processing", "replace", content_start))
        all_requests.extend(
            build_section_requests(doc_index, parsed, delete_range=delete_range)
        )

    # --- Secondary sections (append) ---
    secondary_items = []
    section_map = {
        "risks_issues": "Risks / Issues",
        "customers": "Customers",
        "associates": "Associates",
    }
    for key, doc_section_name in section_map.items():
        raw = raw_sections.get(key, "")
        if not raw:
            continue

        insert_point = find_append_point(full_text, doc_section_name)
        if insert_point is None:
            print(f"  Warning: '{doc_section_name}' section not found in doc, skipping")
            continue

        parsed = parse_markdown_to_doc_content(raw)
        secondary_items.append((doc_section_name, parsed, insert_point))

    secondary_items.sort(key=lambda x: x[2], reverse=True)

    for doc_section_name, parsed, insert_point in secondary_items:
        print(f"\nFound '{doc_section_name}' section, will append")
        print(f"  {len(parsed['text'])} chars, {len(parsed['links'])} links")
        write_plan.append((doc_section_name, "append", insert_point))
        doc_index = insert_point + 1
        all_requests.extend(
            build_section_requests(doc_index, parsed)
        )

    if not all_requests:
        print("\nNo content to publish.")
        return True

    print(f"\nWrite plan: {len(write_plan)} section(s)")
    for name, action, pos in write_plan:
        print(f"  {action.upper()} {name} at char {pos}")

    if dry_run:
        print("\n[DRY RUN] Would execute the above. No changes made.")
        return True

    print("\nPublishing to Google Docs...")
    result = service.documents().batchUpdate(
        documentId=doc_id, body={"requests": all_requests}
    ).execute()

    print(f"Success! {len(result.get('replies', []))} operations completed.")
    print(f"Doc: https://docs.google.com/document/d/{doc_id}/edit")
    return True


# --- Main ---

def main():
    parser = argparse.ArgumentParser(description="Publish DP section to Google Docs")
    parser.add_argument("--doc-id", default=None,
                        help="Google Doc ID (auto-discovers from Drive folder if omitted)")
    parser.add_argument("--draft", type=str,
                        help="Path to draft file (auto-detected if omitted)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be published without writing")
    args = parser.parse_args()

    if args.draft:
        draft_path = Path(args.draft)
    else:
        draft_path = find_latest_draft()

    if not draft_path or not draft_path.exists():
        print("Error: no draft found. Run generate.py first.")
        sys.exit(1)

    creds = get_credentials()
    doc_id, doc_title = resolve_doc_id(args.doc_id, creds)
    print(f"Draft: {draft_path}")
    print(f"Target doc: {doc_id}" + (f" ({doc_title})" if doc_title else ""))

    raw_sections = extract_raw_sections_from_draft(draft_path)
    section_names = list(raw_sections.keys())
    print(f"Sections found in draft: {', '.join(section_names)}")

    for name, raw in raw_sections.items():
        parsed = parse_markdown_to_doc_content(raw)
        print(f"\n{'─' * 40}")
        print(f"[{name}] {len(parsed['links'])} links, "
              f"bullets: {'yes' if parsed['bullet_range'] else 'no'}")
        print(parsed["text"][:200].rstrip() + ("..." if len(parsed["text"]) > 200 else ""))
    print(f"{'─' * 40}\n")

    try:
        publish(creds, doc_id, raw_sections, dry_run=args.dry_run)
    except Exception as e:
        error_msg = str(e)
        print(f"\n{'!' * 60}")
        print(f"PUBLISH FAILED: {error_msg}")
        print(f"{'!' * 60}")
        print(f"\nDoc: https://docs.google.com/document/d/{doc_id}/edit")

        output_dir = Path(__file__).parent / "output"
        failure_path = output_dir / "publish_failure.json"
        failure_path.write_text(json.dumps({
            "status": "failed",
            "error": error_msg,
            "doc_url": f"https://docs.google.com/document/d/{doc_id}/edit",
            "timestamp": datetime.now().isoformat(),
        }, indent=2))
        print(f"Failure details saved to: {failure_path}")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
