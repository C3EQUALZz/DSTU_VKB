# AI + RAG static analysis in CI: research and claim mapping

Updated: 2026-11-13. This supersedes the earlier proposed SOC scenario. The main case is the student's real CI module; SOC and Microsoft Security Copilot are not the presentation's core story.

## Confirmed personal experience

The student reports configuring a RAG pipeline using OWASP and similar security-knowledge sources, and writing a CI module that scans a codebase for vulnerabilities using AI and RAG as part of static analysis.

Safe English wording: **“I configured a RAG pipeline using security knowledge from OWASP and other sources. I also wrote a CI module that scans source code for potential vulnerabilities.”**

Not confirmed: programming language, LLM, embedding model, vector database, CI provider, code-chunking method, AST or taint analysis, exact additional knowledge sources, report format, blocking policy, production deployment, validation results, and performance metrics. Do not fill those gaps with typical architecture choices. Later clarifications explicitly confirm that GraphRAG and Agentic RAG were implemented; the user also named AG2 and FastMCP. Exact internal versions and workflows remain unspecified.

## Security knowledge: use precise terms

| Resource | What it supplies | Presentation wording |
|---|---|---|
| OWASP | A foundation publishing security projects and guidance; its Top 10 is an awareness document about web-application risk categories. | “OWASP security guidance” — not “the OWASP CVE database.” |
| CWE | A taxonomy of weakness types that can lead to vulnerabilities. | “Weakness knowledge, such as CWE-89 SQL injection.” |
| CVE | Identifiers and records for specific publicly disclosed vulnerabilities in products. | “Historical vulnerability records,” only if actually included. |

Primary sources: [OWASP Top 10 project](https://owasp.org/projects/top-ten), [MITRE CWE about page](https://cwe.mitre.org/about/index.html), and [MITRE's CWE/CVE relationship explanation](https://cwe.mitre.org/about/faq.html). The live CVE website required JavaScript in the text browser; the CWE Program's explicit comparison was checked instead.

Use **OWASP Top 10:2021 A03 Injection** only when the year is shown. The project page currently lists the 2025 edition as the current release; do not silently call A03:2021 the latest version.

## Direct research evidence: Vul-RAG

Version fixed for this presentation: **arXiv:2406.11147v3, June 17, 2025**. [Full paper](https://arxiv.org/html/2406.11147v3), [versioned abstract](https://arxiv.org/abs/2406.11147v3). Do not mix its results with v1 or the later ACM publication.

Vul-RAG retrieves distilled knowledge about vulnerability causes and fixes to guide LLM code assessment. Its PairVul benchmark contains **586 vulnerable/patched function pairs from 420 CVEs**, focused on the Linux kernel and ten CWE categories. Pair accuracy counts a pair as correct only when **both** the vulnerable and patched function are classified correctly.

| Same reported model: GPT-4o | Pair accuracy | Exact location |
|---|---:|---|
| Basic prompt | 0.08 = 8% | Table 1 |
| Code-level RAG | 0.05 = 5% | Table 4 |
| Knowledge-level Vul-RAG | 0.32 = 32% | Table 4 |

Recommended chart: **8% → 32%, +24 percentage points**, labeled **“Published research: GPT-4o on PairVul”** and **“Pair accuracy; higher is better.”** Alternatively compare 5% and 32% from Table 4 only. This is an external benchmark, not the student's CI results or a general detection guarantee. Omit manual-confirmation figures, which are unnecessary here.

## Related AI-assisted SAST evidence: IRIS

[IRIS, official ICLR 2025 proceedings](https://proceedings.iclr.cc/paper_files/paper/2025/hash/582d4e27fa24168f3af1f4582655034b-Abstract-Conference.html), by Ziyang Li, Saikat Dutta, and Mayur Naik, combines LLM-inferred taint specifications and contextual analysis with static analysis. Its CWE-Bench-Java contains 120 manually validated vulnerabilities in real-world Java projects. The abstract reports **CodeQL: 27 detected; IRIS with GPT-4: 55 detected**.

Use IRIS as evidence that LLM assistance and program analysis can complement each other. **This is not a direct RAG-versus-no-RAG benchmark**, and it does not establish the student's implementation, language, or use of CodeQL. Vul-RAG is the better numerical evidence for the RAG research slide.

## Personal workflow: confirmed core and illustrative detail

High-level diagram consistent with the user's account:

**Code in CI → Retrieve relevant security knowledge → AI-assisted static analysis → Findings for developer review.**

The first three stages are supported at a high level by the user's description. A detailed report schema, automatic gating, changed-files-only scans, and particular retrieval internals remain illustrative choices unless confirmed.

If code is useful visually, use language-neutral pseudocode. This is an **illustrative flow, not the student's actual source code or a working SDK example**:

```text
for each code unit selected for analysis:
    knowledge = retrieve relevant security references
    finding = assess code using that knowledge
    record finding and supporting references
review findings before making security decisions
```

This pseudocode deliberately assumes no AST, language, database, model API, or CI vendor.

### Optional teaching example

A short SQL-injection illustration can explain the knowledge/code connection: code mixes user-controlled input into an SQL statement; a retrieved reference explains the weakness and recommends separating values from SQL structure through parameterization. Label it **Illustrative example**, not a finding from the student's scanner.

Primary support: [MITRE CWE-89](https://cwe.mitre.org/data/definitions/89.html), especially Description and Potential Mitigations. [OWASP A03:2021 Injection](https://top10.owasp.org/2021/A03_2021-Injection/) explicitly discusses placing SAST, DAST, and IAST in CI/CD. A source reference may support an explanation, but the presence of a citation does not prove that a model's finding is correct.

## GraphRAG and Agentic RAG in the personal module

The user explicitly clarified that both GraphRAG and Agentic RAG were part of the implementation and requested AG2 and FastMCP as stack examples. Explain their high-level responsibilities as implemented approaches. Detailed graph nodes and tool calls on explanatory diagrams remain illustrative; no particular database, provider, number of agents, or quality metric was reported.

## Limits and honest evaluation

RAG can retrieve irrelevant or outdated security advice. LLM analysis can produce false positives and false negatives. Source code comments and retrieved documents may contain prompt injection; [OWASP LLM01:2025](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) states that RAG does not fully remove that risk and recommends clear trust boundaries, least privilege, and human approval for sensitive actions.

Proposed future evaluation: a labeled test set, precision and recall for findings, citation support, runtime, and cost. Do not invent scores, numbers of vulnerabilities found, speedups, or claims of outperforming established SAST. No test results are confirmed for the personal module.

## Screenshot choices for the actual story

1. **CWE-89 page**: capture the real English title, definition, and/or parameterization mitigation. This is relevant to the scanner's knowledge, rather than a SOC incident screen.
2. **Vul-RAG Table 4**: capture the original paper table with its title, or show a genuine paper screenshot beside an editable chart with accurate attribution.
3. A student's own CI screenshot can be used only if provided later. Do not fabricate a GitHub Actions run or scanner output.

The CWE and paper HTML sources were opened and checked. **No new browser screenshots were produced by this research task.**

## Claim–source mapping

| Claim | Evidence | Scope |
|---|---|---|
| The student configured RAG and wrote a CI scanning module. | User's explicit account, relayed by parent. | Personal implementation, high level only. |
| OWASP, CWE, and CVE serve different roles. | OWASP project page; MITRE CWE About and FAQ. | Terminology; does not prove all were ingested. |
| Knowledge-level RAG can improve vulnerability classification in a reported experiment. | Vul-RAG v3 Tables 1 and 4; §3.1.2–3.1.3. | PairVul / reported GPT-4o results only. |
| LLM assistance can complement static analysis. | IRIS ICLR 2025 abstract. | Java benchmark; not direct RAG evidence. |
| SQL injection involves mixing untrusted input with SQL structure. | MITRE CWE-89; OWASP A03:2021. | Illustrative teaching example. |
| Static security testing can be included in CI/CD. | OWASP A03:2021 Description. | General practice; no vendor assumption. |
| RAG does not eliminate prompt injection. | OWASP LLM01:2025. | Limitation and proposed safeguards. |
| GraphRAG and Agentic RAG were part of the module; AG2 and FastMCP were named as stack components. | User clarification. | Personal account; exact internals unspecified. |

The previous SOC research is optional background only. Microsoft grounding/plugins are not proof of any specific internal RAG architecture and are not needed in the twelve-slide CI story.
