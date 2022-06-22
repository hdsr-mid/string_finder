from pathlib import Path

CHUNK_READ_THRESHOLD_BYTES = 1024 * 4
PROGRESS_PERCENTAGE_STEP = 5


# PATH CONSTANTS
# --------------
# BASE_DIR avoid 'Path.cwd()', as ftp_results.main() should be callable from everywhere
BASE_DIR = Path(__file__).parent.parent
TEST_DATA_DIR = BASE_DIR / "tests" / "data"
