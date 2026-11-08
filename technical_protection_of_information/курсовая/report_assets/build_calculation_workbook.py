# -*- coding: utf-8 -*-
"""Excel OOXML с проверяемыми формулами и сохранёнными результатами вычисления."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.etree import ElementTree as X
import json
import math
import sys

B=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(B/'analysis'))
from calculate_variant99 import intelligibility
D=json.loads((B/'analysis/variant99_calculations.json').read_text())
M='http://schemas.openxmlformats.org/spreadsheetml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
P='http://schemas.openxmlformats.org/package/2006/relationships'
X.register_namespace('',M)


def name(col):
    s=''
    while col:
        col,r=divmod(col-1,26)
        s=chr(65+r)+s
    return s


class Sheet:
    def __init__(self,title):
        self.title=title
        self.cells={}
    def put(self,row,col,val,formula=None,style=None):
        self.cells[(row,col)]=(val,formula,style if style is not None else (4 if isinstance(val,str) else 1))
    def header(self,labels,row=3):
        for c,v in enumerate(labels,1):self.put(row,c,v,style=3)
    def xml(self):
        root=X.Element('{'+M+'}worksheet')
        views=X.SubElement(root,'{'+M+'}sheetViews')
        view=X.SubElement(views,'{'+M+'}sheetView',workbookViewId='0',showGridLines='0')
        X.SubElement(view,'{'+M+'}pane',ySplit='3',topLeftCell='A4',activePane='bottomLeft',state='frozen')
        X.SubElement(root,'{'+M+'}sheetFormatPr',defaultRowHeight='22')
        cols=X.SubElement(root,'{'+M+'}cols')
        maxcol=max(c for r,c in self.cells)
        if self.title=='Описание':
            X.SubElement(cols,'{'+M+'}col',min='1',max='1',width='32',customWidth='1')
            X.SubElement(cols,'{'+M+'}col',min='2',max='2',width='110',customWidth='1')
        else:
            X.SubElement(cols,'{'+M+'}col',min='1',max=str(maxcol),width='18',customWidth='1')
        data=X.SubElement(root,'{'+M+'}sheetData')
        for row in sorted(set(r for r,c in self.cells)):
            e=X.SubElement(data,'{'+M+'}row',r=str(row))
            if row==3:e.set('ht','58');e.set('customHeight','1')
            elif self.title=='Описание':e.set('ht','42');e.set('customHeight','1')
            for col in sorted(c for r,c in self.cells if r==row):
                val,formula,style=self.cells[(row,col)]
                cell=X.SubElement(e,'{'+M+'}c',r=f'{name(col)}{row}',s=str(style))
                if isinstance(val,str) and formula is None:
                    cell.set('t','inlineStr')
                    X.SubElement(X.SubElement(cell,'{'+M+'}is'),'{'+M+'}t').text=val
                else:
                    if formula is not None:X.SubElement(cell,'{'+M+'}f').text=formula
                    X.SubElement(cell,'{'+M+'}v').text=str(val)
        X.SubElement(root,'{'+M+'}pageMargins',left='.3',right='.3',top='.5',bottom='.5',header='.2',footer='.2')
        return X.tostring(root,encoding='utf-8',xml_declaration=True)


def probability(q):
    a=(.78+5.46*math.exp(-.0043*(27.3-abs(q))**2))/(1+10**(.1*abs(q)))
    return a if q<=0 else 1-a


def pf(q):
    a=f'(0.78+5.46*EXP(-0.0043*(27.3-ABS({q}))^2))/(1+10^(0.1*ABS({q})))'
    return f'IF({q}<=0,{a},1-({a}))'


def wf(r):
    return f'IF({r}<0.15,1.54*{r}^0.25*(1-EXP(-11*{r})),1-EXP(-11*{r}/(1+0.7*{r})))'


sheets=[]
guide=Sheet('Описание');sheets.append(guide)
guide.header(['Расчёты для окончания зачётки 99','Пояснение'])
for row,items in enumerate([
    ['Варианты','П.1 — 2; П.2 — 1. Источник: задание КР, с.3.'],
    ['Синие числа','Исходные данные задания и явно принятые параметры.'],
    ['Остальные числа','Формулы Excel с сохранёнными результатами; при открытии включён пересчёт.'],
    ['Геометрия комнаты','В формулы W не входит. Высота3380мм и дверь1200×2228мм подтверждены пользователем.'],
    ['НЧ: слабый сигнал','ЛР3 с.11: при Uсш−Uш<1дБ Uс[дБ]=Uсш[дБ]−7дБ.'],
    ['НЧ: модель речи','С усилением по условию варианта; шумы — для цепи электропитания.'],
    ['Исходная сигнализация','По условию пожарной и охранной сигнализации нет. НЧ расчёт — оценка извещателя, рассматриваемого для проектируемой системы.'],
    ['ВЧ: расстояние R','Принято R=2Ra=0.50м; это условие расчётной модели, не измерение.'],
    ['ВЧ: коэффициент Kз','На листе ВЧ формула (D/R)^2; ветвь верна при λ/(2π)<R,D≤6λ.'],
    ['Наводки: частоты','КР:кГц; ЛР6 для тех же исходных данных:МГц. Единицы сохранены по заданию.'],
    ['Наводки: объект','Основной результат — отдельная клавиатура, без ветви +10дБ. Альтернативная ветвь тоже показана.'],
    ['Ограничение','Расчёт по учебным исходным данным; не протокол натурной аттестации аудитории.'],
],4):
    for col,v in enumerate(items,1):guide.put(row,col,v)

par=Sheet('Параметры');sheets.append(par)
par.header(['Октава,Гц','Lн без усил.,дБ','Lн с усил.,дБ','ΔA,дБ','kᵢ','Uш цепи питания,мкВ','ΔF,кГц'])
for i,row in enumerate(zip([250,500,1000,2000,4000],[66,66,61,56,53],[80,80,75,70,67],[18,14,9,6,5],[.03,.12,.2,.3,.26],[151,74,20.5,4.6,1],[.18,.355,.69,1.4,2.8]),4):
    for c,v in enumerate(row,1):par.put(i,c,v,style=2)
par.put(11,1,'Источник');par.put(11,2,'ЛР2 с.26–27; ЛР3 с.10,12; ЛР4 с.21–23')
summary=[]
for title,key in [('Акустика','acoustic'),('Виброакустика','vibration')]:
    s=Sheet(title);sheets.append(s)
    s.header(['f,Гц','Lтс,дБ','Lс+ш,дБ','Lш,дБ','Lн,дБ','Lс,дБ','ΔL,дБ','Lс.прив,дБ','E,дБ','ΔA,дБ','kᵢ','Qᵢ,дБ','pᵢ','Rᵢ=pᵢkᵢ'])
    for row,v in enumerate(D[key]['rows'],4):
        q=v['snr_dB']-[18,14,9,6,5][row-4];p=probability(q);k=[.03,.12,.2,.3,.26][row-4]
        vals=[v['frequency_Hz'],v['test_dB'],v['signal_noise_dB'],v['noise_dB'],v['normal_dB'],v['signal_dB'],v['correction_dB'],v['referred_dB'],v['snr_dB'],[18,14,9,6,5][row-4],k,q,p,p*k]
        forms={5:f"'Параметры'!B{row}",6:f'10*LOG10(10^(C{row}/10)-10^(D{row}/10))',7:f'B{row}-E{row}',8:f'F{row}-G{row}',9:f'H{row}-D{row}',10:f"'Параметры'!D{row}",11:f"'Параметры'!E{row}",12:f'I{row}-J{row}',13:pf(f'L{row}'),14:f'M{row}*K{row}'}
        for c,val in enumerate(vals,1):s.put(row,c,val,forms.get(c),1 if c>=5 else 2)
    s.put(11,1,'R');s.put(11,2,D[key]['R'],'SUM(N4:N8)')
    s.put(12,1,'W');s.put(12,2,D[key]['W'],wf('B11'))
    s.put(13,1,'Норма W');s.put(13,2,.3,style=2)
    summary.append((title,D[key]['W'],f"'{title}'!B12",.3))

s=Sheet('НЧ');sheets.append(s)
s.header(['f,Гц','Lᵢ,дБ','Lн,дБ','Uсш,дБ','Uш,дБ','Uсш,мкВ','Uш,мкВ','Uс,мкВ','Kᵢ','Uс.прив,мкВ','Uш.н,мкВ','Δ выход','U1,мкВ','U2,мкВ','Kлинии','Δ КЗ','Δ выход,дБ','Δ КЗ,дБ','ΔA,дБ','kᵢ','Q выход','p выход','Rᵢ выход','Q КЗ','p КЗ','Rᵢ КЗ'])
u1=[500.21,200,944.25,360.12,1100];u2=[62.14,8.72,34.54,78.52,95.12]
for row,v in enumerate(D['low_frequency']['rows'],4):
    a=[18,14,9,6,5][row-4];k=[.03,.12,.2,.3,.26][row-4]
    db1=20*math.log10(v['snr_output']);db2=20*math.log10(v['snr_boundary']);q1=db1-a;q2=db2-a
    vals=[v['frequency_Hz'],v['sound_dB'],v['normal_sound_dB'],v['signal_noise_dB'],v['noise_dB'],10**(v['signal_noise_dB']/20),10**(v['noise_dB']/20),v['signal_uV_method'],v['correction'],v['referred_uV'],v['norm_noise_uV'],v['snr_output'],u1[row-4],u2[row-4],v['line_attenuation'],v['snr_boundary'],db1,db2,a,k,q1,probability(q1),probability(q1)*k,q2,probability(q2),probability(q2)*k]
    formulas={3:f"'Параметры'!C{row}",6:f'10^(D{row}/20)',7:f'10^(E{row}/20)',8:f'IF(D{row}-E{row}<1,10^((D{row}-7)/20),SQRT(F{row}^2-G{row}^2))',9:f'10^((B{row}-C{row})/20)',10:f'H{row}/I{row}',11:f"'Параметры'!F{row}",12:f'J{row}/K{row}',15:f'M{row}/N{row}',16:f'L{row}/O{row}',17:f'20*LOG10(L{row})',18:f'20*LOG10(P{row})',19:f"'Параметры'!D{row}",20:f"'Параметры'!E{row}",21:f'Q{row}-S{row}',22:pf(f'U{row}'),23:f'V{row}*T{row}',24:f'R{row}-S{row}',25:pf(f'X{row}'),26:f'Y{row}*T{row}'}
    for c,val in enumerate(vals,1):s.put(row,c,val,formulas.get(c),1 if c in formulas else 2)
for row,label,val,form in [(11,'R выход',D['low_frequency']['output']['R'],'SUM(W4:W8)'),(12,'W выход',D['low_frequency']['output']['W'],wf('B11')),(14,'R КЗ',D['low_frequency']['boundary']['R'],'SUM(Z4:Z8)'),(15,'W КЗ',D['low_frequency']['boundary']['W'],wf('B14'))]:
    s.put(row,1,label);s.put(row,2,val,form)
summary.append(('НЧ на КЗ',D['low_frequency']['boundary']['W'],"'НЧ'!B15",.3))

s=Sheet('ВЧ');sheets.append(s)
constants=[('F,МГц',432.47832,None),('Kант,1/м',25,None),('Ra,м',.25,None),('R,м — принято',.5,None),('D,м',.55,None),('λ,м',300/432.47832,'300/B2'),('Kз',1.21,'(B6/B5)^2'),('EшN стац',.03,None),('EшN воз',D['high_frequency']['noise_densities']['vehicle'],'10^(0.7*LOG10(B2*1000)-5.09)'),('EшN нос',D['high_frequency']['noise_densities']['portable'],'10^(0.66*LOG10(B2*1000)-4.53)')]
for row,(label,val,formula) in enumerate(constants,2):
    s.put(row,1,label);s.put(row,2,val,formula,1 if formula else 2)
s.header(['i','ΔF,кГц','Lн,дБ','Lᵢ,дБ','Uсш,дБ','Uш,дБ','Uсш,мкВ','Uш,мкВ','Uс,мкВ','Kᵢ','Uс.прив,мкВ','Eс КЗ,мкВ/м'],14)
for row,v in enumerate(D['high_frequency']['rows'],15):
    paramrow=row-11
    vals=[v['octave'],v['bandwidth_kHz'],v['normal_sound_dB'],v['sound_dB'],v['signal_noise_dB'],v['noise_dB'],10**(v['signal_noise_dB']/20),10**(v['noise_dB']/20),v['raw_signal_uV_with_0_7'],10**((v['sound_dB']-v['normal_sound_dB'])/20),v['referred_uV'],v['field_boundary_uV_per_m']]
    formulas={2:f"'Параметры'!G{paramrow}",3:f"'Параметры'!B{paramrow}",7:f'10^(E{row}/20)',8:f'10^(F{row}/20)',9:f'0.7*SQRT(G{row}^2-H{row}^2)',10:f'10^((D{row}-C{row})/20)',11:f'I{row}/J{row}',12:f'K{row}*$B$3/$B$8'}
    for c,val in enumerate(vals,1):s.put(row,c,val,formulas.get(c),1 if c in formulas else 2)
s.put(22,1,'Проверка R≥2Ra');s.put(22,2,1,'IF(B5>=2*B4,1,0)')
s.put(23,1,'Применимость ветви Kз');s.put(23,2,1,'IF(AND(B5>B7/(2*PI()),B5<=6*B7,B6>B7/(2*PI()),B6<=6*B7),1,0)')
for title,kind,densrow in [('ВЧ_стац','stationary',9),('ВЧ_воз','vehicle',10),('ВЧ_нос','portable',11)]:
    s=Sheet(title);sheets.append(s)
    s.header(['i','Eс КЗ','ΔF,кГц','EшN','Eш.окт','Δ линейное','Δ,дБ','ΔA,дБ','kᵢ','Qᵢ','pᵢ','Rᵢ'])
    density=D['high_frequency']['noise_densities'][kind]
    for row,v in enumerate(D['high_frequency']['rows'],4):
        srcrow=row+11;a=[18,14,9,6,5][row-4];k=[.03,.12,.2,.3,.26][row-4];db=20*math.log10(v['snr_'+kind]);q=db-a;p=probability(q)
        vals=[v['octave'],v['field_boundary_uV_per_m'],v['bandwidth_kHz'],density,density*math.sqrt(v['bandwidth_kHz']),v['snr_'+kind],db,a,k,q,p,p*k]
        fs={1:f"'ВЧ'!A{srcrow}",2:f"'ВЧ'!L{srcrow}",3:f"'ВЧ'!B{srcrow}",4:f"'ВЧ'!$B${densrow}",5:f'D{row}*SQRT(C{row})',6:f'B{row}/E{row}',7:f'20*LOG10(F{row})',8:f"'Параметры'!D{row}",9:f"'Параметры'!E{row}",10:f'G{row}-H{row}',11:pf(f'J{row}'),12:f'K{row}*I{row}'}
        for c,val in enumerate(vals,1):s.put(row,c,val,fs[c])
    s.put(11,1,'R');s.put(11,2,D['high_frequency']['intelligibility'][kind]['R'],'SUM(L4:L8)')
    s.put(12,1,'W');s.put(12,2,D['high_frequency']['intelligibility'][kind]['W'],wf('B11'))
    summary.append((title,D['high_frequency']['intelligibility'][kind]['W'],f"'{title}'!B12",.3))

s=Sheet('Наводки');sheets.append(s)
s.header(['Fс,кГц*','Uсш,дБ','Uш,дБ','U1,дБ','U2,дБ','l А–Б,м','Rкз,м','Uс,дБ','Пᵢ,дБ','Kу,дБ/м','Ri клавиатура,м','Проходит:1/0','Ri с видео,м','Проходит:1/0'])
for row,(v,raw) in enumerate(zip(D['induced'],[(6.25,8,1.25,11.2,3.2),(4.11,6,1.12,10.6,2.8)]),4):
    vals=[*raw,5.25,8,v['signal_dB'],v['Pi_dB'],v['Ky_dB_per_m'],v['Ri_no_video_m'],1,v['Ri_with_video_m'],0]
    fs={8:f'10*LOG10(10^(B{row}/10)-10^(C{row}/10))',9:f'H{row}-C{row}',10:f'(D{row}-E{row})/F{row}',11:f'I{row}/J{row}',12:f'IF(K{row}<G{row},1,0)',13:f'(I{row}+10)/J{row}',14:f'IF(M{row}<G{row},1,0)'}
    for c,val in enumerate(vals,1):s.put(row,c,val,fs.get(c),1 if c in fs else 2)
s.put(8,1,'Максимум Ri без видео');s.put(8,2,max(v['Ri_no_video_m'] for v in D['induced']),'MAX(K4:K5)')
s.put(9,1,'Максимум Ri с видео');s.put(9,2,max(v['Ri_with_video_m'] for v in D['induced']),'MAX(M4:M5)')
s.put(11,1,'* Единицы');s.put(11,2,'В задании кГц; в ЛР6 для тех же чисел МГц. В расчёт пробега частота не входит.')

s=Sheet('Итог');sheets.append(s)
s.header(['Показатель','Значение','Предел','Норма:1/0'])
for row,(label,val,formula,limit) in enumerate(summary,4):
    s.put(row,1,label);s.put(row,2,val,formula);s.put(row,3,limit,style=2);s.put(row,4,1 if val<limit else 0,f'IF(B{row}<C{row},1,0)')
row=4+len(summary)
s.put(row,1,'Наводки: максимум Ri,м');s.put(row,2,max(v['Ri_no_video_m'] for v in D['induced']),"'Наводки'!B8");s.put(row,3,8,style=2);s.put(row,4,1,f'IF(B{row}<C{row},1,0)')

styles=f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><styleSheet xmlns="{M}">
<numFmts count="1"><numFmt numFmtId="164" formatCode="0.000000"/></numFmts>
<fonts count="3"><font><sz val="11"/><name val="Calibri"/></font><font><sz val="11"/><name val="Calibri"/><color rgb="FF1757A0"/></font><font><b/><sz val="11"/><name val="Calibri"/><color rgb="FFFFFFFF"/></font></fonts>
<fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FF17365D"/><bgColor indexed="64"/></patternFill></fill></fills>
<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>
<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
<cellXfs count="5"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/><xf numFmtId="164" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/><xf numFmtId="164" fontId="1" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/><xf numFmtId="0" fontId="2" fillId="2" borderId="0" xfId="0" applyAlignment="1"><alignment wrapText="1" vertical="center"/></xf><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0" applyAlignment="1"><alignment wrapText="1" vertical="top"/></xf></cellXfs>
<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>'''
workbook=X.Element('{'+M+'}workbook')
sheetnodes=X.SubElement(workbook,'{'+M+'}sheets')
rels=X.Element('{'+P+'}Relationships')
types=X.Element('{http://schemas.openxmlformats.org/package/2006/content-types}Types')
C='http://schemas.openxmlformats.org/package/2006/content-types'
for ext,mime in [('rels','application/vnd.openxmlformats-package.relationships+xml'),('xml','application/xml')]:X.SubElement(types,'{'+C+'}Default',Extension=ext,ContentType=mime)
for part,ctype in [('/xl/workbook.xml','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml'),('/xl/styles.xml','application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml')]:X.SubElement(types,'{'+C+'}Override',PartName=part,ContentType=ctype)
for i,s in enumerate(sheets,1):
    sh=X.SubElement(sheetnodes,'{'+M+'}sheet',name=s.title,sheetId=str(i));sh.set('{'+R+'}id',f'rId{i}')
    X.SubElement(rels,'{'+P+'}Relationship',Id=f'rId{i}',Type=R+'/worksheet',Target=f'worksheets/sheet{i}.xml')
    X.SubElement(types,'{'+C+'}Override',PartName=f'/xl/worksheets/sheet{i}.xml',ContentType='application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml')
X.SubElement(workbook,'{'+M+'}calcPr',calcId='191029',calcMode='auto',fullCalcOnLoad='1',forceFullCalc='1')
X.SubElement(rels,'{'+P+'}Relationship',Id='rStyles',Type=R+'/styles',Target='styles.xml')
rootrels=X.Element('{'+P+'}Relationships');X.SubElement(rootrels,'{'+P+'}Relationship',Id='rId1',Type=R+'/officeDocument',Target='xl/workbook.xml')
output=B/'Расчеты_99_формулы.xlsx'
with ZipFile(output,'w',ZIP_DEFLATED) as z:
    for path,root in [('[Content_Types].xml',types),('_rels/.rels',rootrels),('xl/workbook.xml',workbook),('xl/_rels/workbook.xml.rels',rels)]:z.writestr(path,X.tostring(root,encoding='utf-8',xml_declaration=True))
    z.writestr('xl/styles.xml',styles)
    for i,s in enumerate(sheets,1):z.writestr(f'xl/worksheets/sheet{i}.xml',s.xml())
print(output.name,'листов:',len(sheets),'формул:',sum(1 for s in sheets for v in s.cells.values() if v[1] is not None))
