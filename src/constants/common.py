# -*- coding: utf-8 -*-

from pydantic.dataclasses import dataclass


@dataclass
class DBTables:
    state: str = 'state'


int2emoji = {
    1: '1️⃣',
    2: '2️⃣',
    3: '3️⃣',
    4: '4️⃣',
    5: '5️⃣',
    6: '6️⃣',
    7: '7️⃣️',
    8: '8️⃣',
    9: '9️⃣',
    10: '🔟'
}

#emoji2int = {value: key for (key, value) in int2emoji.items()}

DB_TABLES = DBTables()
