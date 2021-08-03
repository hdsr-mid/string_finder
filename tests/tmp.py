from path_finder import FileFinder
from pathlib import Path
from string_finder.finder import StringsInFilesFinder

import logging


def setup_logging() -> None:
    """Adds a configured strearm handler to the root logger."""
    log_level = logging.INFO
    log_date_format = "%H:%M:%S"
    log_format = "%(asctime)s %(filename)s %(levelname)s %(message)s"

    _logger = logging.getLogger()
    _logger.setLevel(log_level)
    formatter = logging.Formatter(fmt=log_format, datefmt=log_date_format)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(formatter)
    _logger.addHandler(stream_handler)


setup_logging()


logger = logging.getLogger(__name__)

logger.info("find files")
file_finder = FileFinder(
    single_start_dir=Path("Q:/") / "WIS" / "CAW" / "Oppervlaktewater",
    extension=".xml",
    limit_depth=False,
    filename_regex="^HDSR_CAW_[0-9]{12}$",
)
logger.info(f"found {len(file_finder.paths)}")

# #081_ES1 ['TUURDIJK' || 'Eindstand Stuw Neer'],2010-01-01 00:00:00,2013-03-26 00:00:00
# 081_ES1 bestond  volgens roger niet voor 2011, lets see:
word_files_finder = StringsInFilesFinder(
    file_paths=file_finder.paths,
    strings=["TUURDIJK", '<startDate date="2010-01-01"'],
    max_dist=6,
    get_lines=True,
    stop_after_first_file_hit=True,
    stop_after_first_line_hit=False,
)
results = word_files_finder.run()
print(results)
