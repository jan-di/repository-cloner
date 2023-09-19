import related


@related.immutable
class GithubConfig(object):
    apiUrl = related.StringField(required=False)
    apiToken = related.StringField(required=False)
    syncStrategy = related.StringField(required=False)


@related.immutable
class Target(object):
    name = related.StringField()
    basePath = related.StringField()
    type = related.StringField()
    github = related.ChildField(GithubConfig, required=False)


@related.immutable
class Config(object):
    targets = related.SequenceField(Target, required=False)


def read_config(file: str = "config.yaml"):
    with open(file, "r", encoding="utf8") as f:
        config_yaml = f.read()

    return related.to_model(Config, related.from_yaml(config_yaml))
