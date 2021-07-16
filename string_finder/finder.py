import logging
from pathlib import Path
from typing import Dict, List, TextIO

from string_finder.constants import CHUNK_READ_THRESHOLD_BYTES, PROGRESS_PERCENTAGE_STEP

logger = logging.getLogger(__name__)


class StringsInFilesFinder:
    def __init__(
        self,
        file_paths: List[Path],
        strings: List[str],
        get_lines: bool = False,
        stop_after_first_file_hit: bool = True,
        stop_after_first_line_hit: bool = True,
    ):
        self.file_paths = file_paths
        self.strings = strings
        self.get_lines = get_lines
        self.stop_after_first_file_hit = stop_after_first_file_hit
        self.stop_after_first_line_hit = stop_after_first_line_hit
        self.__validate_constructor()
        self.progress_mapper = self.get_progress_mapper(nr_file_paths=len(file_paths))

    def __validate_constructor(self):
        assert self.strings
        assert self.file_paths
        assert [isinstance(_string, str) for _string in self.strings]
        # assert [isinstance(_path, Path) for _path in self.file_paths]
        assert isinstance(self.get_lines, bool)
        assert isinstance(self.stop_after_first_file_hit, bool)
        assert isinstance(self.stop_after_first_line_hit, bool)

    @staticmethod
    def get_progress_mapper(
        nr_file_paths: int, progress_step: int = PROGRESS_PERCENTAGE_STEP
    ) -> Dict[int, int]:
        """Map file_index to a progress percentage [0-100] with (file_index / total_number_files * 100)
        Example:
            input:
                nr_xml_file_paths = 12
                log_stepsize = 2
            output: {file_index: percentage}
                {3: 25, 6: 50, 9: 75, 12: 100}
        """
        assert isinstance(nr_file_paths, int)
        assert 0 < progress_step < 100, "please use a progress_step between 0 and 100"
        # start=0, end=101 to make sure 100% is also logged
        percentages = [x for x in range(0, 101, progress_step)]
        progress_mapper = {
            (percentage / 100 * nr_file_paths) - 1: percentage
            for percentage in sorted(percentages)
        }
        progress_mapper = {round(k): v for k, v in progress_mapper.items() if k >= 0}
        return progress_mapper

    def __search_lines(
        self, text_io_chunks: List[TextIO], _path: Path, result: Dict
    ) -> Dict:
        string_line_nr = {}
        for _string in self.strings:
            if self.stop_after_first_line_hit:
                string_line_nr[_string] = self.__get_string_first_line(
                    _string=_string, text_io_chunks=text_io_chunks
                )
                assert string_line_nr[_string]
            else:
                string_line_nr[_string] = self.__get_string_all_lines(
                    _string=_string, text_io_chunks=text_io_chunks
                )
        assert sorted(string_line_nr.keys()) == sorted(self.strings)
        return string_line_nr

    @staticmethod
    def __get_string_first_line(_string: str, text_io_chunks: List[TextIO]) -> int:
        start_line_nr = 0
        for text_io_chunk in text_io_chunks:
            for line_nr, line in enumerate(text_io_chunk):
                if _string in line:
                    return start_line_nr + line_nr
            start_line_nr += len(text_io_chunk)

    @staticmethod
    def __get_string_all_lines(_string: str, text_io_chunks: List[TextIO]) -> List[int]:
        start_line_nr = 0
        line_nrs = []
        for text_io_chunk in text_io_chunks:
            for line_nr, line in enumerate(text_io_chunk):
                if _string in line:
                    line_nrs.append(start_line_nr + line_nr)
            start_line_nr += len(text_io_chunk)
        return line_nrs

    @staticmethod
    def __get_chunks(opened_file: TextIO, chunk_size: int = CHUNK_READ_THRESHOLD_BYTES):
        """Lazy function (generator) to read a file piece by piece."""
        while True:
            data = opened_file.readlines(chunk_size)  # better than opened_file.read()
            if not data:
                break
            yield data

    @staticmethod
    def __chunk_holds_string(text_io_chunk: TextIO, _string: str) -> bool:
        for file_line in text_io_chunk:
            if _string in file_line:
                return True
        return False

    def __file_holds_all_strings(self, text_io_chunks: List[TextIO]) -> bool:
        search_string_left = self.strings.copy()
        for chunk in text_io_chunks:
            if not search_string_left:
                return True
            for _string in search_string_left:
                if self.__chunk_holds_string(text_io_chunk=chunk, _string=_string):
                    search_string_left.remove(_string)
                    continue
        return False if search_string_left else True

    def run(self) -> Dict[Path, Dict]:
        logger.info(
            f"start finding {self.strings} in {len(self.file_paths)} files, get_lines={self.get_lines}"
        )
        result = {}
        for index, _path in enumerate(self.file_paths):
            progress = self.progress_mapper.get(index)
            if progress:
                logger.info(f"progress {progress}%")
            opened_file = open(file=_path, mode="r")
            text_io_chunks = [
                text_io_chunk
                for text_io_chunk in self.__get_chunks(opened_file=opened_file)
            ]
            if not self.__file_holds_all_strings(text_io_chunks=text_io_chunks):
                continue
            if self.get_lines:
                result[_path] = self.__search_lines(
                    text_io_chunks=text_io_chunks, _path=_path, result=result
                )
            else:
                result[_path] = {_string: "" for _string in self.strings}
            opened_file.close()
            if self.stop_after_first_file_hit:
                return result
        return result
