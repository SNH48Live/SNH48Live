import yaml

from common import DATA_DIR


with open(DATA_DIR / 'stages.yml') as fp:
    STAGES = yaml.load(fp)


def title2stage(title):
    for stage in STAGES:
        if stage in title:
            return stage
    return None


def stage2team(stage):
    if stage is None:
        return 'joint'
    elif stage in STAGES:
        return STAGES[stage]['team']
    else:
        raise ValueError(f"'{stage}' is not a recognized stage")
