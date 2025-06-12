import requests
import os
import json
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
from datetime import date

load_dotenv()

APP_ID = os.environ.get('PLANNING_CENTER_APP_ID')
SECRET = os.environ.get('PLANNING_CENTER_SECRET')

API_BASE_URL = "https://api.planningcenteronline.com"
MORNING_WORSHIP_SERVICE_TYPE_ID = 1397044

# Info from https://api.planningcenteronline.com/services/v2/service_types/1397044/team_positions?per_page=100
team_positions = {
    "Preacher": None,
    "Service Leader": None,
    "Pastoral Prayer": None,
    "Scripture Reader": None,
    "Confession of Faith": None,
    "Catechism": None,
    "Confession of Sin & Assurance of Pardon": None,
    "Lord's Supper Leader": None,
}

name_titles_json = os.getenv("NAME_TITLES_JSON", "{}")
name_titles = json.loads(name_titles_json)

def call_planning_center_api():
    print("""
.-----------------------------------------------------.
| ____  _____ ____   ____        _ _      _   _       |
||  _ \|  ___/ ___| | __ ) _   _| | | ___| |_(_)_ __  |
|| |_) | |_ | |     |  _ \| | | | | |/ _ \ __| | '_ \ |
||  _ <|  _|| |___  | |_) | |_| | | |  __/ |_| | | | ||
||_| \_\_|   \____| |____/ \__,_|_|_|\___|\__|_|_| |_||
'-----------------------------------------------------'
    \n
Fetching data from Planning Center...
          """)
    plan_id = get_latest_plan_id()
    if plan_id:
        print_plan_team_members(plan_id)
        print_plan_items(plan_id)
    else:
        print("No valid plan ID found.")
    
    print_bulletin_checklist()


def get_latest_plan_id() -> int:
    """Returns the ID of the most recently updated plan."""

    # Sorting by the latest updated plan
    url = f"{API_BASE_URL}/services/v2/service_types/{MORNING_WORSHIP_SERVICE_TYPE_ID}/plans?order=sort_date&after={date.today().strftime('%Y-%m-%d')}T10:00:00Z&filter=after"
    response = requests.get(url, auth=HTTPBasicAuth(APP_ID, SECRET))

    if response.status_code != 200:
        print(f"Failed to fetch latest plan ID: {response.status_code}")
        return None

    data = response.json().get("data", [])
    if not data:
        print("No plans found.")
        return None

    return int(data[0].get("id"))

def print_plan_team_members(plan_id: int) -> None:
    """Fetches and prints the team members for the latest worship plan."""

    url = f"{API_BASE_URL}/services/v2/service_types/{MORNING_WORSHIP_SERVICE_TYPE_ID}/plans/{plan_id}/team_members"
    response = requests.get(url, auth=HTTPBasicAuth(APP_ID, SECRET))

    if response.status_code != 200:
        print(f"Failed to fetch team members: {response.status_code}")
        return

    data = response.json().get("data", [])
    
    for member in data:
        attrs = member.get("attributes", {})
        status = attrs.get("status")
        position_name = attrs.get("team_position_name")
        name = attrs.get("name")

        if status == "C" and position_name in team_positions:
            team_positions[position_name] = name

    print("\n=== Confirmed Team Members ===")
    for position, member_name in team_positions.items():
        if member_name and member_name in name_titles.keys():
            print(f"  {position}: {member_name} ({name_titles[member_name]})")
        else:
            print(f"  {position}: {member_name if member_name else 'None'}")

def print_plan_items(plan_id: int) -> None:
    """Fetches and prints the order of service for the latest worship plan."""

    url = f"{API_BASE_URL}/services/v2/service_types/{MORNING_WORSHIP_SERVICE_TYPE_ID}/plans/{plan_id}/items"
    response = requests.get(url, auth=HTTPBasicAuth(APP_ID, SECRET))
    for plan_item in response.json()["data"]:
        attributes = plan_item["attributes"]

        # Skip irrelevant items
        if attributes["item_type"] == "header" or attributes["service_position"] == "pre":
            continue

        title = attributes.get("title", "").strip()

        if attributes["item_type"] == "song":
            print(f"\n=== SONG: {title} ===")
            continue

        description = attributes.get("description", "")
        html_details = attributes.get("html_details", "")

        print(f"\n=== {title} ===")

        # Print description if it exists
        if description:
            print("\n  Description:\n")
            print("    " + description.strip().replace("\n", "\n    "))

        # Print HTML details if present and it's a sermon
        if html_details and title.lower() == "sermon":
            soup = BeautifulSoup(html_details, "html.parser")
            plain_text = soup.get_text(separator="\n", strip=True)
            if plain_text:
                print("\n  Details:\n")
                for line in plain_text.splitlines():
                    if line.strip():
                        print("    " + line.strip())

def print_bulletin_checklist():
    """Prints the weekly bulletin checklist."""
    print("\n=== Weekly Bulletin Checklist ===\n")
    checklist = [
        "Update sermon series title",
        "Increment sermon series number",
        'Pluralize “hymns/songs” where there are multiple',
        "Remove duplicate names",
        "Update front page scripture",
        "Add upcoming events from last week's bulletin",
        "Add any new upcoming events and remove old events",
        "Update Bible study books",
        "Update sermon outline",
        "Check sermon outline points (especially the verse numbers!)",
        "Verify bulletin against Planning Center Online",
        "Verify whether call to worship is responsive",
        "Save file in shared folder as `YYYY-MM-DD`",
        "Alert Pastor for review"
    ]

    for item in checklist:
        print(f" - {item}")

if __name__ == "__main__":
    call_planning_center_api()
