import unittest
import tempfile
import os

from calendar_app.calendar import Calendar


class CalendarTests(unittest.TestCase):
    def test_add_and_list(self):
        fd, db_path = tempfile.mkstemp()
        os.close(fd)
        cal = None
        try:
            cal = Calendar(db_path)
            eid = cal.add_event("Test event", "2025-11-11 10:00")
            self.assertIsInstance(eid, int)
            events = cal.list_events()
            self.assertTrue(any(e['id'] == eid for e in events))
        finally:
            if cal:
                cal.conn.close()
            os.unlink(db_path)

    def test_list_by_date(self):
        fd, db_path = tempfile.mkstemp()
        os.close(fd)
        cal = None
        try:
            cal = Calendar(db_path)
            cal.add_event("Morning", "2025-11-12 09:00")
            cal.add_event("Afternoon", "2025-11-12 14:00")
            events = cal.list_events("2025-11-12")
            self.assertEqual(len(events), 2)
        finally:
            if cal:
                cal.conn.close()
            os.unlink(db_path)

    def test_remove(self):
        fd, db_path = tempfile.mkstemp()
        os.close(fd)
        cal = None
        try:
            cal = Calendar(db_path)
            eid = cal.add_event("To remove", "2025-11-13 12:00")
            ok = cal.remove_event(eid)
            self.assertTrue(ok)
            events = cal.list_events()
            self.assertFalse(any(e['id'] == eid for e in events))
        finally:
            if cal:
                cal.conn.close()
            os.unlink(db_path)


if __name__ == '__main__':
    unittest.main()
