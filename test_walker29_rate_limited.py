"""Offline tests; no motor SDK or robot connection."""
import json, math
import numpy as np
from walker29_rate_limited import Walker29, DEFAULT, NA

PATH = '/mnt/data/A29v14a.npz'
with open('/mnt/data/A29v14a.stance.json', encoding='utf-8') as f:
    js = json.load(f)

for h in ('0.80', '0.73'):
    ref=js[h]
    q=DEFAULT.copy();q[:NA]=ref['q']
    yaw=0.;pitch=math.radians(ref['pitch_deg'])
    quat=[math.cos(pitch/2),0.,math.sin(pitch/2),0.]
    walker=Walker29(path=PATH,max_cmd_step_rad=0.03)  # EXAMPLE only
    # In deployment this MUST be the last motor-publisher commanded target.
    walker.reset(h=float(h),last_sent_target_15=q[:NA].copy())
    last=q[:NA].copy()
    max_seen=0.
    for frame in range(100):
        sent=walker.step(np.zeros(3),quat,q,np.zeros(29),[0,0,0],float(h))
        delta=float(np.max(np.abs(sent-last)))
        assert delta <= 0.030001, (h, frame, delta)
        assert np.all(np.isfinite(sent))
        max_seen=max(max_seen,delta)
        if frame in (0,1,9,49,99):
            print('h',h, 'frame',frame,'max_sent_step',round(delta,5), 'raw_step',round(walker.last_diag['raw_max_step_rad'],5),
                  'raw_gap',round(walker.last_diag['raw_max_tracking_gap_rad'],5), 'joint',walker.last_diag['raw_max_tracking_gap_joint'])
        last=sent.copy()
    print('PASS', h, 'max_sent_step',max_seen)

# Fails closed unless the actual last published command is supplied.
w = Walker29(path=PATH)
try:
    w.step([0,0,0],[1,0,0,0],DEFAULT,np.zeros(29),[0,0,0],0.73)
except RuntimeError as e:
    print('PASS no prior command ->',str(e)[:75])
else:
    raise AssertionError('missing previous target did not fail closed')
