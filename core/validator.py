import urllib.request
import json

class Validator:
    @staticmethod
    def check_slack(token):
        """Validates Slack tokens via auth.test API."""
        url = "https://slack.com/api/auth.test"
        req = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}'})
        try:
            with urllib.request.urlopen(req) as response:
                res = json.loads(response.read().decode())
                return res.get("ok", False)
        except:
            return False

    @staticmethod
    def check_github(token):
        """Validates GitHub PAT tokens."""
        url = "https://api.github.com/user"
        req = urllib.request.Request(url, headers={'Authorization': f'token {token}'})
        try:
            with urllib.request.urlopen(req) as response:
                return response.getcode() == 200
        except:
            return False
