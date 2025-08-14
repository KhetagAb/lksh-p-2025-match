from dynaconf import Dynaconf

settings: Dynaconf = Dynaconf(
    settings_files=["lkshmatch/config.toml"],
    environments=True,
    load_dotenv=True,
    default_env="prod",
    envvar_prefix=False, # don't force prefix matching
    env="test",
)
