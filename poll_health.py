import time, requests, sys

for i in range(15):
    try:
        r = requests.get('http://localhost:5000/health', timeout=1)
        print('HEALTH_OK', r.status_code)
        print(r.text)
        sys.exit(0)
    except Exception:
        print('.', end='', flush=True)
        time.sleep(1)

print('HEALTH_TIMEOUT')
sys.exit(1)
