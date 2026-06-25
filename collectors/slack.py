"""
Sweep Slack messages for each team member over the past week.
Uses Slack search.messages API to find messages from each person
across all accessible channels.

Supports two auth modes:
  - xoxp token: standard user API token (requires Slack App + admin approval)
  - xoxc + xoxd: browser session tokens (no admin approval needed,
    extract with slack-token-extractor or similar)
"""

from datetime import datetime, timedelta
from typing import List, Optional
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SlackCollector:

    def __init__(self, token: str, members: List[dict], cookie: str = None):
        headers = {}
        if cookie:
            headers["cookie"] = f"d={cookie}"
        self.client = WebClient(token=token, headers=headers)
        self.members = members

    def _resolve_user_ids(self) -> dict:
        """Map email addresses to Slack user IDs.

        Uses slack_id from config when available. For members without
        a pre-set ID, attempts users.lookupByEmail (works with xoxp
        tokens, fails with xoxc). Members without an ID will fall back
        to username-based search in collect().
        """
        resolved = {}
        needs_lookup = []
        for member in self.members:
            if member.get("slack_id"):
                resolved[member["name"]] = member["slack_id"]
            else:
                needs_lookup.append(member)

        for member in needs_lookup:
            try:
                resp = self.client.users_lookupByEmail(email=member["email"])
                uid = resp["user"]["id"]
                resolved[member["name"]] = uid
                print(f"  Resolved {member['name']} -> {uid}")
            except SlackApiError as e:
                error = e.response['error']
                if error == "not_allowed_token_type":
                    print(f"  Skipping API lookup for {member['name']} (xoxc token)")
                else:
                    print(f"  Could not resolve {member['email']}: {error}")
        return resolved

    def _search_messages(self, query: str) -> List[dict]:
        """Run a search_messages query and return parsed results."""
        messages = []
        try:
            resp = self.client.search_messages(
                query=query, sort="timestamp", sort_dir="desc", count=50
            )
            for match in resp.get("messages", {}).get("matches", []):
                messages.append({
                    "text": match.get("text", ""),
                    "channel": match.get("channel", {}).get("name", ""),
                    "timestamp": match.get("ts", ""),
                    "permalink": match.get("permalink", ""),
                })
        except SlackApiError as e:
            print(f"  Slack search error: {e.response['error']}")
        return messages

    def collect(self, days_back: int = 7) -> dict:
        """Main entry point: sweep messages for all team members."""
        after = (datetime.utcnow() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        before = datetime.utcnow().strftime("%Y-%m-%d")
        print(f"Sweeping Slack messages from {after} to {before}...")

        user_ids = self._resolve_user_ids()
        results = {}

        for member in self.members:
            name = member["name"]
            email = member["email"]
            uid = user_ids.get(name)

            if uid:
                query = f"from:<@{uid}> after:{after} before:{before}"
            else:
                username = email.split("@")[0]
                query = f"from:{username} after:{after} before:{before}"

            messages = self._search_messages(query)
            results[name] = {
                "messages": messages,
                "count": len(messages),
            }
            print(f"  {name}: {len(messages)} messages")

        return results
