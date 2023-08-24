from typing import Optional

import yaml
from yaml.loader import SafeLoader
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class NERConfig(BaseModel):
    stanza_path: str = "models/stanza_model"
    ner_hf: str = "models/ner_bert"


class APISettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='api_', env_file='config/.env')

    max_input_length: int = 10000
    config_path: str = "config/config.yaml"
    version: Optional[str] = None

api_settings = APISettings()

with open(api_settings.config_path, 'r', encoding='utf-8') as f:
    ner_config = NERConfig(**yaml.load(f, Loader=SafeLoader))
