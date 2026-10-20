import json,glob,importlib.util,re
S={}
for f in sorted(glob.glob('_content/s*_*.py')):
    sp=importlib.util.spec_from_file_location('m',f);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);S.update(m.S)
for sid,d in S.items():
    assert len(d['st'])==16,sid
    loc={'th':[],'en':[],'es':[]}
    for i,r in enumerate(d['st']):
        assert len(r)==12,(sid,i)
        c=d['colors'][i//4]
        for k,o in (('th',0),('en',4),('es',8)): loc[k].append(list(r[o:o+4])+[c])
    imgs=[f"{d['art']}/chapter-{i}.webp" for i in range(1,17)]
    obj={'id':sid,'number':d['number'],'titles':d['titles'],'locales':loc,'images':imgs,'cover':imgs[0],'descriptions':d['desc']}
    open(f'story-catalog/{sid}.js','w').write(f'STORY_CATALOG["{sid}"]='+json.dumps(obj,ensure_ascii=False,separators=(',',':'))+';\n')
    print(sid,d['number'],d['art'])

# ---- extra languages ----
LANGS=['th','en','es','zh','ja','ko','vi','id','ms','fil','hi','ar','fr','de','it','pt','ru','tr','pl','nl','uk']
for sid,d in S.items():
    p=f'story-catalog/{sid}.js'; obj=json.loads(open(p).read().split('=',1)[1].rstrip().rstrip(';'))
    for lg in LANGS[3:]:
        sp=importlib.util.spec_from_file_location('st',f'_content/i18n/st_{lg}.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
        t,ds,st=m.ST[sid]; assert len(st)==16 and all(len(x)==4 and all(y.strip() for y in x) for x in st),(lg,sid)
        obj['titles'][lg]=t; obj['descriptions'][lg]=ds
        obj['locales'][lg]=[list(x)+[d['colors'][i//4]] for i,x in enumerate(st)]
    assert set(obj['locales'])==set(LANGS)
    open(p,'w').write(f'STORY_CATALOG["{sid}"]='+json.dumps(obj,ensure_ascii=False,separators=(',',':'))+';\n')
print('merged',len(LANGS),'langs')
