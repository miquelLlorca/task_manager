import datetime
from data import *
import subprocess

EVENTS_FILE = "/home/miquel/Escritorio/REPOS/task_manager/data/events.json"
reminder_days = 7



class Notifier:
    @staticmethod
    def send(title, message, urgency="normal", icon=None, timeout=5000):
        """
        urgency: "low", "normal", "critical"
        timeout: milliseconds
        icon: path to PNG/SVG or system icon name
        """

        cmd = ["notify-send"]

        # urgency
        cmd += ["--urgency", urgency]

        # timeout (ms)
        cmd += ["--expire-time", str(timeout)]

        # icon (optional)
        if icon:
            cmd += ["--icon", icon]

        # title + message
        cmd += [title, message]

        subprocess.run(cmd)



def check_reminders():
    events = load_events()
    now = datetime.datetime.now()

    for ev in events:
        print(ev)
        start = ev.get("start")
        if not start:
            continue

        # Parse date
        try:
            start_dt = datetime.datetime.fromisoformat(start)
        except Exception:
            continue

        delta = start_dt - now 
        # If now crossed the reminder time

        if(delta <= datetime.timedelta(days=1)):
            msg = f"Starts at {start_dt.strftime('%Y-%m-%d %H:%M')}"
            Notifier.send(
                "🔥 Deadline approaching",
                msg,
                urgency="critical"
            )

        elif (delta <= datetime.timedelta(days=reminder_days)):
            title = f"⏰ Reminder: {ev['category']} - {ev['title']}"
            msg = f"Starts at {start_dt.strftime('%Y-%m-%d %H:%M')}"
            Notifier.send(
                title,
                msg,
                urgency="critical"
            )

if __name__ == "__main__":
    check_reminders()