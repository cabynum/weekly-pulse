#!/usr/bin/env python3
"""
Google Docs Publisher - writes the Data Processing section to the live
AAET Weekly Pulse doc.

Reads the latest draft, strips markdown formatting, identifies the
target section in the Google Doc, and replaces it.

Usage:
    python publish.py [--doc-id ID] [--dry-run]

Requires:
    GOOGLE_DOCS_CREDENTIALS env var pointing to a service account JSON key,
    OR GOOGLE_APPLICATION_CREDENTIALS for default auth.
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/documents"]

DEFAULT_DOC_ID = "1jMyzuYlkKyl_CULDhyb2CaWGUrAkk4DI6rW0diI0J38"

TEAM_SECTION = "Data Processing"
NEXT_SECTION = "RAG / Agent Ops"


def get_credentials():
    """Build credentials from service account JSON or user OAuth credentials."""
    import json

    creds_path = os.getenv("GOOGLE_DOCS_CREDENTIALS")
    if not creds_path:
        creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    if creds_path:
        with open(creds_path) as f:
            info = json.load(f)

        if info.get("type") == "service_account":
            return service_account.Credentials.from_service_account_file(
                creds_path, scopes=SCOPES
            )

        # User credentials (from gcloud auth application-default login)
        from google.oauth2.credentials import Credentials as UserCredentials
        quota_project = info.get("quota_project_id", "itpc-gcp-ai-eng-claude")
        return UserCredentials(
            token=info.get("access_token"),
            refresh_token=info.get("refresh_token"),
            token_uri=info.get("token_uri", "https://oauth2.googleapis.com/token"),
            client_id=info.get("client_id"),
            client_secret=info.get("client_secret"),
            scopes=SCOPES,
            quota_project_id=quota_project,
        )

    # Try default credentials discovery
    import google.auth
    creds, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/documents",
                                           "https://www.googleapis.com/auth/drive.readonly"])
    return creds


def strip_markdown_links(text: str) -> str:
    """Convert [text](url) to just text."""
    return re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)


def extract_section_from_draft(draft_path: Path) -> str:
    """Extract the 'Suggested Section' content from the draft markdown."""
    content = draft_path.read_text()

    # Try with --- separator first (CI-generated format)
    match = re.search(
        r"## Suggested Section.*?\n\n(.*?)(?=\n---\n)",
        content,
        re.DOTALL,
    )
    if not match:
        # Fallback: capture until next ## heading or end of file
        match = re.search(
            r"## Suggested Section.*?\n\n(.*?)(?=\n## |\Z)",
            content,
            re.DOTALL,
        )
    if not match:
        print(f"Error: could not find 'Suggested Section' in {draft_path}")
        sys.exit(1)

    section = match.group(1).strip()
    return strip_markdown_links(section)


def format_for_doc(section_text: str) -> str:
    """Convert the section into plain text suitable for Google Docs.

    Input format (from synthesizer):
        **Data Processing** (Chris Bynum) - 12 issues completed

        Highlights:

        - Completed RHOAIENG-67538: Remove .tekton CI pipeline files...
        - Merged 6 PRs across tracked repositories

        In progress: 40 active issues.

        Feature watch: ...

    Output format (for Google Doc bullet list):
        Completed RHOAIENG-67538: Remove .tekton CI pipeline files...
        Merged 6 PRs across tracked repositories
        In progress: 40 active issues.
        Feature watch: ...
    """
    lines = section_text.split("\n")
    output_lines = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("**"):
            continue
        if stripped == "Highlights:":
            continue
        if stripped.startswith("- "):
            output_lines.append(stripped[2:])
        else:
            output_lines.append(stripped)

    return "\n".join(output_lines)


def read_doc_body(service, doc_id: str) -> str:
    """Read the full document body as plain text, return (text, doc)."""
    doc = service.documents().get(documentId=doc_id).execute()
    body = doc.get("body", {})
    text_parts = []
    for element in body.get("content", []):
        if "paragraph" in element:
            for elem in element["paragraph"].get("elements", []):
                text_content = elem.get("textRun", {}).get("content", "")
                text_parts.append(text_content)
        elif "table" in element:
            for row in element["table"].get("tableRows", []):
                for cell in row.get("tableCells", []):
                    for content in cell.get("content", []):
                        if "paragraph" in content:
                            for elem in content["paragraph"].get("elements", []):
                                text_content = elem.get("textRun", {}).get("content", "")
                                text_parts.append(text_content)

    return "".join(text_parts), doc


def find_section_indices(full_text: str, section_name: str, next_section: str):
    """Find the start and end character indices of our section.

    Returns (content_start, content_end) where:
    - content_start is the index AFTER "Data Processing\\n"
    - content_end is the index of the start of the next section name

    We target the FIRST occurrence that appears in a "Weekly Updates"
    context (the current week's template).
    """
    weekly_updates_pos = full_text.find("Weekly Updates")
    if weekly_updates_pos == -1:
        return None, None

    search_start = weekly_updates_pos
    section_pos = full_text.find(section_name, search_start)
    if section_pos == -1:
        return None, None

    content_start = section_pos + len(section_name) + 1  # +1 for newline

    next_pos = full_text.find(next_section, content_start)
    if next_pos == -1:
        return None, None

    content_end = next_pos

    return content_start, content_end


def publish(doc_id: str, content: str, dry_run: bool = False):
    """Publish content to the Google Doc."""
    creds = get_credentials()
    service = build("docs", "v1", credentials=creds)

    print(f"Reading document {doc_id}...")
    full_text, doc = read_doc_body(service, doc_id)

    content_start, content_end = find_section_indices(
        full_text, TEAM_SECTION, NEXT_SECTION
    )
    if content_start is None:
        print(f"Error: could not find '{TEAM_SECTION}' section in the document")
        sys.exit(1)

    existing_content = full_text[content_start:content_end]
    print(f"\nFound '{TEAM_SECTION}' section (chars {content_start}-{content_end})")
    print(f"Existing content ({len(existing_content)} chars):")
    preview = existing_content[:100].replace("\n", "\\n")
    print(f"  '{preview}...'")

    new_content = content + "\n"
    print(f"\nNew content ({len(new_content)} chars):")
    preview = new_content[:100].replace("\n", "\\n")
    print(f"  '{preview}...'")

    if dry_run:
        print("\n[DRY RUN] Would replace section. No changes made.")
        return True

    # Google Docs API uses 1-based indexing for the body
    # The full_text we extracted starts at index 1 in the doc
    # So character position P in full_text = doc index P + 1
    start_index = content_start + 1
    end_index = content_end + 1

    requests = [
        {
            "deleteContentRange": {
                "range": {
                    "startIndex": start_index,
                    "endIndex": end_index,
                }
            }
        },
        {
            "insertText": {
                "location": {"index": start_index},
                "text": new_content,
            }
        },
    ]

    print("\nPublishing to Google Docs...")
    result = service.documents().batchUpdate(
        documentId=doc_id, body={"requests": requests}
    ).execute()

    print(f"Success! {len(result.get('replies', []))} operations completed.")
    print(f"Doc: https://docs.google.com/document/d/{doc_id}/edit")
    return True


def find_latest_draft() -> Path:
    """Find the most recent draft file."""
    output_dir = Path(__file__).parent / "output"
    today = datetime.now().strftime("%Y-%m-%d")

    # Check today's date folder first
    today_draft = output_dir / today / "draft.md"
    if today_draft.exists():
        return today_draft

    # Check flat naming (draft_YYYY-MM-DD.md)
    flat_draft = output_dir / f"draft_{today}.md"
    if flat_draft.exists():
        return flat_draft

    # Find the most recent draft in any date folder
    date_dirs = sorted(output_dir.glob("20*"), reverse=True)
    for d in date_dirs:
        draft = d / "draft.md"
        if draft.exists():
            return draft

    # Check flat files
    flat_drafts = sorted(output_dir.glob("draft_*.md"), reverse=True)
    if flat_drafts:
        return flat_drafts[0]

    return None


def main():
    parser = argparse.ArgumentParser(description="Publish DP section to Google Docs")
    parser.add_argument("--doc-id", default=DEFAULT_DOC_ID, help="Google Doc ID")
    parser.add_argument("--draft", type=str, help="Path to draft file (auto-detected if omitted)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be published without writing")
    args = parser.parse_args()

    if args.draft:
        draft_path = Path(args.draft)
    else:
        draft_path = find_latest_draft()

    if not draft_path or not draft_path.exists():
        print("Error: no draft found. Run generate.py first.")
        sys.exit(1)

    print(f"Draft: {draft_path}")

    section_text = extract_section_from_draft(draft_path)
    content = format_for_doc(section_text)

    print(f"\nFormatted for Google Docs:\n{'─' * 40}")
    print(content)
    print(f"{'─' * 40}\n")

    try:
        publish(args.doc_id, content, dry_run=args.dry_run)
    except Exception as e:
        error_msg = str(e)
        print(f"\n{'!' * 60}")
        print(f"PUBLISH FAILED: {error_msg}")
        print(f"{'!' * 60}")
        print("\nThe draft was generated successfully but could not be")
        print("published to the Google Doc automatically.")
        print(f"\nDoc: https://docs.google.com/document/d/{args.doc_id}/edit")
        print("\nPlain-text content to paste manually:")
        print(f"{'─' * 40}")
        print(f"Data Processing\n{content}")
        print(f"{'─' * 40}")

        # Write failure notice for Dashboard notification
        output_dir = Path(__file__).parent / "output"
        failure_path = output_dir / "publish_failure.json"
        import json
        failure_path.write_text(json.dumps({
            "status": "failed",
            "error": error_msg,
            "doc_url": f"https://docs.google.com/document/d/{args.doc_id}/edit",
            "manual_content": f"Data Processing\n{content}",
            "timestamp": datetime.now().isoformat(),
        }, indent=2))
        print(f"\nFailure details saved to: {failure_path}")

        # Exit 0 so CI doesn't fail the whole workflow
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
