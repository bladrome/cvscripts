#!/usr/bin/env python3

import mmcv

import mmdet
from mmseg.models import BACKBONES
from mmcv.utils import build_from_cfg
from mmcv.runner import load_checkpoint

import sys


configfile = sys.argv[1]

cfg = mmcv.Config.fromfile(configfile)
model = build_from_cfg(cfg.model, BACKBONES)

print(f'Config:\n{cfg.pretty_text}')
