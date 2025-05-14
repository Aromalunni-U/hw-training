import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M"
)

BASE_URL = "https://www.harrynorman.com/roster/Agents"

JSON_PATH = "2025-05-14/harrynorman.json"