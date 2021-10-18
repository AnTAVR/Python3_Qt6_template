import logging
import os
import subprocess
from typing import Sequence, Dict

logger = logging.getLogger(__name__)


def run_command(command: Sequence[str],
                cwd: str = None,
                env: Dict[str, str] = None) -> subprocess.CompletedProcess:
    if cwd is None:
        cwd = os.getcwd()
    if env is None:
        env = os.environ.copy()
    logger.info("run {}; cwd = '{}'".format(command, cwd))
    result_run = subprocess.run(command, cwd=cwd, env=env, capture_output=True)
    if result_run.returncode:
        logger.warning("run {}; err = '{}'".format(command, result_run.stderr.decode()))
    return result_run
