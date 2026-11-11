import pathlib

import yaml

DATA = pathlib.Path(__file__).parent.parent / "data" / "monsters.yaml"
ELEMENTS = ["불", "물", "풀", "전기", "땅"]


def load():
    return yaml.safe_load(DATA.read_text(encoding="utf-8"))


def test_level_range():
    for m in load():
        assert isinstance(m["level"], int), m["id"]
        assert 1 <= m["level"] <= 99, m["id"]


def test_hp_positive():
    for m in load():
        assert isinstance(m["hp"], int), m["id"]
        assert m["hp"] > 0, m["id"]


def test_element_allowed():
    for m in load():
        assert m["element"] in ELEMENTS, m["id"]


def test_weakness_not_same():
    for m in load():
        assert m["weakness"] != m["element"], m["id"]


def test_id_unique():
    ids = [m["id"] for m in load()]
    assert len(ids) == len(set(ids))