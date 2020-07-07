import os
from notion.client import NotionClient
from notion.client import RecordStore
from notion.records import Record
from notion.block import CollectionViewPageBlock
from notion.block import TextBlock
from notion.collection import CollectionRowBlock
from notion.collection import NotionDate
from imdb import IMDb
from imdb import helpers
import time
from datetime import datetime, timedelta

IMDB_TO_NOTION_TYPE = {
    "tv series": "series",
    "movie": "movie"
}

# Obtain the `token_v2` value by inspecting your browser cookies on a logged-in session on Notion.so
notion_client = NotionClient(token_v2=os.environ["NOTION_TOKEN"], monitor=True,start_monitoring=True)

imdb_client = IMDb()


# Setup connection to the Notion movie watchlist databse 
movie_database: CollectionViewPageBlock = notion_client.get_block("https://www.notion.so/09f8cae7e34149c28a7662ae07f4f599?v=ee890a52135c4f079cc8d0b1e1202e1f")
movie_list = movie_database.collection.get_rows()


def fetch_imdb_movie(title: str) -> dict:
    """
    Returns a dict containing the relevant movie information that
    we want to put into the Notion database entry
    """

    print(f'Searching for the imdb object "{title}"')
    searched_movie_list = imdb_client.search_movie(title)
    movie_id = searched_movie_list[0].movieID # Use the first movie/series
    movie = imdb_client.get_movie(movie_id)

    movie_data = {
        "type": IMDB_TO_NOTION_TYPE.get(movie["kind"]),
        "movie_id": movie_id,
        "title": movie.get("title"),
        "plot": movie.get("plot"),
        "rating": movie.get("rating"),
        "genres": movie.get("genres")
    }

    print(movie.get("plot"))
    print("next")
    print(movie["plot"][0].split("::")[0])
    return movie_data

def look_for_new_entry(movie_list):
    for movie in movie_list:
        if not movie.imdb:
            return movie

def new_entry_callback():
    # The list of movies
    movie_list = movie_database.collection.get_rows()
    movie: CollectionRowBlock = look_for_new_entry(movie_list)

    if movie:
        print("Found new movie", movie)
        
        # Check if the movie was just recently added to the list
        created_time: datetime = movie.created
        cooldown: datetime = timedelta(minutes=1)

        if created_time + cooldown > datetime.utcnow():
            print("Not yet considered done")
            # Not yet considered "done edited"
            return

        # fetch movie data from IMDB via the fetch function
        movie_data = fetch_imdb_movie(movie.name)
        # get movie title from notion entry

        # THE MOVIE'S ID NUMBER "https://www.imdb.com/title/tt" + idNum

        
        movie.imdb = "https://www.imdb.com/title/tt" + movie_data.get("movie_id")
        movie.name = movie_data.get("title")
        movie.type = movie_data.get("type")
        movie.rating = movie_data.get("rating")
        movie.genre = movie_data.get("genres")
        movie.children.add_new(TextBlock, title=movie_data.get("plot"))
       

        # take data and populate notion page

        # if necessary, push changes to notion / update notion page with changes

def poll_updates():
    while True:
        print("Refreshing")
        movie_database.collection.refresh()
        print("Refreshd")
        new_entry_callback()
        print("Callback done")
        time.sleep(2)


movie_database.collection.add_callback(new_entry_callback)
poll_updates()

# Its from this point the application runs

# TODO Listen for changes on the database, when a new entry is added. Call new_entry_callback()
# and pass the new entry page to the function
