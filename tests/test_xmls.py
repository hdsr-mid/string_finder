from pathlib import Path
from typing import List

import pytest

from string_finder.constants import TEST_DATA_DIR
from string_finder.finder import StringsInFilesFinder


@pytest.fixture
def caw_xml_paths() -> List[Path]:
    xml_dir = TEST_DATA_DIR / "xmls"
    assert xml_dir.is_dir()
    _paths = [x for x in xml_dir.iterdir()]
    assert (
        len(_paths) == 4
    ), f"expected 4 xml files in {xml_dir}, but found {len(_paths)}"
    return _paths


def test_1(caw_xml_paths):

    word_files_finder = StringsInFilesFinder(
        file_paths=caw_xml_paths,
        strings=["WIJKERSLOOT", "2011-09-19"],
        get_lines=False,
        stop_after_first_file_hit=True,
        stop_after_first_line_hit=True,
    )
    results = word_files_finder.run()
    assert results == {
        TEST_DATA_DIR / "xmls/HDSR_CAW_1.xml": {"WIJKERSLOOT": "", "2011-09-19": ""}
    }


def test_2(caw_xml_paths):
    word_files_finder = StringsInFilesFinder(
        file_paths=caw_xml_paths,
        strings=["WIJKERSLOOT", "2011-09-19"],
        get_lines=True,
        stop_after_first_file_hit=True,
        stop_after_first_line_hit=True,
    )
    results = word_files_finder.run()
    assert results == {
        TEST_DATA_DIR / "xmls/HDSR_CAW_1.xml": {"WIJKERSLOOT": 12, "2011-09-19": 8}
    }


def test_3(caw_xml_paths):
    word_files_finder = StringsInFilesFinder(
        file_paths=caw_xml_paths,
        strings=["WIJKERSLOOT", "2011-09-19"],
        get_lines=True,
        stop_after_first_file_hit=False,
        stop_after_first_line_hit=True,
    )
    results = word_files_finder.run()
    assert results == {
        TEST_DATA_DIR / "xmls/HDSR_CAW_1.xml": {"WIJKERSLOOT": 12, "2011-09-19": 8},
        TEST_DATA_DIR / "xmls/HDSR_CAW_4.xml": {"WIJKERSLOOT": 12, "2011-09-19": 79},
    }


def test_4(caw_xml_paths):
    word_files_finder = StringsInFilesFinder(
        file_paths=caw_xml_paths,
        strings=["WIJKERSLOOT", "2011-09-19"],
        get_lines=True,
        stop_after_first_file_hit=False,
        stop_after_first_line_hit=False,
    )
    results = word_files_finder.run()
    assert results == {
        TEST_DATA_DIR
        / "xmls/HDSR_CAW_1.xml": {
            "WIJKERSLOOT": [12, 35, 59, 90],
            "2011-09-19": [
                8,
                9,
                17,
                20,
                21,
                22,
                23,
                31,
                32,
                40,
                43,
                44,
                45,
                46,
                47,
                55,
                56,
                64,
                67,
                68,
                69,
                70,
                71,
                72,
                73,
                74,
                75,
                76,
                77,
                78,
                86,
                87,
                95,
                98,
                99,
                116,
                136,
                147,
                148,
                156,
                159,
                167,
                168,
                176,
                179,
                196,
                216,
                227,
                228,
                236,
                239,
                247,
                248,
                256,
                259,
                267,
                268,
                276,
                279,
                280,
                281,
                282,
                283,
                284,
                285,
                286,
                287,
                288,
                296,
                297,
                305,
                308,
                316,
                317,
                325,
                328,
                336,
                337,
                345,
                348,
                356,
                357,
                365,
                368,
                376,
                377,
                385,
                388,
                396,
                397,
                405,
                408,
                416,
                417,
                425,
                428,
                429,
                430,
                431,
                432,
                433,
                434,
                435,
                436,
                437,
                438,
                439,
                440,
                441,
                442,
                443,
                444,
                445,
                446,
                447,
                448,
                449,
                450,
                451,
                452,
                453,
                454,
                455,
                456,
                457,
                458,
                459,
                460,
                461,
                462,
                463,
                464,
                465,
                466,
                467,
                468,
                469,
                470,
                471,
                472,
                473,
                474,
                475,
                483,
                484,
                492,
                495,
                496,
                497,
                498,
                499,
                500,
                501,
                502,
                503,
                504,
                505,
                506,
                507,
                508,
                509,
                510,
                511,
                512,
                513,
                514,
                515,
                516,
                517,
                518,
                519,
                520,
                521,
                522,
                523,
                524,
                525,
                526,
                527,
                528,
                529,
                530,
                531,
                532,
                533,
                534,
                535,
                536,
                537,
                538,
                539,
                540,
                541,
                542,
            ],
        },
        TEST_DATA_DIR
        / "xmls/HDSR_CAW_4.xml": {
            "WIJKERSLOOT": [12, 32, 83],
            "2011-09-19": [79, 80, 88, 91, 92, 93, 94],
        },
    }