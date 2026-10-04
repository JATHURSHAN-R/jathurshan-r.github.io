"""Contract and privacy regression checks; no network or real secrets."""
import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('sync_htb', Path(__file__).resolve().parents[1] / 'scripts/sync_htb.py')
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)

class SyncTests(unittest.TestCase):
    def test_only_selected_fields_leave_api_boundary(self):
        basic = {'profile': {'id':2170950, 'system_owns':11, 'user_owns':12, 'email':'private@example.invalid', 'account_id':'private', 'rank':'Legacy rank'}}
        challenges = {'profile': {'challenge_owns': {'solved':1, 'total':856}}}
        self.assertEqual(sync.selected_fields(basic, challenges), {'htb_system_owns':'11', 'htb_user_owns':'12', 'htb_challenges':'1'})
    def test_wrong_profile_fails(self):
        with self.assertRaises(sync.SyncError):
            sync.selected_fields({'profile':{'id':1}}, {})
    def test_missing_schema_fails(self):
        with self.assertRaises(sync.SyncError):
            sync.selected_fields({'profile':{'id':2170950}}, {'profile':{}})
    def test_invalid_counts_fail(self):
        for value in (True, -1, 1.5, '11', None, 1000001):
            with self.subTest(value=value), self.assertRaises(sync.SyncError):
                sync.count(value)
    def test_user_flag_is_not_claimed_as_completion(self):
        fields = sync.activity_fields({'data':[{'type':'user','name':'Nimbus','private':'excluded'}]})
        self.assertEqual(fields, {'htb_activity_name':'Nimbus','htb_activity_label':'user flag recorded'})
    def test_non_machine_activity_is_ignored(self):
        fields = sync.activity_fields({'data':[{'type':'challenge','name':'Example'}]})
        self.assertEqual(fields['htb_activity_name'], 'No recent machine activity')
    def test_unexpected_activity_fails(self):
        with self.assertRaises(sync.SyncError):
            sync.activity_fields({'data':'unexpected'})
    def test_markup_in_activity_fails(self):
        with self.assertRaises(sync.SyncError):
            sync.activity_fields({'data':[{'type':'user','name':'<script>'}]})
    def test_redirects_are_not_followed(self):
        self.assertIsNone(sync.NoRedirect().redirect_request(None,None,302,'',{},'https://example.invalid'))

if __name__ == '__main__':
    unittest.main()
