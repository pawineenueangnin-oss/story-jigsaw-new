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
