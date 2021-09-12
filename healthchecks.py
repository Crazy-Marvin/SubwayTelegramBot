import dotenv, os, requests

try:
    requests.get("https://hc-ping.com/db037b86-718a-4ce1-aecc-70e0a994965e", timeout=300)
except requests.RequestException as e:
    print("Ping failed: %s" % e)
