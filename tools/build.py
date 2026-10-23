"""根据游戏原版配置表生成「归墟珍宝阁」mod 的 Output/*.xml、modData.json 和商品清单。

用法: python build.py <解包目录> <输出 mod 目录>
解包目录需包含从游戏 AssetBundle 解出的 data/TbItemCfg、data/TbTypeCfg、loc/TbItemCfgLocal（见 README）。
"""
import json,uuid,os,sys,xml.etree.ElementTree as ET
S=sys.argv[1]; OUT=sys.argv[2]
types={e.find('id').text:(e.find('parent').text if e.find('parent') is not None else None) for e in ET.parse(f'{S}/data/TbTypeCfg').getroot()}
def top(t): p=types.get(str(t)); return int(p) if p and p!='-1' else int(t)
loc={e.find('id').text:e.find('Chinese').text for e in ET.parse(f'{S}/loc/TbItemCfgLocal').getroot()}
items=[i for i in json.load(open(f'{S}/data/TbItemCfg',encoding='utf-8-sig')) if i.get('block',0)!=1]
def pick(f): return sorted([i for i in items if f(i)], key=lambda i:(i.get('gradeId',0),int(i['id']) if i['id'].isdigit() else 0))
G3=set(range(312,316))      # 四阶上品及以上（锻造锤、丹炉）
G4=set(range(310,316))      # 四阶下品及以上（材料、灵草）
GS=set(range(19,23))        # 地阶上品至天阶上品（功法、术法）
mat =pick(lambda i: top(i.get('typeId',0))==11 and i.get('gradeId') in G4)
mat3=pick(lambda i: top(i.get('typeId',0))==11 and i.get('gradeId')==309)
ham =pick(lambda i: i.get('typeId')==910 and i.get('gradeId') in G3)
herb=pick(lambda i: top(i.get('typeId',0))==10 and i.get('gradeId') in G4)
herb3=pick(lambda i: top(i.get('typeId',0))==10 and i.get('gradeId')==309)
furn=pick(lambda i: i.get('typeId')==906 and i.get('gradeId') in G3)
gong=pick(lambda i: top(i.get('typeId',0))==3 and i.get('gradeId') in GS)
shu =pick(lambda i: top(i.get('typeId',0))==4 and i.get('gradeId') in GS)
rune=pick(lambda i: i.get('typeId')==911)
BUILD=9001
funcs=[(9001,'材料','11,99',11355),(9002,'功法','3',10491),(9003,'术法','4',10491),(9004,'灵草','10,99',10515),(9005,'符文','99',10516)]
# (row id, function, items, stock count)
rows=[(9001,9001,mat,10),(9002,9001,ham,1),(9003,9002,gong,1),(9004,9003,shu,1),(9005,9004,herb,10),(9006,9004,furn,1),(9007,9005,rune,1),(9008,9001,mat3,20),(9009,9004,herb3,20)]
H='<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
def arr(name,entries):
    s=H+f'<ArrayOf{name} xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n'
    for e in entries:
        s+=f'\t<{name}>\n'+''.join(f'\t\t<{k}>{v}</{k}>\n' for k,v in e)+f'\t</{name}>\n'
    return s+f'</ArrayOf{name}>\n'
os.makedirs(f'{OUT}/Output',exist_ok=True); os.makedirs(f'{OUT}/Config',exist_ok=True)
w=lambda n,s: open(f'{OUT}/Output/{n}.xml','w',encoding='utf-8').write(s)
w('TbBuildCfg',arr('TbBuildCfg',[[('id',BUILD),('name','归墟珍宝阁'),('order',5),('place',2),('buildIcon','Icon/build/wanbaolou'),('path','SceneBG/wanbaolou'),('functionId',','.join(str(f[0]) for f in funcs))]]))
w('TbFunctionCfg',arr('TbFunctionCfg',[[('id',i),('name',n),('remark','归墟珍宝阁 '+n),('type',1),('saleId',s),('npcId',npc)] for i,n,s,npc in funcs]))
w('TbPlaceTypeCfg',arr('TbPlaceTypeCfg',[[('id',238),('name','1_238'),('buildId',f'46,2,3,16,{BUILD}')]]))
w('TbShopFixCfg',arr('TbShopFixCfg',[[('id',rid),('mapId','10'),('buildId',BUILD),('functionId',fid),('fixItemId',','.join(i['id'] for i in its)),('itemNumber',n)] for rid,fid,its,n in rows]))
w('TbFindCfg',arr('TbFindCfg',[[('id',9001),('name','归墟珍宝阁不刷随机商品'),('mapId','10'),('place',2),('buildId',BUILD),('weight',999),('count',0),('layerId',4)]]))
# 保留已有 mod Id，避免游戏把它当成新 mod
_md=f'{OUT}/Config/modData.json'
mid=json.load(open(_md,encoding='utf-8'))['Id'] if os.path.exists(_md) else uuid.uuid4().hex
json.dump({"Id":mid,"name":"归墟珍宝阁","perview":"","description":"在终章归墟岛的奉仙镇新增建筑「归墟珍宝阁」，分五个柜台出售顶级货物：材料（三阶上品及以上材料、四阶上品及以上锻造锤）、功法、术法（地阶上品至天阶上品）、灵草（三阶上品及以上灵草、四阶上品及以上丹炉），另设符文柜台出售全部锻造符文。每30天补货。","language":0,"tags":["商店"],"gameVersion":"","isOpenSource":True,"author":"JIANYU TANG","authorId":0,"publishfileid":0,"dependency":[],"modVisibility":0,"changeLog":"1.2 材料灵草扩充到三阶上品起，功法术法扩充到地阶上品起；1.1 新增符文柜台；1.0 初版"},open(f'{OUT}/Config/modData.json','w',encoding='utf-8'),ensure_ascii=False,indent=2)
with open(f'{OUT}/商品清单.txt','w',encoding='utf-8') as f:
    for rid,fid,its,n in rows:
        fn=[x[1] for x in funcs if x[0]==fid][0]
        f.write(f'== {fn}（每种 {n} 个）\n')
        for i in its: f.write(f"  {i['id']}\t{loc.get(i['name'],i['name'])}\tgrade {i['gradeId']}\t价格 {i.get('price')}\tmaxCount {i.get('maxCount')}\n")
print({k:len(v) for k,v in dict(mat=mat,ham=ham,herb=herb,furn=furn,gong=gong,shu=shu,rune=rune,mat3=mat3,herb3=herb3).items()})
