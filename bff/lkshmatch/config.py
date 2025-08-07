from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="MATCH",
    settings_files=['config.toml'],
    environments=True,
    load_dotenv=True,
    default_env="prod",
    env="test",
)
