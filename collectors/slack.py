"""
Sweep Slack messages for each team member over the past week.
Uses Slack search.messages API with a user token to find messages
from each person across all accessible channels.
"""

from datetime import datetime, timedelta
from typing import List, Optional
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SlackCollector:

    def __init__(self, token: str, members: List[dict]):
        self.client = WebClient(token=token)
        self.members = members

    def _resolve_user_ids(self) -> dict:
        """Map email addresses to Slack user IDs if not already set."""
        resolved = {}
        for member in self.members:
            if member.get("slack_id"):
                resolved[member["name"]] = member["slack_id"]
                continue
            try:
                resp = self.client.users_lookupByEmail(email=member["email"])
                uid = resp["user"]["id"]
                resolved[member["name"]] = uid
                print(f"  Resolved {member['name']} -> {uid}")
            except SlackApiError as e:
                print(f"  Could not resolve {member['email']}: {e.response['error']}")
        return resolved

    def search_user_messages(self, user_id: str, after_date: str,
                             before_date: str) -> List[dict]:
        """Search for messages from a specific user in a date range."""
        query = f"from:<@{user_id}> after:{after_date} before:{before_date}"
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
            uid = user_ids.get(name)
            if not uid:
                results[name] = {"messages": [], "count": 0}
                continue

            messages = self.search_user_messages(uid, after, before)
            results[name] = {
                "messages": messages,
                "count": len(messages),
            }
            print(f"  {name}: {len(messages)} messages")

        return results
