# IMDB Movie lookup for Notion database entries
Automatically adds a movie's rating, genre, type, imdb-link, plot, and an emoji to an entry in a Notion database based on the Title.


<!-- TABLE OF CONTENTS -->
## Table of Contents
* [About the Project](#about-the-project)
* [Notion prerequisites](#notion-prerequisites)
  * [The Notion token](#the-notion-token)
  * [The database url](#the-database-url)
  * [The database properties](#the-database-properties)
* [Getting started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Getting started using Docker](#getting-started-using-docker)
  * [Prerequisites](#prerequisites-1)
  * [Installation](#installation-1)
  * [Run application](#run-application)
* [Development setup](#development-setup)
* [Contributing](#contributing)
* [License](#license)
* [Acknowledgements](#acknowledgements)


<!-- ABOUT THE PROJECT -->
## About The Project
We made this tool since we are lazy and did not want to, manually, add a lot of information about each and every movie that we added to our movie watchlist that we have in Notion. Since both of us being programmers, the solution for this lazy-problem was a nobrainer. Lets create a python-application that does this for us!

This python application is listening to changes to our movie watchlist database. When adding a new movie, application automatically fetches the information about the movie from imdb and populates the properties, adds the plot as the content, and an appripriate emoji for that particluar database entry.

![imdb-notion-in-action]


## Notion prerequisites
There is some things you have to setup in / acquire from Notion before we can get started.

### The Notion token
Open your web browser and navigate to Notion. Once the page is loaded, press `F12`. You should now see the developer console open up. Press the top navigation `Application`. In this section you should see a bunch of things to the left. One of which says `Cookies` under `Storage`, press the _Notion cookie_ and then locate the `token_v2` cookie. The following picture shows how it look like in Chrome.
![chrome-developer-tools-image]  
Copy the value of this token and add it to the `.env_example` file.


### The database url
Open your web browser and navigate to Notion. Once the page is loaded, navigate to your database page and simpyl copy the url.  
Copy the value of this token and add it to the `.env_example` file.

Rename the `.env_exampel` to just `.env`
```sh
$ mv .env_example .env
```

Note: Do not add any whitespace around the `=` sign in the `.env` file.


### The database properties
Make sure that the movie watchlist has the right properties. Add the following to the database:
* imdb (url), this will be populated by the imdb url
* Genre (multi-select), self explanatory
* Rating (number), also self explanatory
* Type (mult-select), what type it is (`movie`/`series`/`mini series`)

![movie-properties-image]


<!-- GETTING STARTED USER-->
<!-- This section explains how a user should install and use the application -->
## Getting started
To get the application to run locally, follow these simple steps.
The application is running inside a python virtual environment for simplicity reasons and amongs other things it makes dealing with package dependencies easier.

If you wanna run the application inside a docker container, jump to [Getting started using Docker](#getting-started-using-docker)


### Prerequisites
In order to run this application you have to have the following things installed on your computer.
* python3.8
* pipenv

The following command will install everything for you, if you have a system that does not support this command. A quick google will help you getting these packages installed
```sh
$ sudo apt install python3.8 python3-pip
```

Now, if you are a user that simply want to run this application and have it populate database entries in Notion with information from IMDB.

If you are a developer and would like to run and continue development on the application, continue to [Development setup](#development-setup)


### Installation 
Setup the python environment and install the necessary dependencies
```sh
pipenv install
```


<!-- This section explains how a user should install and use the application using docker -->
## Getting started using Docker
If you just want to run this program and have it working out of the box in a matter of minutes. Docker is the way to go. You still have to do the step regarding the acquiring of the Notion token and database url though. [Notion prerequisites](#notion-prerequisites)

### Prerequisites
* Docker, you can read more about how to install it [here](https://www.docker.com/get-started).

### Installation
Build the docker image
```sh
$ docker build -t imdb-notion .
```

### Run application
This will start the container and then run the application.
```sh
$ docker run imdb-notion
```

Done, go ahead and try to add a movie to your movie list and watch as the python applcation adds the relevant information to the entry.


<!-- DEVELOPMENT SETUP (Getting started developer)-->
<!-- This section explains how a user should install and use the application -->
## Development setup
In case you want to keep developing on the project you also have to install
the packages that are necessary for development.
```sh
pipenv install --dev
```


<!-- CONTRIBUTING -->
## Contributing
Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/amazing-feature`)
3. Commit your Changes (`git commit -m 'Adds amazing-feature'`)
4. Push to the Branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


<!-- LICENSE -->
## License
Distributed under the MIT License. See [LICENSE](LICENSE) for more information.


<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* This project would not have been possible without the unofficial Notion-Python client. Read more about it here: [notion-py](https://github.com/jamalex/notion-py).
* Same goes for the imdb python client, read about that one here: [IMDbPY](https://imdbpy.github.io/).
* For acquiring the emojis, we use [emoji](https://github.com/carpedm20/emoji/).


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[chrome-developer-tools-image]: /images/chrome_developer_tools.png
[imdb-notion-in-action]: /images/imdb_notion_in_action.gif
[movie-properties-image]: /images/movie_properties.png
