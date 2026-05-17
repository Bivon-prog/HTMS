import requests, re

BASE = 'http://localhost:8000/api'

r = requests.post(f'{BASE}/auth/login/', json={'email': 'admin@htms.go.ke', 'password': 'Admin@1234'})
token = r.json()['token']['access']
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

r2 = requests.get(f'{BASE}/tickets/', headers=headers)
ticket_id = r2.json()['results'][0]['id']

r3 = requests.get(f'{BASE}/auth/', headers=headers, params={'role': 'Agent'})
j3 = r3.json()
agent_id = j3[0]['id'] if isinstance(j3, list) else j3['results'][0]['id']

# Assign request
r4 = requests.patch(
    f'{BASE}/tickets/{ticket_id}/assign/',
    headers=headers,
    json={'assigned_agent': agent_id}
)
print('Status:', r4.status_code)
if r4.status_code >= 400:
    body = r4.text
    # Try to get the exception message
    exc_match = re.search(r'<pre class="exception_value">(.*?)</pre>', body, re.DOTALL)
    if exc_match:
        print('Exception:', exc_match.group(1).strip()[:300])
    # Get all frames
    frames = re.findall(
        r'<code>(.*?)</code>.*?File "(.*?)", line (\d+), in (.*?)\n',
        body, re.DOTALL
    )
    # Simpler: grab all "File..." lines
    lines = [l.strip() for l in body.split('\n') if 'File' in l and '.py' in l]
    print('\nAll file references:')
    for l in lines[-15:]:
        clean = re.sub(r'<[^>]+>', '', l).strip()
        if clean:
            print(' ', clean)
    # Get the TypeError message
    tb = re.findall(r'TypeError[^<\n]*', body)
    print('\nTypeErrors found:')
    for t in tb[:5]:
        print(' ', t)
