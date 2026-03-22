# analysis/geoip.py
# Looks up an IP address → returns country, city, ISP.
# Uses ip-api.com (free, no API key needed, 45 req/min limit).

import requests

_cache = {}   # store results so we don't look up same IP twice

def get_geo(ip: str) -> dict:
    """
    Input:  "45.142.212.100"
    Output: {"country":"Russia", "city":"Moscow", "isp":"Selectel", ...}
    """
    # Skip private/local IPs — they have no geolocation data
    if ip.startswith(("127.", "192.168.", "10.", "172.", "::1")):
        return {"country": "Local", "city": "localhost", "isp": "private"}

    if ip in _cache:
        return _cache[ip]

    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
        d = r.json()
        if d.get("status") == "success":
            result = {
                "country":      d.get("country",     "Unknown"),
                "country_code": d.get("countryCode", ""),
                "city":         d.get("city",        "Unknown"),
                "isp":          d.get("isp",         "Unknown"),
                "lat":          d.get("lat",         0),
                "lon":          d.get("lon",         0),
            }
            _cache[ip] = result
            return result
    except Exception as e:
        print(f"[GEO] Failed for {ip}: {e}")

    return {"country": "Unknown", "city": "Unknown", "isp": "Unknown"}