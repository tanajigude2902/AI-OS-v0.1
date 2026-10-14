import os
import json
import subprocess

class DeviceTools:
    @staticmethod
    def toggle_torch(state: bool):
        val = "on" if state else "off"
        os.system(f"termux-torch {val}")
        return f"Torch {val}"

    @staticmethod
    def get_battery():
        try:
            res = subprocess.check_output(["termux-battery-status"]).decode("utf-8")
            data = json.loads(res)
            return f"Battery {data.get('percentage')}% hai, status: {data.get('status')}."
        except Exception:
            return "Battery status check nahi ho paya."

    @staticmethod
    def open_app_or_url(url_or_pkg):
        os.system(f"termux-open-url {url_or_pkg}")
        return f"Opening {url_or_pkg}"

    @staticmethod
    def send_notification(title, content):
        os.system(f'termux-notification --title "{title}" --content "{content}"')
        return "Notification sent."
