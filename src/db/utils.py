# -*- coding: utf-8 -*-

from db import database
from db.repo.state import StateRepository


def get_repos(config):
    db = database.Database(config["database"]["url"])
    db.create_database()

    state_repo = StateRepository(session_factory=db.session)

    return state_repo
