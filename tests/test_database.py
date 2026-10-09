from core.events import Event
from database.db import Database
def test_database_roundtrip(tmp_path):
 db=Database(tmp_path/'test.db'); db.initialize(); db.insert_event(Event('CONNECTION')); assert db.stats()[0]['events']==1
