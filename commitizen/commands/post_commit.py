import os
import tempfile
from pathlib import Path

from commitizen.config import BaseConfig


class PostCommit:
    def __init__(self, config: BaseConfig, *args):
        pass

    def __call__(self, *args, **kwargs):
        exit(self.post_commit())

    def post_commit(self):
        backup_file = Path(
            tempfile.gettempdir(), f"cz.commit{os.environ.get('USER', '')}.backup"
        )
        print(backup_file, '=== 이거 실행 안되나?', flush=True)

        # remove backup file if it exists
        if backup_file.is_file():
            backup_file.unlink()
