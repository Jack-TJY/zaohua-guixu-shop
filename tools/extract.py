"""从游戏 AssetBundle 中解出 TextAsset 配置表。

用法: python extract.py <输出目录> <bundle 文件>...
需要: pip install UnityPy
"""
import os
import sys

import UnityPy

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
for f in sys.argv[2:]:
    env = UnityPy.load(f)
    for o in env.objects:
        if o.type.name == 'TextAsset':
            d = o.read()
            b = d.m_Script.encode('utf-8', 'surrogateescape') if isinstance(d.m_Script, str) else d.m_Script
            with open(os.path.join(out, d.m_Name), 'wb') as fp:
                fp.write(b)
