import os
from pathlib import Path

AUTHOR:   str = 'Ryuu Mitsuki'

ROOT_DIR: str = str(Path(__file__).resolve().parent.parent)
LOGS_DIR: str = os.path.join(ROOT_DIR, 'logs')
TMP_DIR:  str = os.path.join(ROOT_DIR, 'tmp')


del os, Path
