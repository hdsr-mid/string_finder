from pathlib import Path

from path_finder import FileFinder

from string_finder.finder import StringsInFilesFinder

file_finder = FileFinder(
    single_start_dir=Path("Q:/") / "WIS" / "CAW" / "Oppervlaktewater",
    extension=".xml",
    limit_depth=False,
    filename_regex="^HDSR_CAW_[0-9]{12}$",
)
print(len(file_finder.paths))

# #081_ES1 ['TUURDIJK' || 'Eindstand Stuw Neer'],2010-01-01 00:00:00,2013-03-26 00:00:00
# 081_ES1 bestond  volgens roger niet voor 2011, lets see:
word_files_finder = StringsInFilesFinder(
    file_paths=file_finder.paths,
    strings=["TUURDIJK", "2010-01-01"],
    get_lines=False,
    stop_after_first_file_hit=False,
    stop_after_first_line_hit=False,
)
results = word_files_finder.run()
print(results)
