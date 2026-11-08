# -*- coding: utf-8 -*-
"""Исправление раздела 4 без пересохранения стилей и разметки исходного DOCX.

Формулы: локальные методики ЛР2, ЛР3, ЛР4 (2026), ЛР6.
Числа специальных исследований: приложение к заданию КР, варианты 2/1.
"""
from copy import deepcopy
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree as E
import hashlib
import json
import math
import sys

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / 'analysis'))
from calculate_variant99 import intelligibility

SRC = BASE / 'отчет_с_титульником.docx'
DATA = json.loads((BASE / 'analysis/variant99_calculations.json').read_text())
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
      'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}


def tag(name):
    a, b = name.split(':')
    return '{' + NS[a] + '}' + b


def el(name, **attrs):
    out = E.Element(tag(name))
    for k, v in attrs.items():
        out.set(tag(k.replace('_', ':')), str(v))
    return out


def num(value, digits=4):
    if isinstance(value, str):
        return value
    return f'{value:.{digits}f}'.replace('.', ',')


def text_of(node):
    return ''.join(node.xpath('.//w:t/text() | .//m:t/text()', namespaces=NS))


def replace_text(node, text):
    """Сохраняет pPr и первый rPr; изменяет только содержимое параграфа."""
    rpr = node.find('.//w:rPr', NS)
    rpr = deepcopy(rpr) if rpr is not None else None
    for child in list(node):
        if child.tag != tag('w:pPr'):
            node.remove(child)
    run = el('w:r')
    if rpr is not None:
        run.append(rpr)
    lines = str(text).split('\n')
    for i, line in enumerate(lines):
        if i:
            run.append(el('w:br'))
        t = el('w:t')
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
        t.text = line
        run.append(t)
    node.append(run)


def mt(text):
    r = el('m:r')
    p = el('w:rPr')
    p.append(el('w:rFonts', w_ascii='Cambria Math', w_hAnsi='Cambria Math'))
    r.append(p)
    t = el('m:t')
    t.text = text
    r.append(t)
    return r


def pieces(*items):
    return [mt(x) if isinstance(x, str) else x for x in items]


def container(name, *items):
    out = el(name)
    for it in items:
        if isinstance(it, list):
            out.extend(it)
        else:
            out.append(mt(it) if isinstance(it, str) else it)
    return out


def power(base, exponent):
    return container('m:sSup', container('m:e', base), container('m:sup', exponent))


def fraction(a, b):
    return container('m:f', container('m:num', a), container('m:den', b))


def root(a):
    pr = container('m:radPr', el('m:degHide', m_val='1'))
    return container('m:rad', pr, el('m:deg'), container('m:e', a))


def equation(paragraph, *items):
    for c in list(paragraph):
        if c.tag != tag('w:pPr'):
            paragraph.remove(c)
    paragraph.append(container('m:oMathPara', container('m:oMath', pieces(*items))))


def piecewise(paragraph, left, rows):
    arr = el('m:eqArr')
    for row in rows:
        arr.append(container('m:e', pieces(*row)))
    dpr = container('m:dPr', el('m:begChr', m_val='{'), el('m:endChr', m_val=''))
    d = container('m:d', dpr, container('m:e', arr))
    equation(paragraph, left, d)


with ZipFile(SRC) as z:
    original = {i.filename: z.read(i.filename) for i in z.infolist()}
    infos = z.infolist()
doc = E.fromstring(original['word/document.xml'])
body = doc.find('w:body', NS)
P = body.findall('w:p', NS)
T = body.findall('w:tbl', NS)
changes = []


def p(index, text):
    before = text_of(P[index])
    replace_text(P[index], text)
    changes.append({'paragraph_original': index, 'before': before, 'after': text})


def after(index, text):
    node = deepcopy(P[240])
    replace_text(node, text)
    P[index].addnext(node)
    return node


def before(index, text):
    node = deepcopy(P[240])
    replace_text(node, text)
    P[index].addprevious(node)
    return node


def cell(table, row, col, value):
    tc = T[table].findall('w:tr', NS)[row].findall('w:tc', NS)[col]
    paragraphs = tc.findall('w:p', NS)
    if not paragraphs:
        paragraphs = [el('w:p')]
        tc.append(paragraphs[0])
    replace_text(paragraphs[0], value)
    for extra in paragraphs[1:]:
        tc.remove(extra)


def inventory_table(index, rows):
    """Меняет строки перечня, сохраняя ширины столбцов и оформление ячеек."""
    table=T[index]
    existing=table.findall('w:tr',NS)
    prototype=deepcopy(existing[1])
    for tr in existing[1:]:table.remove(tr)
    for row_index,values in enumerate(rows,1):
        table.append(deepcopy(prototype))
        for column,value in enumerate(values):cell(index,row_index,column,str(value))


inventory=json.loads((BASE/'report_assets/room_inventory.json').read_text())
furniture=inventory['furniture']
equipment=inventory['equipment']
project_equipment=inventory['project_equipment']
show=lambda value: '—' if value is None else value
inventory_table(3,[
    ('стол',furniture['tables_total']),
    ('стул',show(furniture['chairs'])),
    ('доска двухсекционная',furniture['boards']),
    ('мусорное ведро',furniture['bins']),
    ('шкаф',furniture['cupboards']),
    ('тумба под телефон',furniture['telephone_pedestals']),
    ('вешалка напольная',furniture['coat_racks']),
])
equipment_rows=[
    ('персональный компьютер',project_equipment['computers']),
    ('монитор',project_equipment['monitors']),
    ('клавиатура',project_equipment['keyboards']),
    ('компьютерная мышь',project_equipment['mice']),
    ('телефонный аппарат',project_equipment['telephones']),
    ('коммутатор',project_equipment['network_switches']),
]
inventory_table(4,equipment_rows)
p(124, 'В аудитории размещены 12 учебных столов и один отдельный стол. Перечень мебели приведён в таблице 1.1.')
p(126, 'В соответствии с исходными условиями задания в ЗП принимаются три персональных компьютера, объединённых в локальную сеть без выхода за пределы помещения. Перечень оборудования приведён в таблице 1.2.')
p(128, '')


# Текст и исходная постановка.
p(121, 'По исходным условиям задания защищаемое помещение не оборудовано системой пожарной и охранной сигнализации. Их установка предусматривается в составе мероприятий по физической защите объекта.')
p(225, '4 Определение характеристик идентифицированных каналов утечки информации')
p(226, '4.1 Утечки по акустическому и виброакустическому каналам')
p(227, 'Исследуется стена аудитории 1-499, выходящая в коридор. Общая ширина стены составляет 6385 мм, высота помещения — 3380 мм; дверной проём — 1200×2228 мм. Дверь, вентиляционные проёмы и выступы учитываются отдельно. Исходные данные варианта 2 относятся к однородному участку стены.')
after(227, 'Обработка результатов выполняется по методике ЛР № 2 за 2026 год, с.15–16 и приложениям 3.2–3.3 (с.26–27). Расчётная оценка основана на результатах специальных измерений, приведённых в задании.')
# Старые рисунки потолка/телефона/ПЭВМ не выдаются за новые схемы.
for image_p, caption_p in [(228,229),(231,232),(267,268),(297,298),(326,327)]:
    for idx in [image_p, caption_p]:
        if P[idx].getparent() is body:
            body.remove(P[idx])
p(238, 'Для акустического контроля стены контрольные точки проектируются на расстоянии 0,5 м от её внешней поверхности; для вибрационного контроля — непосредственно на ограждающей конструкции. По ЛР № 2, с.5, для однородной поверхности ориентировочно намечается одна точка на участок размером около 2×2 м. Проёмы и неоднородные участки исследуются отдельно.')
p(239, 'В расчёте применяется модель речи без звукоусиления: Lнᵢ = [66; 66; 61; 56; 53] дБ для пяти октав 250–4000 Гц. При обработке вибрационных измерений нормируется исходное акустическое воздействие; значения V подставляются вместо измеренных вибрационных уровней по методике ЛР № 2.')
equation(P[242], 'Lсᵢ = 10 lg(', power('10', fraction('Lс+шᵢ','10')), ' − ', power('10',fraction('Lшᵢ','10')), ')')
piecewise(P[250], 'W = ', [
    ['1,54·',power('R','0,25'),'·(1 − ',power('e','−11R'),'),  R < 0,15;'],
    ['1 − ',power('e',fraction('−11R','1 + 0,7R')),',  R ≥ 0,15.'],
])
def p_fraction():
    numerator = pieces('0,78 + 5,46·',power('e',pieces('−4,3·',power('10','−3'),'·',power('(27,3 − |Qᵢ|)','2'))))
    denominator = pieces('1 + ',power('10','0,1|Qᵢ|'))
    return fraction(numerator,denominator)
piecewise(P[253], 'pᵢ = ', [[p_fraction(),',  Qᵢ ≤ 0;'],['1 − ',p_fraction(),',  Qᵢ > 0.']])
p(255, 'Здесь Δᵢ — октавное отношение сигнал/шум в дБ; ΔAᵢ — формантный параметр речи; kᵢ — весовой коэффициент. По ЛР № 2, с.27: ΔAᵢ=[18;14;9;6;5] дБ, kᵢ=[0,03;0,12;0,20;0,30;0,26]. Для акустики и виброакустики Δᵢ=Eᵢ уже выражено в дБ. Для линейных отношений напряжений далее используется перевод Δᵢ[дБ]=20·lg(Δᵢ). Веса берутся непосредственно из методики.')
for table,key in [(6,'acoustic'),(7,'vibration')]:
    rows=DATA[key]['rows']
    for col,r in enumerate(rows,1):
        for row,field in [(1,'test_dB'),(2,'signal_noise_dB'),(3,'noise_dB')]:
            cell(table,row,col,num(r[field],3))
cell(6,1,0,'Lтсᵢ, дБ')
cell(6,2,0,'Lс+шᵢ, дБ')
for table,key in [(8,'acoustic'),(9,'vibration')]:
    rows=DATA[key]['rows']
    for col,r in enumerate(rows,1):
        for row,field in [(1,'test_dB'),(2,'signal_noise_dB'),(3,'noise_dB'),
                          (4,'signal_dB'),(5,'normal_dB'),(6,'correction_dB'),
                          (7,'referred_dB'),(8,'snr_dB')]:
            cell(table,row,col,num(r[field],3))
    cell(table,9,1,'Рассчитанное значение W = '+num(DATA[key]['W'],6))
for row,label in [(1,'Lтсᵢ, дБ'),(2,'Lс+шᵢ, дБ'),(3,'Lшᵢ, дБ'),(4,'Lсᵢ, дБ'),
                  (5,'Lнᵢ, дБ'),(6,'ΔLᵢ, дБ'),(7,'Lс.привᵢ, дБ'),(8,'Eᵢ, дБ')]:
    cell(8,row,0,label)
p(262, 'Вывод: для однородного участка стены в коридор Wак=0,549066 и Wвибр=0,575576. Оба значения превышают Wн=0,3: нормы противодействия акустической и виброакустической разведке не выполняются. Акустическая разборчивость также превышает 0,5 — критерий для непреднамеренного прослушивания. Требуются мероприятия по защите стены с последующей проверкой их эффективности. Результат не распространяется автоматически на дверь, вентиляционные проёмы и остальные конструкции.')

# НЧ АЭП — вариант 2, цепь электропитания, со звукоусилением.
p(264, 'Для проектируемой пожарной системы оценивается извещатель по варианту 2 задания (с.7–8). Исследуемая линия — электропитание; подключение симметричное; средства защиты отсутствуют. Исходные данные заданы с учётом работы звукоусиления, поэтому применяются Lнᵢ=[80;80;75;70;67] дБ (ЛР № 3, с.10).')
p(266, 'Измерительная схема предусматривает акустическое воздействие на извещатель, регистрацию напряжений в исследуемой цепи питания и точки T1/T2 для определения затухания до границы КЗ.')
low = DATA['low_frequency']['rows']
low_raw = [[275,100.10,44,41,500.21,62.14], [525,96.12,45,44,200,8.72],
           [1025,97,42,43,944.25,34.54], [2025,91.21,41,40,360.12,78.52],
           [4025,89,32,32,1100,95.12]]
cell(10,0,1,'2')
for j,label in [(4,'Напряжение в цепи питания в точке T1, U1ᵢ, мкВ'),
                (5,'Напряжение в цепи питания на границе КЗ T2, U2ᵢ, мкВ')]:
    cell(10,3,j,label)
for j,row in enumerate(low_raw,4):
    for k,v in enumerate(row):cell(10,j,k,str(v).replace('.',','))
after(271, 'При Uсшᵢ−Uшᵢ<1 дБ применяется прямо предусмотренный в ЛР № 3, с.11, приём: Uсᵢ[дБ]=Uсшᵢ[дБ]−7 дБ. Для 1025 Гц разность равна −1 дБ, поэтому Uс=35 дБмкВ=56,234133 мкВ; для 4025 Гц разность равна 0 дБ, поэтому Uс=25 дБмкВ=17,782794 мкВ. Обычное вычитание энергий в этих двух строках не применяется. При реальном исследовании методика рекомендует повторное измерение при малом превышении сигнала над шумом (ЛР № 3, с.10).')
p(276, 'Нормированные электрические шумы выбираются по виду исследуемой цепи. Для цепи электропитания по таблице 3.4 ЛР № 3 (с.12) используются Uш.нᵢ=[151;74;20,5;4,6;1] мкВ. Значения для телефонных линий в этом расчёте не применяются.')
for j,r in enumerate(low,1):
    for k,v in enumerate([r['frequency_Hz'],10**(r['signal_noise_dB']/20),10**(r['noise_dB']/20),r['signal_uV_method'],r['correction'],r['referred_uV']]):
        cell(12,j,k,num(v,4) if k else str(v))
cell(13,0,1,'Нормированный шум цепи электропитания, Uш.нᵢ, мкВ')
cell(13,0,2,'Шум для расчёта отношения сигнал/шум, мкВ')
cell(14,0,1,'Коэффициент затухания исследуемой линии, Kлᵢ')
for j,r in enumerate(low,1):
    for k,v in [(1,r['norm_noise_uV']),(2,r['norm_noise_uV']),(3,r['snr_output'])]:cell(13,j,k,num(v,6))
    for k,v in [(1,r['line_attenuation']),(2,r['snr_boundary'])]:cell(14,j,k,num(v,6))
cell(13,1,4,num(DATA['low_frequency']['output']['W'],6))
cell(14,1,3,num(DATA['low_frequency']['boundary']['W'],6))
p(292, 'Вывод: на выходе рассматриваемого извещателя W=0,868670, а на границе КЗ после учёта затухания W*=0,137873<0,3. Для устройства проектируемой системы при заданных параметрах линии норма противодействия на границе КЗ выполняется.')

# ВЧ АЭП — вариант 1, принтер.
p(294, 'Для расчёта ВЧ АЭП по варианту 1 задания (с.10–11) в составе ОТСС рассматривается принтер. В исходных результатах исследований в эфире в диапазоне 10 кГц…1,2 ГГц указан сигнал встроенного генератора F=432,47832 МГц.')
p(295, 'При акустическом тональном воздействии 1025 Гц для этой несущей заданы модуляционные составляющие. Используются Kант=25 м⁻¹, Ra=0,25 м, D=0,55 м, Δн=0,30 и Wн=0,30. Октавная модель речи без звукоусиления: Lнᵢ=[66;66;61;56;53] дБ.')
p(296, 'Расстояние R между измерительной антенной и корпусом ТС в задании не указано. Для расчётной схемы явно принимается R=2Ra=0,50 м — минимальное расстояние, допускаемое ЛР № 4, с.5. Это принятое условие модели, а не новый результат натурного измерения. По приложению 2 методики (с.20): λ=300/F=0,693676 м; λ/(2π)=0,110402 м; 6λ=4,162056 м. Поскольку R и D находятся между этими границами, Kз=(D/R)²=1,21.')
p(300, 'Таблица 4.3.1 – Исходные данные на частоте 432,47832 МГц')
high = DATA['high_frequency']['rows']
fixed = ['432,47832','25','0,30','0,30','0,25','0,55']
for i,v in enumerate(fixed):
    cell(15,i,1,v)
    cell(16,i,1,v)
for i,r in enumerate(high,7):
    for j,v in enumerate([r['octave'],r['sound_dB'],r['signal_noise_dB'],r['noise_dB']]):
        cell(15,i,j,str(v).replace('.',','))
dens=DATA['high_frequency']['noise_densities']
for i,k in enumerate(['stationary','vehicle','portable'],6):cell(16,i,1,num(dens[k],9))
cell(16,9,1,'1,21')
cell(16,10,5,'Напряжение «сигнал+шум», Uсшᵢⱼ, мкВ')
for i,r in enumerate(high,11):
    values=[r['octave'],r['bandwidth_kHz'],r['sound_dB'],r['signal_noise_dB'],r['noise_dB'],
            10**(r['signal_noise_dB']/20),10**(r['noise_dB']/20)]
    for j,v in enumerate(values):cell(16,i,j,str(v).replace('.',',') if j in [0,2,3,4] else num(v,6))
for i,r in enumerate(high,1):
    k=10**((r['sound_dB']-r['normal_sound_dB'])/20)
    for j,v in enumerate([r['octave'],k,r['raw_signal_uV_with_0_7'],r['referred_uV'],r['field_boundary_uV_per_m']]):
        cell(17,i,j,str(v) if j==0 else num(v,6))
    for j,kind in enumerate(['stationary','vehicle','portable'],1):
        noise=dens[kind]*math.sqrt(r['bandwidth_kHz'])
        cell(18,i,j,num(noise,8))
        cell(19,i,2*j-1,num(r['snr_'+kind],6))
        cell(19,i,2*j,'Да' if r['snr_'+kind]<.3 else 'Нет')
cell(17,0,4,'Напряжённость поля на границе КЗ, Eсᵢⱼ, мкВ/м')
for i,kind in enumerate(['stationary','vehicle','portable']):
    cell(20,i,1,num(DATA['high_frequency']['intelligibility'][kind]['W'],6))
    cell(20,i,3,'Нет')
after(312, 'Нормированные плотности вычислены по приложению 3 ЛР № 4, с.21–22, при f=432478,32 кГц: EшN,стац=0,03; EшN,воз=10^(0,7·lg(f)−5,09)=0,071643210; EшN,нос=10^(0,66·lg(f)−4,53)=0,154787706 мкВ/(м·√кГц). Ширины октав ΔFᵢ=[0,180;0,355;0,690;1,400;2,800] кГц. Значения в Гц предварительно делятся на 1000.')
p(322, 'Вывод: при R=0,50 м и D=0,55 м Wстац=0,936329; Wвоз=0,759185; Wнос=0,372150. Все три значения превышают Wн=0,3. Октавный критерий Δ<0,3 нарушен в октавах 1–5 для стационарных, 1–4 для возимых и 1–3 для носимых ТСР. ВЧ акустоэлектрический канал требует мер защиты. Все превышения Uсш−Uш в исходных данных составляют 1–4 дБ; по ЛР № 4, с.7–8, при натурном контроле такие результаты требуют повторных измерений. Здесь выполнена расчётная оценка по выданному варианту.')
after(322, 'Для проверки организационной меры при сохранении R=0,50 м увеличим расстояние принтера до границы КЗ до D=2,00 м. Тогда Kз=(2/0,5)²=16; поле и линейные отношения сигнал/шум уменьшаются в 16/1,21=13,223140 раза. Получаются max(Δстац)=0,270478<0,3 и Wстац≈0,081018; возимые и носимые ТСР также удовлетворяют критериям. При принятой измерительной схеме рекомендуется размещение принтера на расстоянии не менее 2 м от границы КЗ.')

# Наводки — отдельная клавиатура без видеоконтрольного устройства.
p(324, 'По варианту 1 задания (с.12) рассматриваются наводки информативных ПЭМИ клавиатуры на отходящую цепь. Даны компоненты 6,25 и 4,11, пробег до границы КЗ Rкз=8 м и длина линии между А/Б l=5,25 м. В задании частоты подписаны в кГц, а в ЛР № 6 (с.10–11) для полностью совпадающей таблицы — в МГц. Ниже численные значения и единицы таблицы задания сохранены с примечанием; формулы расчёта пробега от частоты непосредственно не зависят.')
p(325, 'В задании описание относится к цепи питания, а длина до КЗ названа длиной линии заземления. Для расчётной оценки используется заданный пробег исследуемой цепи 8 м. Тип линии должен быть окончательно согласован с её схемой; численные уровни и длины не изменяются.')
p(328, 'Исходные данные представлены в таблице 4.4.1: для клавиатуры заданы две частотные компоненты без разделения исследуемой цепи на фазу и ноль.')
p(329, 'Таблица 4.4.1 – Исходные данные клавиатуры (единицы частоты — по заданию)')
cell(21,0,0,'Частота Fс, кГц*')
cell(22,0,0,'Частота Fс, кГц*')
for j,label in enumerate(['Fс, кГц*','Uс+ш, дБ','Uш, дБ','Uс, дБ','U1, дБ','U2, дБ','Kу, дБ/м','Rᵢ, м']):
    cell(22,0,j,label)
raw=[[6.25,8,1.25,11.2,3.2],[4.11,6,1.12,10.6,2.8]]
for i,row in enumerate(raw,2):
    for j,v in enumerate(row):cell(21,i,j,str(v).replace('.',','))
for i,(r,rawrow) in enumerate(zip(DATA['induced'],raw),2):
    values=[rawrow[0],rawrow[1],rawrow[2],r['signal_dB'],rawrow[3],rawrow[4],r['Ky_dB_per_m'],r['Ri_no_video_m']]
    for j,v in enumerate(values):cell(22,i,j,str(v).replace('.',',') if j in [0,1,2,4,5] else num(v,6))
for ti in [21,22]:
    rows=T[ti].findall('w:tr',NS)
    for i in [6,5,4,1]:T[ti].remove(rows[i])
p(337, 'Для исследуемой клавиатуры как отдельного ОТСС без видеоконтрольного устройства максимальная длина пробега вычисляется по соответствующей ветви методики ЛР № 6, с.8:')
equation(P[336], 'Kу [дБ/м] = ', fraction(pieces('20 lg(',fraction('U1 [мкВ]','U2 [мкВ]'),')'),'l [м]'))
p(340, 'Вывод: Uс=[6,968849;4,292476] дБмкВ; Пᵢ=[5,718849;3,172476] дБ; Kу=[1,523810;1,485714] дБ/м; Rᵢ=[3,752995;2,135320] м. Максимальный пробег 3,752995 м меньше Rкз=8 м; для отдельной клавиатуры по принятой ветви методики условие защищённости исследуемой цепи выполняется. Этот вывод не является оценкой всего комплекса ПЭВМ с монитором.')
after(340, 'Примечание к таблицам 4.4.1–4.4.2: * в ЛР № 6 те же частоты приведены в МГц; для выбора диапазона аппаратуры требуется уточнение единиц задания. Если объектом исследования считается весь комплекс с видеоконтрольным устройством, применяется другая формула Rᵢ=(Пᵢ+10)/Kу. Контрольный расчёт даёт 10,315495 и 8,866090 м, то есть обе величины превышают 8 м; защищённость по этой ветви не обеспечивается. При смене объекта исследования вывод необходимо изменить.')

# Небольшие согласования зависимых выводов, чтобы в рабочей копии не оставалось противоположных утверждений.
p(412, 'По расчётам раздела 4 нормы не выполняются для акустического и виброакустического каналов стены в коридор, а также для ВЧ АЭП принтера при принятой измерительной схеме. НЧ АЭП пожарного извещателя на границе КЗ удовлетворяет критерию; вывод по наводкам относится к отдельной клавиатуре.')
p(413, 'Меры акустической и виброакустической защиты предусматриваются для стены, выходящей в коридор, с отдельным учётом проёмов и неоднородных участков.')
p(414, 'Для ВЧ АЭП рассматривается удаление принтера от границы КЗ с расчётной проверкой, приведённой в п.4.3.')
p(415, 'Блок «Соната-ИП3» предназначен для электропитания технических средств защиты информации и объединения подключённых устройств в комплекс ТСЗИ. Установка пожарной и охранной сигнализации предусматривается в составе проектируемых мероприятий. Расчёт НЧ АЭП пожарного извещателя приведён в п.4.2.')
p(416, 'Блок питания и управления «Соната-ИП3» представлен на рисунке 6.1.')
p(466, 'В работе выполнена расчётная оценка четырёх групп технических каналов утечки информации для окончания зачётной книжки 99. Исходные результаты специальных исследований взяты из задания; обработка выполнена по методикам лабораторных работ № 2, 3, 4 и 6.')
p(467, 'Для стены в коридор получены Wак=0,549066 и Wвибр=0,575576, что превышает 0,3. НЧ АЭП пожарного извещателя на границе КЗ даёт W*=0,137873. Для ВЧ АЭП принтера при R=0,50 м и D=0,55 м получены W=0,936329;0,759185;0,372150 для трёх типов ТСР. Для отдельной клавиатуры максимальный расчётный пробег составляет 3,752995 м при заданных 8 м до КЗ.')
p(468, 'Результаты расчётов обосновывают необходимость акустической и виброакустической защиты стены, выходящей в коридор, и ограничения размещения принтера относительно границы КЗ. При заданных параметрах линии норма противодействия НЧ АЭП пожарного извещателя на границе КЗ выполняется; оценка наводок относится к отдельной клавиатуре без видеоконтрольного устройства.')

# Локальные методики добавляются к литературе; существующие номера ссылок сохраняются.
for title in [
    'Методические материалы ДГТУ. Лабораторная работа № 2 «Исследование акустического и виброакустического каналов утечки конфиденциальной информации». 2026. 27 с. Локальный файл: лабораторные/ЛР 2/2026.',
    'Методические материалы ДГТУ. Лабораторная работа № 3 «Расчётный метод оценки защищённости речевой информации от утечки за счёт НЧ акустоэлектрических преобразований». 2026. 26 с. Локальный файл: лабораторные/ЛР 3/2026.',
    'Методические материалы ДГТУ. Лабораторная работа № 4 «Инструментально-расчётный метод контроля защищённости ВЧ АЭП». 2026. 23 с. Локальный файл: лабораторные/ЛР 4/2026.',
    'Методические материалы ДГТУ. Лабораторная работа № 6 «Оценка защищённости ОТСС от утечки информации за счёт наводок». 16 с. Локальный файл: лабораторные/ЛР 6.',
]:
    node=deepcopy(P[485])
    replace_text(node,title)
    body.insert(len(body)-1,node)

# Переносы только внутри изменяемого раздела: строка таблицы не разрывается
# между страницами, подпись остаётся с первой строкой таблицы.
for table in T[6:23]:
    for row in table.findall('w:tr',NS):
        pr=row.find('w:trPr',NS)
        if pr is None:
            pr=el('w:trPr');row.insert(0,pr)
        if pr.find('w:cantSplit',NS) is None:pr.append(el('w:cantSplit'))
for paragraph in P[225:341]:
    if text_of(paragraph).startswith('Таблица '):
        pr=paragraph.find('w:pPr',NS)
        if pr is None:pr=el('w:pPr');paragraph.insert(0,pr)
        if pr.find('w:keepNext',NS) is None:pr.append(el('w:keepNext'))

output=BASE/'отчет_99_расчеты_обновлены.docx'
def pack(path,document):
    xml=E.tostring(document,xml_declaration=True,encoding='UTF-8',standalone=True)
    with ZipFile(path,'w',ZIP_DEFLATED) as z:
        for info in infos:
            z.writestr(info,xml if info.filename=='word/document.xml' else original[info.filename])
pack(output,doc)

# Отдельный раздел удобен для проверки: тот же стиль, исходные таблицы, формулы Word.
section_doc=deepcopy(doc)
section_body=section_doc.find('w:body',NS)
nodes=list(body)
start=nodes.index(P[225])
end=nodes.index(P[341])
calculation_nodes=[deepcopy(x) for x in nodes[start:end]]
sect=deepcopy(body.find('w:sectPr',NS))
for child in list(sect):
    if child.tag in [tag('w:headerReference'),tag('w:footerReference'),tag('w:pgNumType')]:sect.remove(child)
for x in list(section_body):section_body.remove(x)
section_body.extend(calculation_nodes)
section_body.append(sect)
pack(BASE/'Расчетная_часть_99.docx',section_doc)
(BASE/'report_assets/calculation_changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2))
(BASE/'report_assets/source_hash.json').write_text(json.dumps({SRC.name:hashlib.sha256(SRC.read_bytes()).hexdigest()},ensure_ascii=False,indent=2))
print('Созданы',output.name,'и Расчетная_часть_99.docx')
