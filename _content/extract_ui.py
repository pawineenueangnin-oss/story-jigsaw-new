import re,json
s=open('index.html').read()
def lit_at(s,i):
    q=s[i];j=i+1;out='';k=0
    while s[j]!=q:
        if s[j]=='\\': out+=s[j:j+2];j+=2;continue
        if q=='`' and s[j:j+2]=='${':
            d=1;j+=2
            while d:
                if s[j]=='{':d+=1
                elif s[j]=='}':d-=1
                j+=1
            out+='{%d}'%k;k+=1;continue
        out+=s[j];j+=1
    return out,j+1
def split_args(s,i):
    # i at '(' ; returns list of (start,end) for top-level args
    d=0;j=i;args=[];st=i+1
    while True:
        c=s[j]
        if c in '\'"`':
            _,j=lit_at(s,j);continue
        if c in '([{':d+=1
        elif c in ')]}':
            d-=1
            if d==0: args.append((st,j));return args,j
        elif c==',' and d==1: args.append((st,j));st=j+1
        j+=1
def lits(seg):
    out=[];j=0
    while j<len(seg):
        if seg[j] in '\'"`':
            v,j=lit_at(seg,j);out.append(v)
        else:j+=1
    return out
keys=set()
for m in re.finditer(r'storyLabel\(',s):
    if s[m.start()-9:m.start()]=='function ':continue
    args,_=split_args(s,m.end()-1)
    if len(args)>=2:
        for v in lits(s[args[1][0]:args[1][1]]): keys.add(v)
# UI_TEXTS en
i=s.find('const UI_TEXTS=');j=s.find('];\nconst UI_LOOKUP',i)
rows=json.loads(s[i+15:j+1].replace("'",'"')) if False else None
seg=s[i+15:j+1]
# parse rows by literal sequence groups of 3
L=lits(seg)
for k in range(1,len(L),3): keys.add(L[k])
# CORE en
i=s.find(' en:{levels:');keys.update(lits(s[i:s.find('\n',i)]))
# patterns en:`...`
for m in re.finditer(r'en:`',s): keys.add(lit_at(s,m.end()-1)[0])
for m in re.finditer(r"en:'",s): keys.add(lit_at(s,m.end()-1)[0])
keys={k.replace("\\'","'") for k in keys if re.search('[A-Za-z]',k)}
json.dump(sorted(keys),open('_content/ui_keys_en.json','w'),ensure_ascii=False,indent=0)
print(len(keys))
for k in sorted(keys): print(repr(k))
