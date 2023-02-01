# -*- coding: utf-8 -*-

from contextlib import AbstractContextManager
from typing import Callable, Iterator, Mapping

from sqlalchemy.orm import Session

from utils import repo
from models.state import State
from db.exceptions import StateNotFoundError


class StateRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def add(self, state: State) -> State:
        with self.session_factory() as session:
            session.add(state)
            session.commit()
            session.refresh(state)
            return state

    def get_latest_by_uid(self, uid: str) -> State:
        with self.session_factory() as session:
            state = session.query(State).order_by(State.tmst_created.desc()).filter(State.uid == uid).first()
            if not state:
                raise StateNotFoundError(uid)
            return state

    def list(self, spec: Mapping = None) -> Iterator[State]:
        with self.session_factory() as session:
            objs = session.query(State).all()

        return repo.filtration(spec, objs)

    def update(self, state: State) -> None:
        with self.session_factory() as session:
            session.query(State).filter_by(id=state.id).update(dict(
                uid=state.uid,
                username=state.username,
                r_bfr=state.r_bfr,
                r_afr=state.r_afr
            ))

            session.commit()
