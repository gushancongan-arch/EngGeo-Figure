"""Synthetic chart-type examples; no scientific claim."""
from pathlib import Path
import sys, shutil, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.transforms import Bbox

import argparse
import enggeo_style as g
parser=argparse.ArgumentParser()
parser.add_argument('--output',type=Path,default=Path('examples/generated'))
args=parser.parse_args()
O=args.output.resolve()
O.mkdir(parents=True,exist_ok=True)
g.apply_style()
f=plt.figure(figsize=(180/25.4,164/25.4))
axes=[f.add_axes([x/180,y/164,60/180,39/164]) for y in [116,62,10] for x in [15,103]]
colors=[g.PALETTE[k] for k in ['blue','orange','green','purple']]
names=['Group A','Group B','Group C','Group D']
counts=np.array([42,28,18,12])
for ax,ring in zip(axes[:2],[False,True]):
    ax.pie(counts,labels=[f'{n}\n{v}%' for n,v in zip(names,counts)],colors=colors,startangle=90,counterclock=False,
           labeldistance=1.38,wedgeprops={'linewidth':0.6,'edgecolor':'black',**({'width':0.40} if ring else {})},
           textprops={'fontsize':8,'color':'black'},radius=1)
    ax.set_aspect('equal',adjustable='datalim')
    ax.set_xlim(-1.95,1.95);ax.set_ylim(-1.27,1.27)

for ax in axes[2:]:g.style_boxed_axes(ax)
a=axes[2]
a.barh(names,counts,color=colors,edgecolor='black',linewidth=.6,height=.62)
a.invert_yaxis();a.set(xlim=(0,50),xlabel='Number of events')
for i,v in enumerate(counts):a.text(v+1,i,str(v),va='center')

rng=np.random.default_rng(123)
samples=[np.clip(rng.normal(mu,sd,18),0,None) for mu,sd in [(8,2),(13,3),(18,3.2),(23,4)]]
a=axes[3]
b=a.boxplot(samples,positions=np.arange(1,5),widths=.56,patch_artist=True,showfliers=False,
    medianprops={'color':'black','linewidth':1.1},boxprops={'linewidth':.75},whiskerprops={'linewidth':.75},capprops={'linewidth':.75})
for i,(patch,vals,col) in enumerate(zip(b['boxes'],samples,colors)):
    patch.set_facecolor(g.marker_fill_color(col,.78))
    a.scatter(i+1+rng.uniform(-.15,.15,len(vals)),vals,zorder=3,**g.marker_style(col,kind='scatter',size_pt=4,marker=g.MARKERS[i]))
a.set(xticks=[1,2,3,4],xticklabels=['A','B','C','D'],xlabel='Group',ylabel='Displacement (mm)',ylim=(0,34))

a=axes[4]
x=np.linspace(10,90,14)
ys=[]
for i in range(2):
    y=2+.14*x+3*i+rng.normal(0,1.2,len(x));ys.append(y)
    a.scatter(x,y,label=names[i],**g.marker_style(colors[i],kind='scatter',marker=g.MARKERS[i]))
a.set(xlabel='Rainfall (mm)',ylabel='Displacement (mm)',xlim=(0,100),ylim=(0,24))
a.legend(loc='upper left',handletextpad=.4)

heat=np.array([[2,3,5,7,5,3],[1,4,6,9,7,4],[3,5,8,12,9,6],[2,4,7,10,8,5]])
a=axes[5]
cmap=LinearSegmentedColormap.from_list('deepblue_seq',['#F2F6FC','#729BC9','#003F88'])
mesh=a.pcolormesh(np.arange(7),np.arange(5),heat,cmap=cmap,vmin=0,vmax=12,edgecolors='white',linewidth=.5)
a.set(xticks=np.arange(6)+.5,xticklabels=['Jan','Feb','Mar','Apr','May','Jun'],yticks=np.arange(4)+.5,yticklabels=['S1','S2','S3','S4'],xlabel='Month',ylabel='Site',ylim=(4,0))
for r in range(4):
    for c in range(6):a.text(c+.5,r+.5,str(heat[r,c]),ha='center',va='center',color='white' if heat[r,c]>=8 else 'black')
cax=f.add_axes([166/180,10/164,2.4/180,39/164])
cb=f.colorbar(mesh,cax=cax,ticks=[0,6,12]);cb.set_label('Event count');cb.ax.tick_params(direction='out',length=2,pad=2)
g.add_panel_labels(axes)
f.canvas.draw()
def bounds(i):
    renderer=f.canvas.get_renderer()
    members=[axes[i]]+([cax] if i==5 else [])
    return Bbox.union([a.get_tightbbox(renderer) for a in members])
def move(ax, dx=0, dy=0):
    p=ax.get_position()
    ax.set_position([p.x0+dx/f.bbox.width,p.y0+dy/f.bbox.height,p.width,p.height])
target=2.5*f.dpi/25.4
before=[(bounds(i+1).x0-bounds(i).x1)*25.4/f.dpi for i in [0,2,4]]
# Each row is a separate chart-family pair: preserve row alignment, but avoid
# imposing empty Cartesian plot-box widths on circular-chart content.
for i in [0,2,4]:
    dx=target-(bounds(i+1).x0-bounds(i).x1)
    move(axes[i+1],dx=dx)
    if i==4:move(cax,dx=dx)
    f.canvas.draw()
for row in [1,0]:
    upper=Bbox.union([bounds(2*row),bounds(2*row+1)])
    lower=Bbox.union([bounds(2*row+2),bounds(2*row+3)])
    dy=target-(upper.y0-lower.y1)
    for i in [2*row,2*row+1]:move(axes[i],dy=dy)
    f.canvas.draw()
# Resize the physical canvas to the measured artwork; keep font and plot sizes.
union=Bbox.union([bounds(i) for i in range(6)])
pad=1.5*f.dpi/25.4
positions=[a.get_window_extent().frozen() for a in f.axes]
width,height=union.width+2*pad,union.height+2*pad
f.set_size_inches(width/f.dpi,height/f.dpi)
for a,p in zip(f.axes,positions):
    a.set_position([(p.x0-union.x0+pad)/width,(p.y0-union.y0+pad)/height,p.width/width,p.height/height])
f.canvas.draw()
horizontal=[(bounds(i+1).x0-bounds(i).x1)*25.4/f.dpi for i in [0,2,4]]
vertical=[(min(bounds(2*r).y0,bounds(2*r+1).y0)-max(bounds(2*r+2).y1,bounds(2*r+3).y1))*25.4/f.dpi for r in [0,1]]
assert all(abs(v-2.5)<.1 for v in horizontal+vertical),(horizontal,vertical)
g.audit_content_spacing(f,[[a] for a in axes],[(0,1,'horizontal'),(2,3,'horizontal'),(4,5,'horizontal')],json_out=O/'horizontal_spacing.json')
g.audit_content_spacing(f,[[axes[0],axes[1]],[axes[2],axes[3]],[axes[4],axes[5],cax]],[(0,1,'vertical'),(1,2,'vertical')],json_out=O/'vertical_spacing.json')
g.audit_panel_alignment(f,axes,groups=[{'panels':[i,i+1],'checks':['top','bottom','width','height']} for i in [0,2,4]],json_out=O/'alignment.json')
f.savefig(O/'Chart_types_compact_EN.svg')
(O/'spacing_QA.json').write_text(json.dumps({'initial_horizontal_mm':before,'horizontal_mm':horizontal,'vertical_mm':vertical,'canvas_mm':(f.get_size_inches()*25.4).tolist(),'outer_padding_mm':1.5},indent=2),encoding='utf-8')
(O/'synthetic_source_data.json').write_text(json.dumps({'groups':names,'counts':counts.tolist(),'boxplot_samples':[v.tolist() for v in samples],'scatter_rainfall':x.tolist(),'scatter_displacements':[v.tolist() for v in ys],'heatmap':heat.tolist()},indent=2),encoding='utf-8')
(O/'NOTES.md').write_text('''# Chart-type demonstration (synthetic data only)

Six panels, three rows by two columns, with a content-sized canvas. No scientific claim is made. Adjacent row-pair content bounds have 2.5 mm horizontal and vertical clearance. Mixed chart families use explicit within-row alignment rather than fixed column positions. Font and plot physical sizes are preserved.
a: Pie chart; b: donut chart. Both use the same four-category counts (42, 28, 18, 12; total 100) to compare styles, not independent evidence.
c: Horizontal bars show those exact illustrative counts, without invented uncertainty.
d: Box plots show 18 synthetic samples per group, median, quartiles and whiskers to the most extreme points within 1.5 IQR. All observations are overlaid, including any beyond whiskers. Jitter is horizontal only.
e: Synthetic paired rainfall and displacement observations for two groups, no fitted line or causal claim.
f: Synthetic site-by-month event counts. Sequential colours encode magnitude; exact values are annotated. White text on dark cells is used for contrast.
Group colours are consistent across panels. Pie/donut charts have no meaningless Cartesian axes. All Cartesian ticks point outwards. Black marker edges, tinted marker fills, DejaVu Sans then Arial, no titles or footer. Only SVG exported; source data and plotting code retained.
''',encoding='utf-8')
print('SVG exported; six-panel alignment passed.')

