import pathlib

import yaml


HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
STAGES_YML = ROOT / 'data' / 'stages.yml'

with open(STAGES_YML) as fp:
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
