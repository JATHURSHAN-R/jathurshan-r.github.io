"""Sync only public achievement fields for HTB user 2170950.
The API token and full responses are never written to disk or logged.
"""
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, HTTPRedirectHandler, build_opener

ROOT = Path(__file__).resolve().parents[1]
USER_ID = 2170950
BASE = 'https://labs.hackthebox.com/api/'
LIMIT = 1024 * 1024

class SyncError(Exception):
    pass

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def fetch_json(path, token):
    request = Request(BASE + path, headers={
        'Authorization': 'Bearer ' + token,
        'Accept': 'application/json',
        'User-Agent': 'Flame77-Portfolio/1.0'})
    try:
        with build_opener(NoRedirect()).open(request, timeout=25) as response:
            if 'json' not in response.headers.get('Content-Type', '').lower():
                raise SyncError('HTB did not return JSON.')
            raw = response.read(LIMIT + 1)
        if len(raw) > LIMIT:
            raise SyncError('HTB response exceeded the size limit.')
        value = json.loads(raw)
        if not isinstance(value, dict):
            raise SyncError('Unexpected HTB response structure.')
        return value
    except HTTPError as exc:
        raise SyncError('HTB request failed with HTTP ' + str(exc.code) + '.') from None
    except SyncError:
        raise
    except Exception:
        raise SyncError('HTB request or JSON validation failed.') from None

def count(value):
    if type(value) is not int or not 0 <= value <= 1000000:
        raise SyncError('Invalid achievement count; nothing updated.')
    return str(value)

def selected_fields(basic, challenges):
    profile = basic.get('profile')
    challenge_profile = challenges.get('profile')
    if not isinstance(profile, dict) or type(profile.get('id')) is not int or profile['id'] != USER_ID:
        raise SyncError('Profile identity mismatch; nothing updated.')
    if not isinstance(challenge_profile, dict) or not isinstance(challenge_profile.get('challenge_owns'), dict):
        raise SyncError('Unexpected challenge schema; nothing updated.')
    return {
        'htb_system_owns': count(profile.get('system_owns')),
        'htb_user_owns': count(profile.get('user_owns')),
        'htb_challenges': count(challenge_profile['challenge_owns'].get('solved')),
    }

def activity_fields(response):
    events = response.get('data')
    if not isinstance(events, list) or len(events) > 1000:
        raise SyncError('Unexpected activity schema; nothing updated.')
    for event in events:
        if not isinstance(event, dict) or event.get('type') not in ('user', 'root'):
            continue
        name = event.get('name')
        if not isinstance(name, str) or not re.fullmatch(r"[\w .()'&-]{1,80}", name):
            raise SyncError('Invalid activity name; nothing updated.')
        return {'htb_activity_name': name,
                'htb_activity_label': 'user flag recorded' if event['type'] == 'user' else 'system flag recorded'}
    return {'htb_activity_name': 'No recent machine activity', 'htb_activity_label': 'No machine flags in the returned activity page'}

def main():
    token = os.environ.get('HTB_API_TOKEN', '').strip()
    if not token:
        raise SyncError('HTB_API_TOKEN is missing; existing deployment retained.')
    basic = fetch_json(f'v4/user/profile/basic/{USER_ID}', token)
    challenges = fetch_json(f'v4/user/profile/progress/challenges/{USER_ID}', token)
    fields = selected_fields(basic, challenges)
    activity = fetch_json(f'v5/user/profile/activity/{USER_ID}', token)
    fields.update(activity_fields(activity))
    fields['htb_synced_at'] = datetime.now(timezone.utc).strftime('%d %b %Y, %H:%M UTC')
    target = ROOT / 'content.json'
    content = json.loads(target.read_text(encoding='utf-8'))
    content.update(fields)
    # All responses validated before replacing the build input. No commit is made.
    temporary = target.with_suffix('.tmp')
    temporary.write_text(json.dumps(content, indent=2) + '\n', encoding='utf-8')
    temporary.replace(target)
    print('HTB sync successful: ' + fields['htb_system_owns'] + ' system owns, ' + fields['htb_user_owns'] + ' user owns, ' + fields['htb_challenges'] + ' challenges.')

if __name__ == '__main__':
    try:
        main()
    except SyncError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
    except Exception:
        print('Sync validation failed; existing deployment retained.', file=sys.stderr)
        raise SystemExit(1)
