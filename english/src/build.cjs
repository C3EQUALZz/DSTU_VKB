const pptxgen = require('pptxgenjs');
const D = require('docx');
const fs = require('fs');
const path = require('path');
const C = require('./content.json');
const root=path.resolve(__dirname,'..'), out=path.join(root,'output');
fs.mkdirSync(out,{recursive:true});
const p = new pptxgen(); p.layout='LAYOUT_WIDE';
p.author=C.author; p.subject='RAG, GraphRAG and Agentic RAG for static code analysis in CI';
p.title=C.title; p.company=''; p.lang='en-GB';
p.theme={headFontFace:'Arial',bodyFontFace:'Arial',lang:'en-GB'};
const S=p.ShapeType, K={bg:'0B1220',panel:'142035',white:'F7FAFC',muted:'B9C6D8',cyan:'39D0D8',blue:'6F91E8',amber:'F5C76A',line:'3C506D'};
const manifest=[]; let current; let serial=0;
function name(group,label='object') {
 const n=`s${current.number}_${group?'g'+group:'static'}_${++serial}_${label}`;
 if(group){(current.groups[group]??=[]).push(n);} return n;
}
function text(s,t,x,y,w,h,size=22,opts={}){
 const {group,...rest}=opts; const n=name(group,'text');
 s.addText(t,{x,y,w,h,fontFace:'Arial',fontSize:size,color:K.white,margin:0,breakLine:false,vertAlign:'mid',valign:'mid',paraSpaceAfter:0,objectName:n,...rest});
 current.boxes.push({n,x,y,w,h,fontSize:size,fontFace:rest.fontFace||'Arial',bold:!!rest.bold,text:typeof t==='string'?t:t.map(x=>x.text).join('')}); return n;
}
function box(s,x,y,w,h,{group,fill=K.panel,line=fill,radius=true,...rest}={}){
 const n=name(group,'box');s.addShape(radius?S.roundRect:S.rect,{x,y,w,h,rectRadius:0.12,radius:0.12,fill:{color:fill},line:{color:line,width:1},objectName:n,...rest});return n;
}
function line(s,x1,y1,x2,y2,group,color=K.line,arrow=true){
 const n=name(group,'link'); const o={x:Math.min(x1,x2),y:Math.min(y1,y2),w:Math.abs(x2-x1),h:Math.abs(y2-y1),flipH:x2<x1,flipV:y2<y1,line:{color,width:1.6,...(arrow?{endArrowType:'triangle'}:{})},objectName:n}; s.addShape(S.line,o);return n;
}
function node(s,label,x,y,w=2.2,h=0.9,group,color=K.cyan){box(s,x,y,w,h,{group,line:color});text(s,label,x+.15,y+.1,w-.3,h-.2,18,{group,bold:true,align:'center'});}
function footer(s,n,source=''){
 text(s,'RAG for Secure Code',.65,7.08,3.0,.18,10.5,{color:K.muted});
 if(source)text(s,source,3.4,7.06,8.5,.26,10.5,{color:K.muted,align:'right'});
 text(s,String(n).padStart(2,'0')+' / 12',12.0,7.06,.67,.26,10.5,{color:K.muted,align:'right'});
}
function slide(n,title,section,source=''){
 current={number:n,groups:{},boxes:[]};manifest.push(current); const s=p.addSlide();s.background={color:K.bg};
 text(s,section,.65,.48,11,.25,13,{color:K.cyan});
 if(title)text(s,title,.65,1.05,12.0,1.05,title.length>44?32:36,{bold:true,breakLine:false});
 footer(s,n,source);const c=C.slides[n-1];s.addNotes(`${c.en}\n\nРусский перевод\n${c.ru}\n\nПоказ: ${c.cue}\n\nSources\n${c.sources.map(k=>C.sources[k].title+'\n'+C.sources[k].url).join('\n\n')}`);return s;
}
function image(s,file,x,y,w,h,group){const n=name(group,'screenshot');s.addImage({path:path.join(root,'assets',file),...p.constructor.imageSizingContain?.(file,x,y,w,h),x,y,w,h,objectName:n});return n;}
function fitImage(s,file,x,y,w,h,group){const n=name(group,'screenshot');const full=path.join(root,'assets',file);const b=fs.readFileSync(full),iw=b.readUInt32BE(16),ih=b.readUInt32BE(20),scale=Math.min(w/iw,h/ih);s.addImage({path:full,x:x+(w-iw*scale)/2,y:y+(h-ih*scale)/2,w:iw*scale,h:ih*scale,objectName:n});return n;}
function code(s,lines,x,y,w,h,{group,label='Illustrative pseudocode',size=17}={}){
 box(s,x,y,w,h,{group,fill:'101A2A',line:'314560'});
 text(s,label,x+.22,y+.14,w-.44,.3,12,{group,color:K.muted});
 lines.forEach((l,i)=>text(s,l,x+.23,y+.64+i*.33,w-.46,.32,size,{group,fontFace:'Courier New',color:/^(from|def|for|if|@)/.test(l)?K.cyan:K.white,breakLine:false}));
}
function chart(s,labels,values,x,y,w,h,group,{max=100,format='0',color=K.cyan,axisTitle}={}){
 const n=name(group,'chart');s.addChart(p.ChartType.bar,[{name:'Result',labels,values}],{
  x,y,w,h,barDir:'col',grouping:'clustered',showLegend:false,showTitle:false,
  chartColors:[color],varyColors:true,showValue:true,dataLabelPosition:'outEnd',dataLabelFormatCode:format,
  dataLabelColor:K.white,dataLabelBkgrdColor:K.bg,dataLabelFormatCodeSourceLinked:false,dataLabelFontSize:22,
  catAxisLabelColor:K.white,catAxisLabelFontSize:16,valAxisLabelColor:K.muted,valAxisLabelFontSize:13,
  valAxisMinVal:0,valAxisMaxVal:max,valAxisMajorUnit:max/4,
  catAxisLineColor:K.line,valAxisLineColor:K.line,valGridLine:{color:'273A52',width:1},catGridLine:{style:'none'},
  showCatName:false,showBorder:false,showCatName:false,showSerName:false,showValue:true,
  chartArea:{fill:{color:K.bg},border:{color:K.bg,transparency:100}},plotArea:{fill:{color:K.bg},border:{color:K.bg,transparency:100}},
  showValue:false,showTitle:false,showLegend:false,showCatName:false,
  showValue:true,objectName:n,
 });
 if(axisTitle)text(s,axisTitle,x+.05,y-.35,w,.3,14,{color:K.muted,group});
}

// 1 — cover. The graphic is part of the topic, not background decoration.
{
const s=slide(1,'','Cybersecurity / Continuous integration');
text(s,`${C.author}  ·  Group ${C.group}`,.7,.96,6.9,.3,17,{color:K.muted});
text(s,'RAG for\nSecure Code',.65,1.45,6.9,2.2,54,{bold:true,breakLine:false});
text(s,C.subtitle,.7,3.95,6.3,.65,25,{color:K.muted});
text(s,'Retrieval. Graphs. Agents.',.7,5.17,6.0,.5,23,{color:K.cyan});
text(s,'How can external knowledge support\nvulnerability detection in CI?',.7,5.92,6.1,.7,19,{color:K.muted});
node(s,'Source code',8.0,1.9,3.3,1,1,K.blue);node(s,'Security knowledge',8.0,3.45,3.3,1,1,K.cyan);node(s,'Evidence-based review',8.0,5,3.3,1,1,K.amber);
line(s,9.65,2.9,9.65,3.45,1);line(s,9.65,4.45,9.65,5,1);
}
// 2 — actual contents, visibly sequential.
{
const s=slide(2,'Contents','Presentation route');
const items=[['The problem','Why security knowledge matters'],['The pipeline','RAG inside my CI module'],['The evidence','What Vul-RAG research reports'],['Architecture','GraphRAG, Agentic RAG, AG2 and FastMCP'],['The value','Costs, evaluation and conclusions']];
line(s,1.04,2.42,1.04,6.37,null,K.line,false);
items.forEach(([a,b],i)=>{const y=2.2+i*.87;s.addShape(S.ellipse,{x:.86,y:y+.08,w:.36,h:.36,fill:{color:K.cyan},line:{color:K.cyan},objectName:name(null,'step')});text(s,String(i+1),.86,y+.08,.36,.36,13,{color:K.bg,bold:true,align:'center'});text(s,a,1.58,y,4.1,.42,25,{bold:true});text(s,b,6.15,y+.03,6.35,.45,20,{color:K.muted});});
}
// 3 — real English screenshot and precise terminology.
{
const s=slide(3,'Why AI Code Review Needs Security Knowledge','Problem and relevance','Sources: OWASP Top 10; MITRE CWE-89');
text(s,'Code alone may hide the security context.',.7,2.12,11.8,.45,25,{color:K.cyan});
box(s,.7,2.94,7.4,3.65,{fill:'FFFFFF',radius:false});text(s,'CWE-89 · SQL injection',1.0,3.18,6.8,.4,23,{color:'183D62',bold:true});fitImage(s,'cwe89.png',1.0,3.83,6.8,2.4);
[['OWASP','Guidance and risk categories'],['CWE','Types of software weaknesses'],['CVE','Specific disclosed vulnerabilities']].forEach(([a,b],i)=>{text(s,a,8.55,3.05+i*1.03,3.7,.35,23,{bold:true});text(s,b,8.55,3.47+i*1.03,3.75,.52,17,{color:K.muted});});
text(s,'Use external knowledge to improve code review.',.75,6.65,11.8,.3,18,{color:K.cyan});
}
// 4 — distinction between offline preparation and query-time analysis.
{
const s=slide(4,'How a Basic RAG Pipeline Works','Method','Sources: Lewis et al., 2020; Anthropic, 2024');
text(s,'Prepare the knowledge base',.7,2.15,5.7,.4,23,{bold:true,group:1});
['Documents','Passages','Search index'].forEach((t,i)=>{node(s,t,.7+i*2.02,2.88,1.75,.86,1,i===2?K.cyan:K.blue);if(i<2)line(s,2.45+i*2.02,3.31,2.72+i*2.02,3.31,1);});
text(s,'Analyze the code',.7,4.1,5.8,.4,23,{bold:true,group:2});
node(s,'Code + task',.7,4.85,1.75,.86,2,K.blue);node(s,'Retrieve',2.72,4.85,1.75,.86,2);node(s,'AI review',4.74,4.85,1.75,.86,3,K.amber);
line(s,2.45,5.28,2.72,5.28,2);line(s,4.47,5.28,4.74,5.28,3);line(s,5.61,3.74,5.61,4.05,2,K.cyan,false);line(s,5.61,4.05,3.6,4.05,2,K.cyan,false);line(s,3.6,4.05,3.6,4.85,2,K.cyan);
text(s,'The retriever finds relevant passages.',.75,6.06,5.9,.35,17,{color:K.muted});
text(s,'Relevant passages are added to the prompt.',.75,6.48,6.1,.35,17,{color:K.muted});
code(s,['code = select_code()','query = describe_task(code)','evidence = retrieve(query)','finding = assess(code, evidence)','record(finding)'],7.1,2.5,5.5,3.15,{group:4,size:17});
text(s,'Update documents separately from the model.',7.15,6.04,5.2,.78,20,{color:K.cyan,group:4});
}
// 5 — project facts, no invented provider or implementation metrics.
{
const s=slide(5,'My CI Security Module','Project experience','High-level project account; workflow simplified for explanation');
text(s,'I developed a CI module for AI-assisted static analysis.',.7,2.13,11.9,.58,25,{color:K.cyan});
const nodes=[['Codebase',.7,1,K.blue],['Knowledge retrieval',3.1,2,K.cyan],['AI analysis',6.2,3,K.blue],['Findings',9.45,4,K.amber]];
nodes.forEach(([label,x,g,col],i)=>{node(s,label,x,3.35,i===1?2.65:2.1,1.05,g,col);if(i>0){const prev=nodes[i-1];line(s,prev[1]+(i===2?2.65:2.1),3.87,x,3.87,g);}});
box(s,3.1,4.76,3.0,1.03,{group:2});text(s,'RAG + GraphRAG',3.3,4.94,2.6,.3,19,{group:2,bold:true});text(s,'Security knowledge',3.3,5.32,2.6,.25,15,{group:2,color:K.muted});
line(s,4.43,4.76,4.43,4.4,2,K.cyan);
box(s,6.45,4.76,5.45,1.03,{group:3});text(s,'Agentic RAG  /  AG2  /  FastMCP',6.65,4.96,5.0,.3,19,{group:3,bold:true});text(s,'Agent orchestration and tool access',6.65,5.34,5.0,.25,15,{group:3,color:K.muted});
line(s,7.25,4.76,7.25,4.4,3,K.blue);
text(s,'Knowledge collected from OWASP supports code analysis.',.75,6.3,11.8,.45,21,{color:K.muted});
}
// 6 — native editable evidence chart.
{
const s=slide(6,'Research Evidence: Vul-RAG','Published research','Du et al., Vul-RAG, arXiv v3 (2025), Tables 1 and 4');
text(s,'GPT-4o on PairVul',.75,2.17,6,.4,24,{bold:true});
chart(s,['Basic prompt','Vul-RAG'],[8,32],.72,3.05,6.5,3.35,1,{max:40,format:'0"%"',axisTitle:'Pair accuracy (%) · higher is better'});
text(s,'+24',8.02,2.67,3.9,1.03,64,{color:K.cyan,bold:true,group:1});
text(s,'percentage points',8.07,3.78,4.1,.42,22,{group:1});
text(s,'Both versions must be\nclassified correctly:\nvulnerable and patched.',8.05,4.5,4.35,1.35,21,{color:K.muted});
text(s,'586 function pairs · external benchmark',.95,6.54,11.6,.3,17,{color:K.muted});
}
// 7 — native explanatory graph + actual documentation screenshot.
{
const s=slide(7,'GraphRAG: Connecting Related Facts','Architecture','Source: Microsoft GraphRAG documentation; left graph is illustrative');
text(s,'Retrieve relationships as well as passages.',.7,2.13,11.8,.45,24,{color:K.cyan});
const n=[['Code element',.85,3.15,2.15,K.blue],['Weakness',3.7,3.15,2.15,K.cyan],['Guidance',3.7,5.13,2.15,K.amber],['Related context',.85,5.13,2.15,K.blue]];
[[0,1],[1,2],[0,3],[3,2]].forEach(([a,b])=>line(s,n[a][1]+1.08,n[a][2]+.42,n[b][1]+1.08,n[b][2]+.42,2));
n.forEach(([label,x,y,w,c])=>node(s,label,x,y,w,.85,1,c));
text(s,'Illustrative security-knowledge graph',.85,6.38,5.3,.35,15,{color:K.muted});
box(s,7.05,2.99,5.5,3.67,{fill:'FFFFFF',radius:false});fitImage(s,'graphrag-docs.png',7.13,3.07,5.34,3.51);
text(s,'Microsoft GraphRAG: an external example',7.08,6.7,5.4,.23,13,{color:K.muted});
}
// 8 — agent loop + genuine minimal API example (not a fabricated full SDK).
{
const s=slide(8,'Agentic Analysis with AG2 and FastMCP','Implementation roles','Sources: AG2; FastMCP Quickstart; LangGraph Agentic RAG');
node(s,'AG2 agents',.75,2.8,2.25,.88,1,K.blue);node(s,'FastMCP tools',3.85,2.8,2.25,.88,2,K.cyan);line(s,3,3.24,3.85,3.24,2);
node(s,'Assess evidence',3.85,4.57,2.25,.88,3,K.amber);node(s,'More context?',.75,4.57,2.25,.88,3,K.blue);line(s,4.98,3.68,4.98,4.57,3);line(s,3.85,5.01,3,5.01,3);line(s,1.88,4.57,1.88,3.68,3);
text(s,'Bound the number of steps.\nDefine a stopping condition.',.8,6.1,5.6,.65,21,{color:K.cyan});
code(s,['from fastmcp import FastMCP','mcp = FastMCP("Security")','GUIDE = {"CWE-89": "Parameterize SQL."}','@mcp.tool','def lookup(cwe: str) -> str:','    return GUIDE.get(cwe, "Not found")'],6.78,2.65,5.8,3.48,{group:4,label:'Minimal FastMCP tool example',size:15});
text(s,'This tool is one component of a RAG system.',6.85,6.35,5.6,.5,17,{color:K.muted});
}
// 9 — native editable comparison table.
{
const s=slide(9,'Which Approach Fits the Task?','Comparison','Sources: Microsoft GraphRAG; LangGraph retrieval documentation');
const rows=[
 [{text:'Approach',options:{bold:true}},{text:'Useful when…',options:{bold:true}},{text:'Additional work',options:{bold:true}}],
 ['Basic RAG','A few passages contain the answer.','Indexing and retrieval'],
 ['GraphRAG','Facts are connected across sources.','Graph construction and updates'],
 ['Agentic RAG','The next search depends on earlier results.','More decisions and tool calls']
];
s.addTable(rows,{x:.75,y:2.48,w:11.83,h:3.38,colW:[2.45,5.25,4.13],rowH:[.65,.91,.91,.91],fontFace:'Arial',fontSize:20,color:K.white,fill:K.panel,border:{type:'solid',pt:1,color:K.bg},margin:.18,breakLine:false,autoPage:false,verbose:false,
 bold:false,
});
// Header is deliberately separate for a clear table hierarchy.
box(s,.75,2.48,11.83,.68,{fill:'20334C',radius:false});
text(s,'Approach',.95,2.65,2.1,.3,20,{bold:true,color:K.cyan});text(s,'Useful when…',3.4,2.65,4.8,.3,20,{bold:true,color:K.cyan});text(s,'Additional work',8.65,2.65,3.6,.3,20,{bold:true,color:K.cyan});
text(s,'These approaches can be combined.',.8,6.23,11.7,.5,26,{color:K.cyan});
}
// 10 — second native chart, accurate and scoped.
{
const s=slide(10,'When Does RAG Save Money?','Value and cost','Microsoft Research, Dynamic community selection (2024)');
text(s,'Select evidence. Control model calls.',.7,2.13,11.7,.45,24,{color:K.cyan});
chart(s,['Static search','Dynamic search'],[100,23],.75,3.12,6.3,3.15,1,{max:120,axisTitle:'Relative token cost · static search = 100'});
text(s,'77% lower',7.65,2.99,4.8,.7,37,{bold:true,color:K.cyan,group:1});
text(s,'Reported average token cost\n50 AP News questions\nGraphRAG global search, level 1',7.7,3.94,4.6,1.2,19,{color:K.muted,group:1});
text(s,'Total cost also includes indexing,\nretrieval, maintenance and review.',7.7,5.52,4.7,.9,20,{color:K.amber});
text(s,'Experimental comparison; not measured savings for my CI module.',.95,6.55,11.5,.3,16,{color:K.muted});
}
// 11 — concise evaluation, explicit required grammar.
{
const s=slide(11,'Evaluating an AI-Assisted Scanner','Limits and evaluation','Sources: Vul-RAG; OWASP LLM01:2025');
[['Precision','Are reported findings correct?'],['Recall','Are known problems detected?'],['Evidence','Do sources support the finding?'],['Cost and time','Is the workflow practical in CI?']].forEach(([a,b],i)=>{const x=.75+(i%2)*6.1,y=2.5+Math.floor(i/2)*1.38;box(s,x,y,5.65,1.07);text(s,a,x+.2,y+.15,5.2,.3,22,{bold:true,color:K.cyan});text(s,b,x+.2,y+.57,5.2,.3,18,{color:K.muted});});
text(s,'Retrieving evidence is only the first step.',.8,5.57,11.6,.4,23,{color:K.amber});
text(s,'We expect the scanner to support each finding with evidence.',.8,6.22,11.6,.5,23,{group:1,bold:true});
}
// 12 — conclusion, not a full bibliography disguised as a tiny slide.
{
const s=slide(12,'Conclusions','Research question answered');
const a=[['Retrieve evidence','Security knowledge gives the model useful context.'],['Connect context','Graphs and agents support broader analysis.'],['Measure the value','Validate findings, runtime and total cost.']];
a.forEach(([h,b],i)=>{const y=2.24+i*1.09;text(s,h,.8,y,4.7,.45,29,{bold:true,color:K.cyan});text(s,b,5.6,y+.05,6.8,.5,21,{color:K.muted});});
text(s,'Better retrieval. Clearer context. Reviewable findings.',.8,5.94,11.7,.55,28,{bold:true});
text(s,'Selected sources: Lewis et al. (2020) · Vul-RAG v3 (2025) · Microsoft GraphRAG\nAG2 and FastMCP documentation · Full references in the speaking notes',.8,6.64,11.5,.37,12,{color:K.muted});
}

async function buildDocx(){
const {Document,Paragraph,TextRun,HeadingLevel,AlignmentType,Footer,Header,PageNumber,PageBreak,Table,TableRow,TableCell,WidthType,ShadingType,ExternalHyperlink}=D;
const children=[];
function para(t,opts={}){return new Paragraph({children:[new TextRun({text:t,font:'Arial',size:22,...opts.run})],spacing:{after:120,line:270},...opts});}
function label(t){return para(t,{spacing:{before:180,after:90},run:{bold:true,color:'183D62',size:22}});}
function chunks(t){const a=t.match(/[^.!?]+[.!?]+(?:\s|$)|[^.!?]+$/g)||[t];const k=Math.ceil(a.length/2);return[a.slice(0,k).join('').trim(),a.slice(k).join('').trim()].filter(Boolean);}
const total=C.slides.reduce((n,s)=>n+s.en.split(/\s+/).length,0);
C.slides.forEach((s,i)=>{
 children.push(new Paragraph({text:`${String(i+1).padStart(2,'0')}  ${s.title}`,heading:HeadingLevel.HEADING_1,pageBreakBefore:i>0,spacing:{after:180}}));
 if(i===0){children.push(para(C.subtitle,{run:{size:24,bold:true}}));children.push(para(`${C.author} · Group ${C.group} / ${C.authorRu} · группа ${C.groupRu}`,{run:{size:22,bold:true}}));children.push(para(`B2 • 12 slides • ${total} English words • about 10–12 minutes with pauses and slide builds`,{run:{size:19,color:'526070'}}));}
 children.push(label('English — speaking text'));
 chunks(s.en).forEach(t=>children.push(para(t,{run:{language:{value:'en-GB'}}})));
 children.push(label('Русский перевод'));
 chunks(s.ru).forEach(t=>children.push(para(t,{run:{language:{value:'ru-RU'},size:21}})));
 children.push(para(`Показ слайда: ${s.cue}`,{spacing:{before:160,after:90,line:245},run:{size:19,italics:true,color:'526070'}}));
});
children.push(new Paragraph({text:'Grammar checklist / Обязательная грамматика',heading:HeadingLevel.HEADING_1,pageBreakBefore:true}));
children.push(para('Все примеры ниже присутствуют в видимом английском тексте презентации. Слайды указаны по номеру.'));
C.grammar.forEach(g=>{children.push(new Paragraph({text:`${g.name} — Slide ${g.slide}`,heading:HeadingLevel.HEADING_2,spacing:{before:170,after:80}}));children.push(para(g.example,{run:{bold:true,size:22}}));children.push(para(g.ru,{run:{size:21}}));});
children.push(new Paragraph({text:'Glossary / Термины',heading:HeadingLevel.HEADING_1,pageBreakBefore:true}));
C.glossary.forEach(([a,b,c])=>{children.push(para(`${a} — ${b}`,{spacing:{before:100,after:40,line:250},run:{bold:true,size:21}}));children.push(para(c,{spacing:{after:100,line:245},run:{size:20}}));});
children.push(new Paragraph({text:'References / Источники',heading:HeadingLevel.HEADING_1,pageBreakBefore:true}));
children.push(para('Личный проект описан на основе сведений автора. Показатели Vul-RAG и Microsoft относятся к внешним исследованиям. Учебные схемы и примеры кода не являются исходниками личного проекта.',{run:{size:21}}));
Object.values(C.sources).forEach((s,i)=>{children.push(para(`${i+1}. ${s.title}`,{spacing:{before:130,after:50},run:{size:21,bold:true}}));children.push(new Paragraph({children:[new ExternalHyperlink({link:s.url,children:[new TextRun({text:s.url,style:'Hyperlink',size:18})]})],spacing:{after:100,line:235}}));});
children.push(new Paragraph({text:'How to present / Подготовка к выступлению',heading:HeadingLevel.HEADING_1,pageBreakBefore:true}));
[
'Открой PPTX в настольном Microsoft PowerPoint и запусти показ слайдов. Схемы раскрываются по клику; PDF показывает их итоговое статическое состояние.',
'Прочитай английский текст с секундомером. Ориентир — 115–130 слов в минуту с короткими паузами на схемы и графики. Точное число слов указано в начале документа.',
'На слайде 6 объясни, что pair accuracy оценивает сразу две функции. Рост 8% → 32% равен 24 процентным пунктам. Это не точность личного сканера.',
'На слайде 10 говори о стоимости токенов конкретного эксперимента Microsoft. Снижение на 77% не означает такую же экономию всего проекта.',
'Произношение: RAG — «рэг»; CI — «си-ай»; AG2 — «эй-джи-ту»; MCP — «эм-си-пи»; CWE — «си-дабл-ю-и». Для GraphRAG удобно говорить «граф-рэг».',
'Если спросят о результатах твоего проекта, опирайся на собственные реальные измерения и примеры. Графики презентации относятся к явно указанным публикациям.'
].forEach(t=>children.push(para(t)));
const doc=new Document({creator:C.author,title:C.title,description:'Bilingual speaking script and grammar checklist',styles:{default:{document:{run:{font:'Arial',size:22},paragraph:{spacing:{line:270,after:120}}}},paragraphStyles:[{id:'Heading1',name:'Heading 1',basedOn:'Normal',next:'Normal',quickFormat:true,run:{font:'Arial',size:36,bold:true,color:'142D48'},paragraph:{spacing:{before:0,after:180},keepNext:true}},{id:'Heading2',name:'Heading 2',basedOn:'Normal',next:'Normal',quickFormat:true,run:{font:'Arial',size:25,bold:true,color:'183D62'},paragraph:{keepNext:true}}]},sections:[{properties:{page:{size:{width:11906,height:16838},margin:{top:1000,bottom:1000,left:1050,right:1050}}},headers:{default:new Header({children:[new Paragraph({children:[new TextRun({text:'RAG for Secure Code  |  Speaking notes · EN / RU',size:17,color:'526070'})],spacing:{after:100}})]})},footers:{default:new Footer({children:[new Paragraph({alignment:AlignmentType.RIGHT,children:[new TextRun({text:'Page ',size:18,color:'526070'}),new TextRun({children:[PageNumber.CURRENT],size:18,color:'526070'})]})]})},children}]});
fs.writeFileSync(path.join(out,'RAG_Speaking_Notes_EN_RU.docx'),await D.Packer.toBuffer(doc));
}
(async()=>{
await p.writeFile({fileName:path.join(out,'RAG_for_Secure_Code_base_v4.pptx')});
fs.writeFileSync(path.join(out,'build-manifest.json'),JSON.stringify(manifest,null,2));
if(!process.argv.includes('--slides-only'))await buildDocx();
console.log('Built 12 slides and bilingual DOCX. English words:',C.slides.reduce((n,s)=>n+s.en.split(/\s+/).length,0));
})();
