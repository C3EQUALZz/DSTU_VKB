"""Независимое вычисление формул готового XLSX по его XML и ссылкам ячеек."""
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as X
import math
import re

BASE=Path(__file__).resolve().parents[1]
NS={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
cells={}
with ZipFile(BASE/'Расчеты_99_формулы.xlsx') as z:
    workbook=X.fromstring(z.read('xl/workbook.xml'))
    for i,s in enumerate(workbook.findall('s:sheets/s:sheet',NS),1):
        title=s.get('name')
        root=X.fromstring(z.read(f'xl/worksheets/sheet{i}.xml'))
        for c in root.findall('.//s:c',NS):
            if c.get('t')=='inlineStr':continue
            value=c.find('s:v',NS)
            formula=c.find('s:f',NS)
            cells[(title,c.get('r'))]=(float(value.text),formula.text if formula is not None else None)

token=re.compile(r"'[^']+'!\$?[A-Z]+\$?[0-9]+|\$?[A-Z]+\$?[0-9]+|[A-Za-z_][A-Za-z0-9_.]*|(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?|<=|>=|<>|[-+*/^(),:]|[=<>]")
precedence={':':50,'^':30,'*':20,'/':20,'+':10,'-':10,'<':5,'>':5,'<=':5,'>=':5,'=':5,'<>':5}


class Parser:
    def __init__(self,formula):
        self.tokens=token.findall(formula)
        assert ''.join(self.tokens)==formula.replace(' ',''),formula
        self.i=0
    def peek(self):return self.tokens[self.i] if self.i<len(self.tokens) else None
    def take(self):
        val=self.peek();self.i+=1;return val
    def expression(self,minimum=0):
        item=self.take()
        if item in ['+','-']:left=('unary',item,self.expression(40))
        elif item=='(':
            left=self.expression();assert self.take()==')'
        elif self.peek()=='(':
            self.take();args=[]
            if self.peek()!=')':
                while True:
                    args.append(self.expression())
                    if self.peek()!=',':break
                    self.take()
            assert self.take()==')'
            left=('call',item,args)
        elif re.fullmatch(r'(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?',item):left=('number',float(item))
        else:left=('cell',item.replace('$',''))
        while self.peek() in precedence and precedence[self.peek()]>=minimum:
            op=self.take();p=precedence[op]
            right=self.expression(p if op=='^' else p+1)
            left=('binary',op,left,right)
        return left


def ref(value,sheet):
    if '!' in value:
        part,cell=value.rsplit('!',1);return (part.strip("'"),cell)
    return sheet,value


computed={}
def cell_value(key):
    if key not in computed:
        cached,formula=cells[key]
        if formula:
            parser=Parser(formula)
            ast=parser.expression()
            assert parser.peek() is None,(key,formula)
            result=evaluate(ast,key[0])
        else:result=cached
        computed[key]=result
    return computed[key]


def evaluate(ast,sheet):
    kind=ast[0]
    if kind=='number':return ast[1]
    if kind=='cell':return cell_value(ref(ast[1],sheet))
    if kind=='unary':return evaluate(ast[2],sheet)*(1 if ast[1]=='+' else -1)
    if kind=='binary':
        op=ast[1]
        if op==':':
            first=ref(ast[2][1],sheet);last=ref(ast[3][1],sheet)
            a=re.fullmatch(r'([A-Z]+)([0-9]+)',first[1]);b=re.fullmatch(r'([A-Z]+)([0-9]+)',last[1])
            assert first[0]==last[0] and a[1]==b[1]
            return [cell_value((first[0],a[1]+str(row))) for row in range(int(a[2]),int(b[2])+1)]
        a=evaluate(ast[2],sheet);b=evaluate(ast[3],sheet)
        return {'+':lambda:a+b,'-':lambda:a-b,'*':lambda:a*b,'/':lambda:a/b,'^':lambda:a**b,
                '<':lambda:a<b,'>':lambda:a>b,'<=':lambda:a<=b,'>=':lambda:a>=b,'=':lambda:a==b,'<>':lambda:a!=b}[op]()
    if kind=='call':
        function=ast[1].upper();args=ast[2]
        if function=='IF':return evaluate(args[1] if evaluate(args[0],sheet) else args[2],sheet)
        vals=[evaluate(x,sheet) for x in args]
        if function in ['SUM','MAX']:
            flat=[v for x in vals for v in (x if isinstance(x,list) else [x])]
            return sum(flat) if function=='SUM' else max(flat)
        if function=='AND':return all(vals)
        return {'EXP':math.exp,'LOG10':math.log10,'SQRT':math.sqrt,'ABS':abs,'PI':lambda:math.pi}[function](*vals)
    raise ValueError(ast)


count=0;largest=0
for key,(cached,formula) in cells.items():
    if formula:
        actual=cell_value(key)
        delta=abs(actual-cached)
        assert delta <= 1e-10*max(1,abs(cached)),(key,formula,cached,actual)
        largest=max(largest,delta);count+=1
print(f'Проверено {count} формул XLSX с разрешением ссылок между листами. Максимальное расхождение: {largest:.3g}.')
