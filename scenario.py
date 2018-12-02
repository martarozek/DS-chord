from xmlrpc.client import ServerProxy

from util import get_url
from config import APP_PORT, APP_IP


def scenario_1(app):
    app.put("3", "3")
    app.put("2", "2")
    app.put("1", "1")


def scenario_2(app):
    app.get("3")
    app.get("2")
    app.get("1")


def scenario_3(app):
    app.put("4", "4")
    app.get("4")
    app.put("5", "5")
    app.get("5")
    app.put("6", "6")
    app.get("6")


if __name__ == "__main__":
    app = ServerProxy(get_url(APP_IP, APP_PORT))
    scenario_1(app)
    scenario_2(app)
    scenario_3(app)