#region Data Cleanup
#region stop yelling about errors
import time
from time import struct_time as Time
class ImgRecord:
  time: float
  uuid: str
  archived: bool
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
"""
This unit test tests the helper function
is_old_enough on DB. This function should
return true if the record is older than one month
(threshold for removal.) Otherwise, it should
return false.

Full test set is all possible Image Records. This
set is impractical to cover, since it includes 
variation other than in the time field
(the field we are examining within this tool).

Even within the time field, full testing is
impractical. Instead, we focus on very specific ages
of the records: over a month old, not a month old,
new, and future. Future records are erroneous
in nature, but should not result in a
malformed program state.

Our test tests one of each category, with an
additional test for being too old. If additional
tests are wanted for this feature, add them here.
"""
def has_correct_filter():
  record = ImgRecord()
  record.time = time.time()
  record.time -= 60 * 60 * 24 * 29
  assert db.is_old_enough(record)

  record = ImgRecord()
  record.time = time.time() - 42069
  assert not db.is_old_enough(record)
  
  rec2 = ImgRecord()
  rec2.time = time.time()
  assert not db.is_old_enough(rec2)

  record = ImgRecord()
  record.time = time.time() + 1000
  assert not db.is_old_enough(record)

  record = ImgRecord()
  record.time = time.time() - 67676767
  assert db.is_old_enough(record)



# Integration Test
"""
The integration test checks general DB I/O, as well
as the automated record cleanup process db.cleanup().

Our possible test vectors are all possible database
states. Even moreso than the unit test, the
set of test cases is entirely impossible to test
within a reasonable time.

We test three main categories: old, new, future, and
archived. Again, future is erroneous, but should not
cause a malformed database state. Old records
(older than a month) should be removed by
db.cleanup(), with some exceptions. Actual image
archival is not being tested here; simply that the
archived images will not be deleted for up to a
year.

This also checks the db to ensure that there
were no other records sneaking through. This
test thus requires a LOCK on the db while being
run.
"""
def finds_bad_entries():
  record = ImgRecord()
  record.time = time.time()
  db.add(record)
  db.cleanup()
  xs = db.query(f"UUID = {record.uuid}")
  assert record in xs

  # too old
  record = ImgRecord()
  record.time = time.time() - 60*60*24*29
  db.add(record)
  db.cleanup()
  xs = db.query(f"UUID = {record.uuid}")
  assert record not in xs

  # future
  record = ImgRecord()
  record.time = time.time() + 10000
  db.add(record)
  db.cleanup()
  xs = db.query(f"UUID = {record.uuid}")
  assert record in xs

  # almost too old
  record = ImgRecord()
  record.time = time.time() - 60*60*24*27
  db.add(record)
  db.cleanup()
  assert record in db.query(f"UUID = {record.uuid}")

  # archived image stays
  record = ImgRecord()
  record.time = time.time() - 67676767
  db.add(record)
  db.cleanup()
  assert record in db.query(f"UUID = {record.uuid}")

  # old archived image goes
  record = ImgRecord()
  record.time = time.time() - 6767676767
  db.add(record)
  db.cleanup()
  assert record not in db.query(f"UUID = {record.uuid}")

  # no records that shouldn't be there are there
  db.cleanup()
  for x in db.query():
    assert not db.is_old_enough(x)



# System Test
"""
System Test: This test is done in a live environment,
but due to the limited uptime this test server
is expected to have, cannot and should not
be automated.

This test is a full test of the archival service
only archiving a single image. Test vectors are
all real-world environments; somehow, this is
even more impossible to perform a full test set on.

Given the time required to run this test, this test
cannot be expected to be run multiple times
subsequently; thus, it should be run in parallel.

Additionally, to prevent any potential interference
from electronic failure, this test WILL NOT be run
automatically. It MUST be performed manually.

Recommended tools to run perform test include
a calendar and a notebook.
"""

"""
1. Camera submits photos over course of a day
2. Mark down UUIDs of all photos submitted that day at end
3. Wait 5 weeks
4. Confirm only one of those photos is in DB
5. Wait 1 year
6. Confirm none of these photos exists in DB
"""




#endregion