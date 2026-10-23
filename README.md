# 归墟珍宝阁 —《造化仙缘》终章顶级商店 mod

在终章地图**归墟岛**的城镇**奉仙镇**里新增一栋建筑「归墟珍宝阁」，集中出售游戏里最高档的修炼物资。

使用游戏自带的 mod 系统，只用 XML/JSON 配置覆盖数据表，**不修改游戏原文件，不需要 BepInEx**。

## 柜台与商品

| 柜台 | 出售内容 | 每次补货数量 |
| --- | --- | --- |
| 材料 | 四阶上品材料 16 种；四阶上品至五阶上品锻造锤 5 把 | 材料每种 10 个，锻造锤每把 1 个 |
| 功法 | 天阶上品功法 32 本 | 每本 1 个 |
| 术法 | 天阶上品术法 50 本 | 每本 1 个 |
| 灵草 | 四阶上品灵草 16 种；四阶上品至五阶上品丹炉 5 个 | 灵草每种 10 个，丹炉每个 1 个 |

- 完整清单见 [`归墟珍宝阁/商品清单.txt`](归墟珍宝阁/商品清单.txt)。
- 只上架游戏中可正常使用的物品（排除了被游戏屏蔽的物品，五阶材料和灵草在原版里都是屏蔽状态）。
- 每 30 天补货一次，按物品原价出售（城市商铺价格倍率 1.0）。
- 不混入随机的低阶商品。

## 安装

1. 下载本仓库（Code → Download ZIP），解压。
2. 把 `归墟珍宝阁` 文件夹整个复制到：
   ```
   %USERPROFILE%\AppData\LocalLow\XiaMenLeiYun\Zaohua\MOD\
   ```
   复制后的结构应为 `MOD\归墟珍宝阁\Config\modData.json` 和 `MOD\归墟珍宝阁\Output\*.xml`。
3. 启动游戏，在 Mod 列表中确认「归墟珍宝阁」已启用（本地 mod 默认启用）。
4. 读档进入归墟岛的奉仙镇即可看到新建筑。读取旧存档时游戏会提示 mod 列表发生变化，确认即可。

卸载：删除 `MOD\归墟珍宝阁` 文件夹。

## 文件说明

```
归墟珍宝阁/
├── Config/modData.json      mod 元信息（名称、描述、Id）
├── Output/
│   ├── TbBuildCfg.xml       新建筑「归墟珍宝阁」（id 9001，外观借用万宝楼）
│   ├── TbFunctionCfg.xml    四个交易柜台（id 9001–9004）
│   ├── TbPlaceTypeCfg.xml   把新建筑加入奉仙镇（覆盖地点类型 238）
│   ├── TbShopFixCfg.xml     固定商品清单（id 9001–9006）
│   └── TbFindCfg.xml        关闭这栋建筑的随机商品（id 9001）
└── 商品清单.txt              人类可读的商品列表
tools/
├── extract.py               从游戏资源包解出原版配置表
└── build.py                 根据原版配置表生成上面的 mod 文件
```

### 兼容性

本 mod 新增的条目都使用 9001 起的 ID，并覆盖了地点类型 `238`（奉仙镇的建筑列表）。如果其他 mod 也修改了 `TbPlaceTypeCfg` 中的 238，或占用了同样的 ID，会互相覆盖，以加载顺序靠后的为准。

## 自行重新生成

游戏更新后物品可能变化，可以用 `tools/` 下的脚本重新生成商品清单（需要 Python 3 和 `pip install UnityPy`）。

游戏的配置表存放在 `Zaohua_Data\StreamingAssets\Others\` 下，文件名为 `bundle_` 加上目录名小写后 MD5 的前 16 位：

| 目录 | 文件 |
| --- | --- |
| Xml（物品类型等） | `bundle_0f635d0e0f3874ff.unity3d` |
| Json（含 TbItemCfg） | `bundle_466deec76ecdf5fc.unity3d` |
| LocalXml（中文名称） | `bundle_190aeea761628805.unity3d` |

```bash
O=<游戏目录>/Zaohua_Data/StreamingAssets/Others
python tools/extract.py unpacked/data $O/bundle_0f635d0e0f3874ff.unity3d $O/bundle_466deec76ecdf5fc.unity3d
python tools/extract.py unpacked/loc  $O/bundle_190aeea761628805.unity3d
python tools/build.py unpacked 归墟珍宝阁
```

`unpacked/` 是游戏原版数据，已在 `.gitignore` 中排除，请勿上传。

## 声明

本项目以 [MIT 许可证](LICENSE) 开源。

本项目为玩家自制 mod，与《造化仙缘》官方及开发商无关。游戏内容（物品名称等）版权归原作者所有。
