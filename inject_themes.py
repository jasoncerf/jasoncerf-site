#!/usr/bin/env python3
import os
import re

THEME_BLOCK = '''
<!-- ─── Theme Switcher ─── -->
<style>
  #theme-toast {
    position: fixed; bottom: 2rem; left: 50%;
    transform: translateX(-50%) translateY(20px);
    background: var(--ink); color: var(--cream);
    padding: .5rem 1.4rem; border-radius: 2rem;
    font-family: 'DM Sans', sans-serif;
    font-size: .68rem; letter-spacing: .2em; text-transform: uppercase;
    z-index: 9999; opacity: 0;
    transition: opacity .3s, transform .3s;
    pointer-events: none;
    border: 1px solid rgba(128,128,128,.2);
  }
  #theme-toast.visible { opacity: 1; transform: translateX(-50%) translateY(0); }
  #theme-hint {
    position: fixed; bottom: .75rem; right: 1.2rem;
    font-family: 'DM Sans', sans-serif;
    font-size: .58rem; letter-spacing: .15em; text-transform: uppercase;
    color: var(--mid); opacity: .4; pointer-events: none; z-index: 100;
    transition: opacity .3s;
  }
  #theme-hint:hover { opacity: .8; }
  #theme-cycle-btn {
    display: none;
    position: fixed; bottom: 1.5rem; right: 1.2rem;
    width: 36px; height: 36px; border-radius: 50%;
    background: var(--tan); border: none; cursor: pointer;
    z-index: 9999; align-items: center; justify-content: center;
    font-size: 1rem; opacity: .7; transition: opacity .2s, transform .2s;
  }
  #theme-cycle-btn:hover { opacity: 1; transform: scale(1.1); }
  @media (pointer: coarse) { #theme-cycle-btn { display: flex; } #theme-hint { display: none; } }
</style>
<div id="theme-toast"></div>
<div id="theme-hint">Tab → style</div>
<button id="theme-cycle-btn" aria-label="Cycle theme">◐</button>
<script>
(function(){
  var T=[
    {n:'Warm',     v:{'--cream':'#F7F5F0','--warm':'#EDEAD3','--tan':'#B08A5C','--tan-light':'#CDB08A','--ink':'#18170F','--mid':'#6B6659','--linen':'#E3DDD2','--white':'#FDFCFA'}},
    {n:'Noir',     v:{'--cream':'#0A0A0A','--warm':'#141414','--tan':'#CC3333','--tan-light':'#E05050','--ink':'#EFEFEF','--mid':'#999999','--linen':'#222222','--white':'#1A1A1A'}},
    {n:'Ocean',    v:{'--cream':'#0D1B2A','--warm':'#1B2A3B','--tan':'#4ECDC4','--tan-light':'#7DDBD6','--ink':'#E8F4F8','--mid':'#8FB8C8','--linen':'#1A2E40','--white':'#162333'}},
    {n:'Forest',   v:{'--cream':'#0F1A0F','--warm':'#1A2A1A','--tan':'#4CAF50','--tan-light':'#7BC97E','--ink':'#E8F5E9','--mid':'#81B882','--linen':'#1E301E','--white':'#141F14'}},
    {n:'Neon',     v:{'--cream':'#030A03','--warm':'#071207','--tan':'#00FF41','--tan-light':'#39FF14','--ink':'#CCFFCC','--mid':'#00BB30','--linen':'#0A1A0A','--white':'#050E05'}},
    {n:'Rose',     v:{'--cream':'#FDF0F0','--warm':'#F9E5E5','--tan':'#C06080','--tan-light':'#D88090','--ink':'#2A1020','--mid':'#886070','--linen':'#EDD8D8','--white':'#FEF7F7'}},
    {n:'Slate',    v:{'--cream':'#1A1F2E','--warm':'#252B3B','--tan':'#7C9CBF','--tan-light':'#A0B8D0','--ink':'#E4E8F0','--mid':'#8090A8','--linen':'#2A3040','--white':'#202535'}},
    {n:'Desert',   v:{'--cream':'#FAF0E6','--warm':'#F5E6D3','--tan':'#C45E3C','--tan-light':'#D87D5F','--ink':'#1A0F08','--mid':'#7A5040','--linen':'#E8D8C4','--white':'#FBF5EE'}},
    {n:'Midnight', v:{'--cream':'#0A0D1A','--warm':'#121627','--tan':'#D4AF37','--tan-light':'#E8CB6A','--ink':'#EEF0F8','--mid':'#8890B0','--linen':'#181D30','--white':'#0E1220'}},
    {n:'Mint',     v:{'--cream':'#F0FAF6','--warm':'#E0F4ED','--tan':'#2EB87E','--tan-light':'#5CCFA0','--ink':'#0A2018','--mid':'#407060','--linen':'#D0EDE0','--white':'#F5FBF8'}},
    {n:'Mono',     v:{'--cream':'#FFFFFF','--warm':'#F5F5F5','--tan':'#111111','--tan-light':'#444444','--ink':'#111111','--mid':'#555555','--linen':'#E0E0E0','--white':'#FFFFFF'}},
    {n:'Sepia',    v:{'--cream':'#F4ECD8','--warm':'#EEE0C4','--tan':'#7A5C2E','--tan-light':'#9E7D4A','--ink':'#1C1006','--mid':'#6E5A3A','--linen':'#E8D8B8','--white':'#F8F2E0'}},
    {n:'Ember',    v:{'--cream':'#0D0905','--warm':'#1A1208','--tan':'#FF8C00','--tan-light':'#FFA830','--ink':'#FFF3E0','--mid':'#C0902A','--linen':'#1A1308','--white':'#100B06'}},
    {n:'Lavender', v:{'--cream':'#F5F0FF','--warm':'#EDE6FF','--tan':'#8B5CF6','--tan-light':'#A78BFA','--ink':'#1A0A2E','--mid':'#6B5080','--linen':'#DDD4F5','--white':'#F9F6FF'}},
    {n:'Dusk',     v:{'--cream':'#1A1520','--warm':'#231D2E','--tan':'#C084FC','--tan-light':'#D8A0FF','--ink':'#F0EAF8','--mid':'#8870A0','--linen':'#281E36','--white':'#1E1828'}},
    {n:'Arctic',   v:{'--cream':'#F0F8FF','--warm':'#E6F2FB','--tan':'#0077B6','--tan-light':'#0096CC','--ink':'#001428','--mid':'#4A6A8A','--linen':'#D8EAF5','--white':'#F5FBFF'}}
  ];
  var cur = parseInt(localStorage.getItem('jc-theme')||'0',10);
  if(isNaN(cur)||cur<0||cur>=T.length) cur=0;
  function apply(i){
    var r=document.documentElement,t=T[i];
    for(var k in t.v) r.style.setProperty(k,t.v[k]);
  }
  function toast(name){
    var el=document.getElementById('theme-toast');
    if(!el)return;
    el.textContent=name;
    el.classList.add('visible');
    clearTimeout(el._t);
    el._t=setTimeout(function(){el.classList.remove('visible');},2000);
  }
  function next(){
    cur=(cur+1)%T.length;
    localStorage.setItem('jc-theme',cur);
    apply(cur);
    toast(T[cur].n);
  }
  apply(cur);
  document.addEventListener('keydown',function(e){
    if(e.key!=='Tab')return;
    var tag=document.activeElement&&document.activeElement.tagName;
    if(tag==='INPUT'||tag==='TEXTAREA'||tag==='SELECT')return;
    e.preventDefault();
    next();
  });
  var btn=document.getElementById('theme-cycle-btn');
  if(btn) btn.addEventListener('click',next);
})();
</script>
'''

html_files = [
    'anternet.html',
    'index.html',
    'lab.html',
    'now.html',
    'projects.html',
    'signal.html',
]

base = '/Users/admin1/.openclaw/workspace/jasoncerf-site'

for fname in html_files:
    path = os.path.join(base, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already injected
    if 'theme-toast' in content:
        print(f'SKIP {fname} (already has theme switcher)')
        continue
    
    # Inject before </body>
    new_content = content.replace('</body>', THEME_BLOCK + '</body>', 1)
    
    if new_content == content:
        print(f'WARNING: No </body> found in {fname}')
        continue
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f'OK {fname}')

print('Done.')
