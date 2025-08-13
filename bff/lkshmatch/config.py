from dynaconf import Dynaconf

settings: Dynaconf = Dynaconf(
    envvar_prefix="MATCH",
    settings_files=["lkshmatch/config.toml"],
    environments=True,
    load_dotenv=True,
    default_env="prod",
    env="test"
)
