from typing import List, Any, Tuple, Optional
from collections import Counter
from dataclasses import dataclass

import requests
import yaml


@dataclass
class Config:
    api_key: str

    @staticmethod
    def load() -> 'Config':
        with open('config.yml') as f_config:
            config_yaml = yaml.load(f_config, Loader=yaml.CLoader)
        return Config(
            api_key=config_yaml['API_KEY'],
        )


@dataclass
class MediaWithCount:
    title: str
    count: int


class MovieWithCount(MediaWithCount):
    pass


class TVWithCount(MediaWithCount):
    pass