import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from app import app

client = app.test_client()


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


def test_monster_detail():
    res = client.get("/monsters/slime")
    assert res.status_code == 200
    assert res.get_json()["name"] == "슬라임"


def test_monster_not_found():
    res = client.get("/monsters/abc")
    assert res.status_code == 404


def test_monster_list():
    data = yaml.safe_load((ROOT / "data" / "monsters.yaml").read_text(encoding="utf-8"))
    res = client.get("/monsters")
    assert len(res.get_json()) == len(data)


def test_filter_element():
    res = client.get("/monsters?element=불")
    monsters = res.get_json()
    assert len(monsters) > 0
    for m in monsters:
        assert m["element"] == "불"