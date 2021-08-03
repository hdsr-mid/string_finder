from pathlib import Path
from string_finder.constants import TEST_DATA_DIR
from typing import List

import pytest


@pytest.fixture
def caw_xml_paths() -> List[Path]:
    xml_dir = TEST_DATA_DIR / "xmls"
    assert xml_dir.is_dir()
    _paths = [x for x in xml_dir.iterdir()]
    assert len(_paths) == 4, f"expected 4 xml files in {xml_dir}, but found {len(_paths)}"
    return _paths
