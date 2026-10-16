#region Data Cleanup
#region stop yelling about errors
import time
from time import struct_time as Time
class ImgRecord:
  time: float
  uuid: str
  pass

class db:
  @staticmethod
  def is_old_enough(rec: ImgRecord) -> bool:
    return True
  @staticmethod
  def add(rec: ImgRecord) -> None:
    pass
  OLD_OFFSET = 60*60*24*7*4
  @staticmethod
  def query(q: str|None = None) -> list[ImgRecord]:
    return [] 
  @staticmethod
  def cleanup():
    pass
#endregion

# Unit Test
def has_correct_filter():
  record = ImgRecord()
  record.time = time.time()
  record.time -= 60 * 60 * 24 * 29
  assert db.is_old_enough(record)
  
  rec2 = ImgRecord()
  rec2.time = time.time()
  assert not db.is_old_enough(rec2)

  record = ImgRecord()
  record.time = time.time() + 1000
  assert not db.is_old_enough(record)

  record = ImgRecord()
  record.time = time.time() - 67676767
  assert not db.is_old_enough(record)

# Integration Test
def finds_bad_entries():
  record = ImgRecord()
  record.time = time.time()
  db.add(record)
  db.cleanup()
  xs = db.query()
  assert record in xs

  record = ImgRecord()
  record.time = time.time() - db.OLD_OFFSET - 1
  db.add(record)
  db.cleanup()
  xs = db.query()
  assert record not in xs

  record = ImgRecord()
  record.time = time.time() + 10000
  db.add(record)
  db.cleanup()
  xs = db.query()
  assert record in xs

  for x in db.query():
    assert not db.is_old_enough(x)

# System Test
"""
1. Camera submits photo
2. Confirm photo in DB
3. Camera submits second photo, confirm in DB
4. Wait 5 weeks
5. Confirm only one of those photos is in DB
"""
"""
This test requires 5 weeks to run
due to requirement of naturally populating DB
with camera images.

Running this system test is entirely 
impractical and not recommmended.

There is no automated process
for this test, as is natural for
system tests.


"""




#endregion