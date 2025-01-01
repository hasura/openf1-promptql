# OpenF1 PromptQL

This is a PromptQL (https://promptql.hasura.io) project on OpenF1 data, which gives you an AI assistant to interact with F1 data.

## Ingesting data in Mongo

### Pre-requisites

You need to have Poetry installed: https://python-poetry.org/docs/#installing-with-the-official-installer

### Ingesting 2024 F1 data

```bash
cd openf1
poetry install
MONGO_URI=<mongo db url> poetry run python season.py 2024
```

Note this script may error out if some of the data coming from the API is inconsistnet or the API just errors out. If it's a retriable API error, just run the script again (it can recover from a partial sync). If the data itself is corrupt, then you'll have to manually mark it as "synced" in the database to skip it.

## DDN project

The DDN project is located in `ddn_project` which can be used with PromptQL.
