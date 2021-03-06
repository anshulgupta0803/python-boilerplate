import argparse
from pathlib import Path
import time

from easydict import EasyDict as edict
import yaml
from tqdm.auto import tqdm

from utils.log import Logger


def load_config(args):
    config_file_path = 'config.yml' if args.config_file is None else args.config_file
    config_file_path = Path(config_file_path)

    with open(config_file_path) as config_file:
        cfg = yaml.safe_load(config_file)

    if cfg is None:
        cfg = dict()

    cfg['config_file'] = config_file_path

    for key, value in cfg.items():
        del cfg[key]
        cfg[key.lower()] = value

    for key, value in vars(args).items():
        if key.lower() in cfg:
            continue
        cfg[key.lower()] = value

    return edict(cfg)


def main(nbargs=()):
    parser = argparse.ArgumentParser()

    parser.add_argument("--exp-name", default="default",
                        help="Name of the experiment")

    parser.add_argument("--logs-dir", default="logs",
                        help="Directory for storing logs")

    parser.add_argument("--config-file", default=None,
                        help="Path to config.yml")

    try:
        _ = get_ipython().__class__.__name__
        args = parser.parse_args(nbargs)
    except NameError:
        args = parser.parse_args()

    cfg = load_config(args)

    logger = Logger.get_instance(cfg)

    logger.info("Configuration")
    logger.info("-" * 50)
    for key, value in cfg.items():
        logger.info("{:25s}:\t{:s}".format(str(key), str(value)))
    logger.info("-" * 50)

    for i in tqdm(range(5)):
        logger.info("Info message {:d}".format(i))
        time.sleep(0.5)

    return cfg


if __name__ == "__main__":
    main()
