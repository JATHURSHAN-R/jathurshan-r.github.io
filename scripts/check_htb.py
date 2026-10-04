"""Read-only compatibility check for the owner's HTB profile. Never log responses."""
import json
import os
import urllib.request
import urllib.error

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def main():
    token = os.environ.get('HTB_API_TOKEN', '').strip()
    if not token:
        print('HTB_API_TOKEN is missing; no request sent.')
        return 1
    opener = urllib.request.build_opener(NoRedirect())
    paths = {'basic': 'v4/user/profile/basic', 'activity': 'v5/user/profile/activity', 'challenges': 'v4/user/profile/progress/challenges'}
    ok = True
    for label, path in paths.items():
        req = urllib.request.Request(
            f'https://labs.hackthebox.com/api/{path}/2170950',
            headers={'Authorization': 'Bearer ' + token, 'Accept': 'application/json', 'User-Agent': 'Flame77-Portfolio/1.0'})
        try:
            with opener.open(req, timeout=25) as response:
                print(label + ': HTTP ' + str(response.status) + '; JSON content type: ' + str('json' in response.headers.get('Content-Type','').lower()))
                raw = response.read(1024 * 1024 + 1)
                if len(raw) > 1024 * 1024:
                    raise ValueError('response size')
                data = json.loads(raw)
            if not isinstance(data, dict):
                raise ValueError('response shape')
            # Only schema names and explicitly selected public achievement values.
            print(label + ' top-level schema: ' + json.dumps({k:type(v).__name__ for k,v in data.items() if k.isidentifier() and len(k)<60}))
            profile = data.get('profile', data)
            if isinstance(profile, dict):
                print(label + ' profile schema: ' + json.dumps({k:type(v).__name__ for k,v in profile.items() if k.isidentifier() and len(k)<60}))
                safe = {}
                for key in ('id','rank','level','system_owns','user_owns','challenge_owns','machine_owns','total','owned','total_owns'):
                    value = profile.get(key)
                    if type(value) is int and 0 <= value <= 10000000:
                        safe[key] = value
                    elif key == 'rank' and isinstance(value,str) and len(value)<40 and all(c.isalpha() or c in ' -' for c in value):
                        safe[key] = value
                print(label + ' selected achievement fields: ' + json.dumps(safe))
                owns = profile.get('challenge_owns')
                if isinstance(owns,dict):
                    print('challenge counters: ' + json.dumps({k:v for k,v in owns.items() if k.isidentifier() and type(v) is int and 0<=v<=1000000}))
            activity = data.get('profile', data.get('activity', data.get('data')))
            if isinstance(activity,dict):
                activity = activity.get('activity')
            if isinstance(activity,list) and activity:
                item=activity[0]
                if isinstance(item,dict):
                    print('activity item schema: ' + json.dumps({k:type(v).__name__ for k,v in item.items() if k.isidentifier()}))
                    print('activity public fields: ' + json.dumps({k:v for k,v in item.items() if k in ('name','type','object_type','date','date_diff','flag_type') and isinstance(v,str) and len(v)<100}))
        except urllib.error.HTTPError as exc:
            print(label + ': HTTP ' + str(exc.code) + '; response omitted.')
            ok = False
        except Exception as exc:
            print(label + ': ' + type(exc).__name__ + '; details omitted.')
            ok = False
    return 0 if ok else 1

if __name__ == '__main__':
    raise SystemExit(main())
