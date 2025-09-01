from utils.constants import REGION_LIST, TIER_LIST, MAP_LIST, HERO_LIST

def test_region_list():
    assert isinstance(REGION_LIST, list)
    assert set(REGION_LIST) == {"Americas", "Asia", "Europe"}

def test_tier_list():
    assert "All" in TIER_LIST
    assert all(isinstance(t, str) for t in TIER_LIST)

def test_map_list():
    assert "all-maps" in MAP_LIST
    assert all(isinstance(m, str) for m in MAP_LIST)

def test_hero_list():
    assert "Ana" in HERO_LIST
    assert "Tracer" in HERO_LIST
    assert all(isinstance(h, str) for h in HERO_LIST)
