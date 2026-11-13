# Анимации PowerPoint и учебные code snippets

Проверено 13 ноября 2026 года. Исследование по первичным источникам; презентация пока не генерировалась. Проверка реального воспроизведения остаётся этапом сборки.

## Вывод для выбранного инструментария

Upstream PptxGenJS не предоставляет публичного API native animations/transitions в просмотренной текущей ветке master. Это проверено по [types/index.d.ts](https://github.com/gitbrent/PptxGenJS/blob/master/types/index.d.ts) (заголовок версии 4.0.1) и [src/gen-xml.ts](https://github.com/gitbrent/PptxGenJS/blob/master/src/gen-xml.ts): `animation`, `transition`, `timing` отсутствуют. Страницы с `TransitionProps` в выдаче могут относиться к сторонним forks и не подтверждают возможности upstream.

Практические варианты после сборки слайдов:

1. **Предпочтительный в данной среде:** добавить эффекты через установленный Microsoft PowerPoint и сохранить PPTX самим PowerPoint.
2. **Резервный:** добавить `p:transition` и `p:timing` в OOXML и проверить пакет, открытие, сохранение и slideshow в PowerPoint.

### Локальная возможность PowerPoint проверена

Первичный источник: `/Applications/Microsoft PowerPoint.app/Contents/Resources/PowerPoint.sdef`, прочитан без запуска приложения.

Dictionary определяет:

- `add effect <sequence> for <shape> fx <MsoAnimEffect> trigger <MsoAnimTriggerType>`.
- У слайда есть `timeline`, у timeline — `main sequence`.
- Эффекты `animation type appear`, `animation type fade`.
- Триггеры `on page click`, `with previous`, `after previous`.
- `timing.duration`.
- У `slide show transition`: `entry effect`, `transition duration`, `advance on click`, `advance on time`.
- Переход `entry effect fade`.

Следовательно, **API объявлен доступным**. Его успешное исполнение и поведение в установленной версии ещё не проверены. GUI/AppleScript запуск требует обычного разрешения среды; словарь не заменяет runtime-проверку. Можно создавать один effect с `on page click` для первого объекта смыслового блока и `with previous` для остальных, чтобы фон, подпись и стрелка появлялись вместе.

## Сдержанное движение для этой презентации

Это авторское дизайнерское предложение, не требование стандарта:

- Между слайдами — короткий Fade; без звука и автоматического переключения.
- На схеме RAG — последовательное появление смысловых этапов по клику: question → retrieve → context → generate.
- На Agentic RAG — сначала основной путь, затем условная проверка и возврат к поиску.
- На графиках — появление всей серии либо смыслового сравнения; не анимировать каждый текстовый элемент.
- На code snippets — показывать блок целиком, при необходимости затем выделять ключевые строки.
- Не дублировать слайды ради имитации движения: число слайдов остаётся **12**.
- Текст выступления должен указывать **[Click]** в соответствующих местах.

## OOXML: подтверждённые правила

[Microsoft Learn, Working with animation](https://learn.microsoft.com/en-us/office/open-xml/presentation/working-with-animation): переходы и анимации находятся в slide XML, переход выполняется до объектных эффектов.

[Официальная схема Open XML SDK](https://github.com/dotnet/Open-XML-SDK/blob/main/data/schemas/schemas_openxmlformats_org_presentationml_2006_main.json) подтверждает последовательности:

```text
p:sld:    cSld → clrMapOvr? → transition? → timing? → extLst?
p:timing: tnLst? → bldLst? → extLst?
p:seq:    cTn → prevCondLst? → nextCondLst?
p:cTn:    stCondLst? → endCondLst? → endSync? → iterate?
          → childTnLst? → subTnLst?
p:cBhvr:  cTn → tgtEl → attrNameLst?
p:set:    cBhvr → to?
```

`p:transition` допускает один effect choice, затем необязательные `sndAc`, `extLst`. `p:fade` — обычный PresentationML effect. Для консервативного перехода достаточно:

```xml
<p:transition spd="fast" advClick="1"><p:fade/></p:transition>
```

Не добавлять `advTm`: он задаёт автоматическое переключение. Для минимальной совместимости использовать `spd`, а не нестандартный ненеймспейсный `dur`. Точная длительность существует как расширение `p14:dur`; для короткого Fade она необязательна. [Microsoft, Slide Transitions](https://learn.microsoft.com/en-us/openspecs/office_standards/ms-pptx/99b95b35-568a-4652-9cba-df3d1175952f).

### Native build: схема реализации, пока без runtime-гарантии

Рекомендуемая иерархия:

```text
p:timing
  p:tnLst
    p:par / p:cTn nodeType=tmRoot
      p:childTnLst
        p:seq
          p:cTn nodeType=mainSeq
            p:childTnLst
              delayed parallel wrapper per click
                entrance effect cTn nodeType=clickEffect
                  p:set visibility=visible
                  p:animEffect transition=in filter=fade  [только Fade]
          p:prevCondLst [onPrev → slide target]
          p:nextCondLst [onNext → slide target]
```

Для Appear нужен `p:set` на `style.visibility` с `p:strVal val="visible"`; это показано в [Microsoft SetBehavior](https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.presentation.setbehavior?view=openxml-2.20.0). Для Fade дополнительно используется [AnimateEffect](https://learn.microsoft.com/en-us/dotnet/api/documentformat.openxml.presentation.animateeffect?view=openxml-3.0.1), `transition="in" filter="fade"`, с собственной длительностью `cTn`. [MsoAnimEffect](https://learn.microsoft.com/en-us/office/vba/api/powerpoint.msoanimeffect) подтверждает Appear=1, Fade=10 в объектной модели PowerPoint; отображение в OOXML нужно проверить по сохранённому приложением примеру.

Не выдавать дерево выше за готовый гарантированно совместимый XML: важны оболочки последовательности, start conditions, visibility до первого клика и разные состояния после возврата на слайд. Самый безопасный способ получить эти детали — авторский небольшой образец, сохранённый самим PowerPoint. Проверить его дерево и использовать ту же структуру для оставшихся слайдов.

### Структурная проверка при postprocess

- Разобрать ZIP/XML штатным XML parser; не вставлять XML произвольной заменой строки.
- Найти объекты по стабильному `objectName` → фактическому `p:cNvPr/@id` после генерации.
- Проверить каждую `p:spTgt/@spid` против реальных ID данного слайда.
- Назначить уникальные `p:cTn/@id` внутри слайда.
- Не создавать вторые `p:timing`/`p:transition`; не переставлять `extLst` перед ними.
- Соблюдать namespace URI; не переименовывать случайно namespace в уже существующих атрибутах.
- Запустить Open XML SDK `OpenXmlValidator`, если среда позволяет; отсутствие XML parse errors не означает соответствие схеме.
- Проверить ровно 12 entries в presentation slide list, сохранность notes, chart relationships и embedded files.
- Открыть в PowerPoint без repair dialog, сохранить и повторно сравнить наличие effects/targets.
- В slideshow проверить: начальное скрытие, один смысловой build на клик, порядок, последний клик, следующий слайд, возврат назад.

## Preview и печать

[Microsoft PDF export](https://support.microsoft.com/en-us/powerpoint/training/save-powerpoint-presentations-as-pdf-files) описывает PDF как фиксированный layout. PDF и изображения используются для проверки композиции; они не доказывают playback native animations. Для финального статического экспорта все смысловые элементы должны оставаться читаемыми одновременно, без перекрывающихся взаимоисключающих состояний.

[Microsoft, platform comparison](https://support.microsoft.com/en-us/powerpoint/compare-powerpoint-features-on-different-platforms) подтверждает playback анимаций на разных платформах, но показывает ограничения отдельных функций. Обычные `on page click` builds предпочтительнее интерактивных `on shape click` triggers. Проверять надо именно целевой PowerPoint, а не только Finder/Quick Look/PDF.

## Два коротких учебных Python snippets

Оба примера — **Python-style pseudocode**, не вызовы конкретного SDK. `retrieve`, `generate`, `sufficient`, `rewrite` — абстрактные функции. Не добавлять выдуманные импорты. Показывать подпись **Illustrative pseudocode** на слайде и объяснение в notes/DOCX.

### 1. Basic RAG — 6 строк

```python
question = "What is our refund policy?"
passages = retrieve(question, top_k=5)
context = "\n".join(passages)
prompt = f"Use this evidence:\n{context}\n{question}"
answer = generate(prompt)
print(answer)
```

Смысл: модель получает найденные фрагменты до генерации. В реальной системе нужны правила ответа по источникам, ссылки и обработка недостаточных доказательств; эта короткая схема их не реализует.

### 2. Bounded retrieval loop — 7 строк

```python
query, answer = question, "Insufficient evidence."
for _ in range(3):
    evidence = retrieve(query)
    if sufficient(evidence, question):
        answer = generate(question, evidence)
        break
    query = rewrite(query)
```

Смысл: проверка и максимум три попытки. В Agentic RAG функции выбора/оценки могут использовать модель; данный snippet иллюстрирует ограниченный цикл, не полный универсальный agent. Итог хранится в `answer`. [Официальный LangGraph tutorial](https://docs.langchain.com/oss/python/langgraph/agentic-rag) описывает проверку релевантности и переписывание запроса, но наш snippet написан специально для объяснения.

## Статус доказательств

**Проверено:** текущие upstream файлы, правила Microsoft схемы, элементы OOXML и их назначение, объявления AppleScript API в установленном PowerPoint. Оба Python snippets разобраны `ast.parse` без ошибок; длина — 6 и 7 строк. Абстрактные функции не исполнялись.

**Не проверено:** исполнение AppleScript в этой среде, конкретный postprocess XML в slideshow, точная длительность разных PowerPoint consumers, поведение статического экспорта готового файла. Эти проверки обязательны после создания presentation; пока нельзя обещать, что анимации уже работают.
