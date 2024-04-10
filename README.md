# HCDS G1 Project

## Installation and Running

Install Python and [Pipenv](https://pipenv.pypa.io/en/latest/installation.html)

Update your .env file in the following way

```
REDDIT_CLIENT_ID=client_id_value
REDDIT_CLIENT_SECRET=secret_value
REDDIT_PASSWORD=my_reddit_password
REDDIT_USER_AGENT=testscript by u/fakebot1
REDDIT_USERNAME=my_reddit_username
```

run `pipenv install` to install the virtual env and dependencies

run `pipenv run python scrape_reddit.py` to scape submissions and comments
