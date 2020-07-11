import os
import time
import logging
import re
from datetime import datetime, timedelta
from random import choice
from uuid import uuid1

from notion.client import NotionClient
from notion.client import RecordStore
from notion.records import Record
from notion.block import CollectionViewPageBlock
from notion.block import TextBlock
from notion.collection import CollectionRowBlock
from notion.collection import Collection
from imdb import IMDb
import emoji

from logger import logger

IMDB_TO_NOTION_TYPE = {
    "tv mini series" : "mini series",
    "tv series" : "series",
    "movie": "movie"
}

# Obtain the `token_v2` value by inspecting your browser cookies on a logged-in session on Notion.so
NOTION_TOKEN = os.environ["NOTION_TOKEN"]

# Global variables
notion_client: NotionClient
imdb_client: IMDb
default_emoji: str = ":movie_camera:"
words_to_remove: list = ["the", "and"]


def fetch_imdb_movie(title: str) -> dict:
    """
    Searches for the given title on IMDB and returns a dict containing the
    relevant movie information that we want to put into the Notion database
    entry
    """

    logger.info(f'Searching for the imdb object "{title}"')
    searched_movie_list = imdb_client.search_movie(title)
    movie_id = searched_movie_list[0].movieID  # Use the first movie/series
    movie = imdb_client.get_movie(movie_id)

    movie_data = {
        "type": IMDB_TO_NOTION_TYPE.get(movie["kind"]),
        "movie_id": movie_id,
        "title": movie.get("title"),
        "plot": movie.get("plot"),
        "rating": movie.get("rating"),
        "genres": movie.get("genres")
    }

    return movie_data

colors = [
    "default",
    "gray",
    "brown",
    "orange",
    "yellow",
    "green",
    "blue",
    "purple",
    "pink",
    "red",
]

def add_new_multi_select_value(prop, value, color=None):
    if color is None:
        color = choice(colors)

    collection_schema = collection.get("schema")
    prop_schema = next((val for key, val in collection_schema.items() if val["name"] == prop), None)
    
    if not prop_schema:
        raise ValueError(f'"{prop}" prop does not exist in the collection')
    
    if prop_schema["type"] != "multi_select":
        raise ValueError(f'"{prop}" is not a multi select property')
    try:
        dupe = next((o for o in prop_schema["options"] if o["value"] == value), None)
        if dupe:
            raise ValueError(f'"{value}" already exists in the schema')
    except ValueError as e:
        print(e)

    
    prop_schema["options"].append({"color": color, "id": str(uuid1()), "value": value})
    
    collection.set("schema", collection_schema)

def check_if_new_multi_select_should_be_added(genre_data):
    for genre in genre_data:
        if add_new_multi_select_value("Genre", genre):
            logger.debug("A new genre was added")


def replace_multiple(title: str, to_replace: list):
    title = title.lower()
    for word in to_replace:
        title = title.replace(word, "")
    return title

def find_emoji_for_movie(title: str):
    # regex = r"(?:^|\W)and(?:$|\W)|(?:^|\W)the(?:$|\W)|\s" # Find "and", "the" and spaces. There are no emojis for these "words"/values?
    #words_from_title = re.split(regex, title.lower())
    emoji_dict = emoji.unicode_codes.EMOJI_ALIAS_UNICODE
    words_from_title = replace_multiple(title, words_to_remove).split()

    for word in words_from_title:
        emoji_name = next((key for (key, val) in emoji_dict.items() if word in key), None)
        if emoji_name:
            break

    if not emoji_name:
        emoji_name = default_emoji
    
    return emoji_name

def handle_new_movie_block_in_collection(block_id: str):
    movie_page = notion_client.get_block(block_id)

    # Ugly hack to make sure that the user has had the time to enter
    # the whole movie name
    time.sleep(20)

    if not movie_page.title:
        # Empty title, user was probably to slow to enter the title
        # or pressed the "new" button but then changed his/her mind.
        # Nevertheless, we will not be able to fetch the imdb movie for this
        # entry.
        return

    # Fetch the movie from imdb
    imdb_movie = fetch_imdb_movie(movie_page.title)
    imdb_url = f'https://www.imdb.com/title/tt{imdb_movie.get("movie_id")}'
    movie_emoji = find_emoji_for_movie(imdb_movie.get("title"))

    # Set the properties in the Notion collection entry
    movie_page.set_property("title", imdb_movie.get("title"))
    movie_page.set_property("type", imdb_movie.get("type"))
    movie_page.set_property("imdb", imdb_url)
    movie_page.icon = emoji.emojize(movie_emoji, use_aliases=True)
    # TODO fix so that it adds a tag if it does not exist
    check_if_new_multi_select_should_be_added(imdb_movie.get("genres"))
    movie_page.set_property("genre", imdb_movie.get("genres"))
    movie_page.set_property("rating", imdb_movie.get("rating"))
    

    # Fetch the short description of the movie
    movie_plot = imdb_movie["plot"][0].split("::")[0]

    # Add movie plot to the page content in Notion
    movie_page.children.add_new(TextBlock, title=movie_plot)

def movie_collection_change_callback(record, **kwargs):
    logger.debug("Processing collection change")
    # Something happend in the list, lets see if anything was added

    # Exampel on how the "changes" list looks like
    # [('row_added', 'rows', '735303d9-0ad9-4ca4-8dfa-cd9bebb4170b')]
    collection_changes: list = kwargs.get("changes")

    for change in collection_changes:
        change_action = change[0]
        changed_block_id = change[2]

        if change_action == "row_added":
            # A new movie has been added to the list, lets fetch some data
            # from IMDB
            logger.info("New movie added to the list")
            handle_new_movie_block_in_collection(changed_block_id)

    logger.debug("Done processing collection changes")


if __name__ == "__main__":

    # Initialize connection to Notion
    notion_client = NotionClient(
        token_v2=NOTION_TOKEN,
        monitor=True,
        start_monitoring=True,
        enable_caching=False
    )

    # Initialize the IMDB client
    imdb_client = IMDb()

    # Setup connection to movie list collection
    moive_list_page: CollectionViewPageBlock = notion_client.get_block(
        "https://www.notion.so/09f8cae7e34149c28a7662ae07f4f599?v=ee890a52135c4f079cc8d0b1e1202e1f")
    movie_list_collection: Collection = moive_list_page.collection

    # TEST TO SE IF NEW GENRE CAN BE ADDED
    collection_view = notion_client.get_collection_view(
        "https://www.notion.so/09f8cae7e34149c28a7662ae07f4f599?v=ee890a52135c4f079cc8d0b1e1202e1f", force_refresh=True)
    collection: Collection = collection_view.collection

    # Subscribe to changes towards the movie list
    movie_list_collection.add_callback(movie_collection_change_callback)

    logger.debug("Setup complete")

    while True:
        # Loop forever
        pass
