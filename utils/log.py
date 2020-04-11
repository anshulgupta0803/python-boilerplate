from datetime import datetime
import logging
from pathlib import Path

from tqdm.auto import tqdm


class TqdmHandler(logging.StreamHandler):
    def __init__(self):
        logging.StreamHandler.__init__(self)

    def emit(self, record):
        msg = self.format(record)
        tqdm.write(msg)


class Logger:
    __instance = None

    @staticmethod
    def get_instance(cfg=None):
        if Logger.__instance is None:
            if cfg is None:
                raise Exception("Missing configuration")
            Logger(cfg)
        return Logger.__instance.logger

    def __init__(self, cfg):
        if Logger.__instance is not None:
            raise Exception(
                "Use get_instance() method as this is a singleton class")
        Logger.__instance = self
        self.init_logger(cfg)

    def init_logger(self, cfg):
        self.logger = logging.getLogger(cfg.exp_name)
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            fmt="%(asctime)s - [%(levelname)-8s] %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S%z"
        )  # ISO8601

        try:
            _ = get_ipython().__class__.__name__
            console_handler = logging.StreamHandler()
        except NameError:
            console_handler = TqdmHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        try:
            _ = cfg.logs_dir
        except AttributeError:
            cfg.logs_dir = "logs"

        logs_dir = Path(cfg.logs_dir)
        if not logs_dir.exists():
            logs_dir.mkdir()

        log_file_path = logs_dir / \
            datetime.now().strftime("%Y-%m-%d-%H-%M-%S-{}.log".format(cfg.exp_name))

        cfg.log_file_path = log_file_path

        file_handler = logging.FileHandler(str(log_file_path))
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
