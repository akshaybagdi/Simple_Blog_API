# simple_blog/posts/notion_utils.py  or simple_blog/utils/notion_utils.py

from notion_client import Client
from django.conf import settings

# Initialize Notion client
notion = Client(auth=settings.NOTION_TOKEN)

def add_api_contract_to_notion(api_name, description, request_payload, response_payload):
    """
    Adds an API contract to the Notion database.
    """
    try:
        database_id = settings.NOTION_DATABASE_ID
        notion.pages.create(
            parent={"database_id": database_id},
            properties={
                "Name": {
                    "title": [{"text": {"content": api_name}}],
                },
                "Description": {
                    "rich_text": [{"text": {"content": description}}],
                },
                "Request Payload": {
                    "rich_text": [{"text": {"content": str(request_payload)}}],
                },
                "Response Payload": {
                    "rich_text": [{"text": {"content": str(response_payload)}}],
                },
            },
        )
        return {"status": "success", "message": "API contract added to Notion."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
