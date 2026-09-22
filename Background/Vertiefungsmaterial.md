---
title: "Vertiefungsmaterial: HTTP, CTF, Agenten, Frontier-Sicherheit"
date: 2026-09-21
tags:
  - workshop
  - cyberraum
  - studienstiftung
---

# Vertiefungsmaterial für die AG Cyberraum

Kuratierte Ressourcen zum Nach- und Weiterarbeiten nach dem Workshop.
Die Rückmeldung war, dass wir wegen der Kürze durch die technischen Teile rushen mussten.
Diese Seite hängt jede Vertiefung an den Slot, in dem das Thema vorkam, und mischt Tutorials, CTF-Ressourcen mit weiteren Challenges und Paper zu Agenten und LLMs.
Jeder Eintrag ist mit `(Einstieg)` oder `(Vertiefung)` markiert, damit ihr euren Einstiegspunkt selbst wählt.
Fangt bei jedem Thema mit den `(Einstieg)`-Ressourcen an und geht dann in die Paper.

Verwandte Workshop-Dokumente: [Aufgabenblatt und CTF-Challenges](../Challenges/Aufgabenblatt.md), [ReAct-Agent](../Agent/README.md) und [Folien](../Slides/).

> [!tip] Wenn ihr nur wenig Zeit habt
> Lest die vier Kernpaper [weiter unten](#die-vier-kernpaper) und arbeitet euch durch **eine** CTF-Plattform aus [Zum Weiterüben](#zum-weiterüben-slot-übergreifend).

## Slot 0 und 1: Web Security, HTTP und Juice Shop

Zu [Slot 1](../Slides/Slot-1-Web-Security-Beobachten-und-Verstehen.pptx) und den Aufgaben **Confidential Document** und **Login Admin**.

### HTTP-Grundlagen: Browser, Server, Request und Response

- **[An overview of HTTP (MDN)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview)** · Client-Server-Modell und Grundablauf, deckt den Einstiegsteil des HTTP-Slots ab _(Einstieg)_.
- **[HTTP request methods (MDN)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods)** · Definiert GET, POST, PUT und mehr, also die GET-vs-POST-Unterscheidung und die Grundlage für die PUT-Tampering-Aufgabe _(Einstieg)_.
- **[HTTP response status codes (MDN)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status)** · Vollständige Liste der 1xx bis 5xx Codes mit Bedeutung _(Einstieg)_.
- **[HTTP messages (MDN)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Messages)** · Genauer Aufbau von Request und Response aus Startzeile, Headern und Body _(Vertiefung)_.
- **[curl Tutorial (offiziell)](https://curl.se/docs/tutorial.html)** · Offizielle Einführung in curl von der Kommandozeile, direkter Bezug zur `curl -v`-Übung _(Einstieg)_.
- **[The Art Of Scripting HTTP Requests Using curl](https://curl.se/docs/httpscripting.html)** · GET vs POST, Header und Datenübermittlung per curl, für Requests jenseits des Browsers _(Vertiefung)_.

### Authentifizierung gegen Autorisierung

- **[Authn vs. authz (Cloudflare Learning)](https://www.cloudflare.com/learning/access-management/authn-vs-authz/)** · "Wer bist du" gegen "was darfst du" mit Alltagsanalogie, genau die Slot-Unterscheidung _(Einstieg)_.
- **[Authentication vs. Authorization (Auth0)](https://auth0.com/intro-to-iam/authentication-vs-authorization)** · Komplementäre Erklärung mit Bezug zu RBAC und Least Privilege _(Einstieg)_.

### Broken Access Control und IDOR (Aufgabe Confidential Document)

- **[A01:2021 Broken Access Control (OWASP Top 10)](https://owasp.org/Top10/2021/A01_2021-Broken_Access_Control/)** · Die Nummer-1-Web-Schwachstelle inklusive "force browsing to privileged pages", ordnet Confidential Document ein _(Vertiefung)_.
- **[Insecure direct object references, IDOR (PortSwigger)](https://portswigger.net/web-security/access-control/idor)** · Erklärt IDOR präzise und verlinkt eigene Übungslabs, direkte Vertiefung zu Confidential Document _(Vertiefung)_.

### SQL Injection (Aufgabe Login Admin)

- **[Running an SQL Injection Attack (Computerphile, Mike Pound)](https://www.youtube.com/watch?v=ciNHn38EyRc)** · Anschauliche Video-Demo, niedrigschwelliger Einstieg ohne Vorkenntnisse _(Einstieg)_.
- **[What is SQL Injection? (PortSwigger)](https://portswigger.net/web-security/sql-injection)** · Systematisch inklusive Login-Bypass, UNION und blind SQLi _(Vertiefung)_.
- **[Lab: SQL injection login bypass (PortSwigger)](https://portswigger.net/web-security/sql-injection/lab-login-bypass)** · Interaktives Lab genau zum Muster von Login Admin (`' OR 1=1--`) zum eigenständigen Nachüben _(Vertiefung)_.
- **[SQL Injection Prevention Cheat Sheet (OWASP)](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)** · Die Verteidigungsseite mit Prepared Statements, ergänzt die Angriffssicht um "wie verhindert man es" _(Vertiefung)_.

### HTTP-Methoden und Tampering (Aufgabe Product Tampering, Slot 4)

- **[Web Parameter Tampering (OWASP)](https://community.owasp.org/attacks/Web_Parameter_Tampering)** · Grundprinzip der Manipulation von Parametern wie Preisen und Rechten, das Konzept hinter Product Tampering _(Vertiefung)_.
- **[Mass Assignment Cheat Sheet (OWASP)](https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html)** · Warum ungeschützte PUT/POST-Felder überschrieben werden können und wie man es per Allow-List verhindert _(Vertiefung)_.

### OWASP Juice Shop

- **[OWASP Juice Shop Homepage](https://juice-shop.github.io/juice-shop/)** · Projektseite der verwundbaren App aus dem Workshop, Startpunkt für alles Weitere _(Einstieg)_.
- **[Learning, OWASP Juice Shop](https://juice-shop.github.io/tab_learning.html)** · Bündelt die Hacking-Instructor-Tutorials direkt in der Instanz, ideal ohne CTF-Erfahrung _(Einstieg)_.
- **[juice-shop/juice-shop (GitHub)](https://github.com/juice-shop/juice-shop)** · Repo mit `docker run`- und npm-Anleitung zum lokalen Starten der eigenen Instanz _(Einstieg)_.
- **[Pwning OWASP Juice Shop, Companion Guide](https://pwning.owasp-juice.shop/companion-guide/latest/introduction/README.html)** · Offizielles Begleitbuch von Björn Kimminich mit Hinweisen und vollständigen Lösungen zu jeder Challenge _(Vertiefung)_.

## Slot 2 und 3: LLM-Agenten und der ReAct-Zyklus

Zu [Slot 2](../Slides/Slot-2-Sprachmodell-Skript-Agent-ReAct.pptx), [slot2_agent.py](../Agent/slot2_agent.py) und [slot3_agent.py](../Agent/slot3_agent.py).

### Agenten-Grundkonzepte (Sprachmodell, Skript, Agent)

- **[Building Effective AI Agents (Anthropic)](https://www.anthropic.com/engineering/building-effective-agents)** · Trennt Workflows von echten Agenten und zeigt, wann ein Agent überhaupt sinnvoll ist, Rahmen für die Slot-2-Unterscheidung _(Einstieg)_.
- **["agent" may finally have a widely agreed upon definition (Simon Willison)](https://simonwillison.net/2025/Sep/18/agents/)** · Prägt die knappe Definition "an LLM agent runs tools in a loop to achieve a goal", das "in a loop" ist unsere ReAct-Schleife _(Einstieg)_.
- **[How We Build Effective Agents, Barry Zhang (Anthropic, Video)](https://www.youtube.com/watch?v=D7_ipDqhtwk)** · Talk zu Designprinzipien wie Einfachheit und Agenten-Perspektive _(Einstieg)_.
- **[LLM Powered Autonomous Agents (Lilian Weng)](https://lilianweng.github.io/posts/2023-06-23-agent/)** · Kanonischer Überblick über Planning, Memory und Tool Use mit dem LLM als Controller _(Vertiefung)_.

### ReAct, Tool Use und Function Calling

- **[ReAct Projektseite](https://react-lm.github.io/)** · Interaktive Thought/Action/Observation-Trajektorien, visualisiert genau den in Slot 2 nachgebauten Zyklus _(Einstieg)_.
- **[How tool use works (Claude Docs)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works)** · Das LLM führt Tools nie selbst aus, sondern gibt eine strukturierte Anfrage zurück, die euer Code ausführt, deckt Aktionsformat und Observation aus Slot 2/3 ab _(Einstieg)_.
- **[Function calling (OpenAI Docs)](https://developers.openai.com/api/docs/guides/function-calling)** · Tools als JSON-Schema, zweite Anbieterperspektive zum nativen Tool Use _(Einstieg)_.
- **[Writing effective tools for AI agents (Anthropic)](https://www.anthropic.com/engineering/writing-tools-for-agents)** · Wie man Tool-Beschreibungen und Schemata schreibt, damit das Modell zuverlässig aufruft, passt zu Tool-Adapter und System-Prompt _(Vertiefung)_.

### Selbst einen Agenten bauen

- **[A Super Simple ReAct Agent from Scratch (sesen.ai)](https://sesen.ai/blog/react-agent-from-scratch)** · ReAct-Loop in 31 Zeilen mit Scratchpad-Memory, Schrittlimit und drei bewussten Fehlermodi, praktisch deckungsgleich mit Slot 3 _(Vertiefung)_.
- **[Building an AI agent with tool use in Python, from scratch (dev.to)](https://dev.to/ayinedjimi-consultants/building-an-ai-agent-with-tool-use-in-python-from-scratch-no-framework-4efk)** · Minimaler Agent in rund 150 Zeilen mit Tool-Registry und Dispatcher, genau der Slot-3-Bauplan _(Vertiefung)_.
- **[Create ReAct AI Agent from Scratch (shafiqulai)](https://shafiqulai.github.io/blogs/blog_3.html)** · Ausführlicher, mit Thought-Action-PAUSE-Observation-Prompt, JSON-Parsing und max_iterations _(Vertiefung)_.
- **[Agents (LangChain OSS Docs)](https://docs.langchain.com/oss/python/langchain/agents)** · `create_agent` implementiert das ReAct-Muster, Kontrast zum handgebauten Loop und was ein Framework abstrahiert _(Einstieg)_.
- **[Hugging Face AI Agents Course](https://huggingface.co/learn/agents-course/en/unit0/introduction)** · Kostenloser Kurs mit lauffähigen Notebooks über smolagents, LlamaIndex und LangGraph _(Einstieg)_.
- **[Claude Cookbooks, tool_use (GitHub)](https://github.com/anthropics/claude-cookbooks/tree/main/tool_use)** · Lauffähige Notebooks zu Calculator-Tool, Kundenservice-Agent und SQL _(Vertiefung)_.

### Paper zu Reasoning und Agenten

- **[Chain-of-Thought Prompting Elicits Reasoning in LLMs](https://arxiv.org/abs/2201.11903)** · Wei et al. 2022, arXiv:2201.11903 · Zwischenschritte verbessern komplexes Reasoning, die Grundlage für das "Thought" im ReAct-Zyklus _(Vertiefung)_.
- **[ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)** · Yao et al. 2022/2023 (ICLR 2023), arXiv:2210.03629 · Verschränkt Reasoning-Traces mit Aktionen und reduziert Halluzination, das namensgebende Kernpaper _(Vertiefung)_.
- **[MRKL Systems](https://arxiv.org/abs/2205.00445)** · Karpas et al. 2022, arXiv:2205.00445 · Router plus Experten- und Tool-Module, frühe Blaupause für die Tool-Adapter-Idee _(Vertiefung)_.
- **[Toolformer: Language Models Can Teach Themselves to Use Tools](https://arxiv.org/abs/2302.04761)** · Schick et al. 2023, arXiv:2302.04761 · LLM lernt selbstüberwacht, wann welche API mit welchen Argumenten aufzurufen ist _(Vertiefung)_.
- **[Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366)** · Shinn et al. 2023 (NeurIPS 2023), arXiv:2303.11366 · Agent reflektiert verbal über Feedback, natürliche Erweiterung des ReAct-Loops um Selbstkorrektur _(Vertiefung)_.
- **[A Survey on LLM based Autonomous Agents](https://arxiv.org/abs/2308.11432)** · Wang et al. 2023, arXiv:2308.11432 · Einheitliches Framework für Konstruktion, Anwendung und Evaluation von LLM-Agenten _(Vertiefung)_.
- **[The Rise and Potential of LLM Based Agents: A Survey](https://arxiv.org/abs/2309.07864)** · Xi et al. 2023, arXiv:2309.07864 · Breiter Überblick über Brain-, Perception- und Action-Aufbau und Agenten-Gesellschaften _(Vertiefung)_.

## Slot 4: Vom Eigenbau zum Cybersecurity-Framework (CAI)

Zu [Slot 4](../Slides/Slot-4-CAI-Frameworkvergleich_v8.pptx) und dem Vergleich Eigenbau gegen CAI.

### CAI, das Framework aus dem Workshop

- **[CAI GitHub (aliasrobotics/cai)](https://github.com/aliasrobotics/cai)** · Quellcode mit den Agentenprofilen `one_tool_agent`, `blueteam_agent`, `bug_bounter_agent` und `redteam_agent` sowie CLI-, API- und SDK-Ausführung _(Einstieg)_.
- **[CAI Dokumentation](https://aliasrobotics.github.io/cai/)** · Erklärt genau die Slot-4-Konzepte Agentenauswahl, Handoffs und Orchestrierung samt Laufzeit und Beobachtbarkeit _(Einstieg)_.
- **[How to Build Advanced Cybersecurity AI Agents with CAI (MarkTechPost)](https://www.marktechpost.com/2026/03/29/how-to-build-advanced-cybersecurity-ai-agents-with-cai-using-tools-guardrails-handoffs-and-multi-agent-workflows/)** · Schritt-für-Schritt-Tutorial zum selben Werkzeugraum- und Handoff-Aufbau _(Einstieg)_.
- **[CAI: An Open, Bug Bounty-Ready Cybersecurity AI](https://arxiv.org/abs/2504.06017)** · Mayoral-Vilches et al. 2025, arXiv:2504.06017 · Das offizielle CAI-Paper mit modularer Agentenarchitektur, Guardrails und Human-in-the-Loop _(Vertiefung)_.

### Weitere LLM-Pentest-Werkzeuge zum Vergleich

- **[hackingBuddyGPT (GitHub)](https://github.com/ipa-lab/hackingBuddyGPT)** · "LLM-Hacking in unter 50 Zeilen", ideal als Eigenbau-Gegenbeispiel zu CAI, Paper [Getting pwn'd by AI](https://arxiv.org/abs/2308.00121) (Happe & Cito, FSE 2023) _(Einstieg)_.
- **[Nebula (BerylliumSec)](https://github.com/berylliumsec/nebula)** · CLI-Assistent für Recon und Schwachstellenanalyse mit lokaler oder Cloud-LLM-Anbindung _(Einstieg)_.
- **[PentestGPT (GitHub)](https://github.com/GreyDGL/PentestGPT)** · Staged Reasoning/Generation/Parsing für automatisiertes Pentesting, prominentestes Vergleichsobjekt zu CAI, Paper [arXiv:2308.06782](https://arxiv.org/abs/2308.06782) (Deng et al., USENIX Security 2024) _(Vertiefung)_.
- **[Vulnhuntr (Protect AI)](https://github.com/protectai/vulnhuntr)** · LLM plus statische Analyse verfolgt Datenflüsse von Input bis Sink und meldete autonom gefundene 0-days _(Vertiefung)_.
- **[EnIGMA](https://arxiv.org/abs/2409.16165)** · Abramovich et al. 2025 (ICML), arXiv:2409.16165 · CTF-Agent mit interaktiven Tools, belegt warum der Werkzeugraum über den Erfolg entscheidet, der Kern des Slot-4-Vergleichs _(Vertiefung)_.

### Paper: können Agenten autonom hacken?

- **[LLM Agents can Autonomously Hack Websites](https://arxiv.org/abs/2402.06664)** · Fang et al. 2024, arXiv:2402.06664 · GPT-4-Agenten hacken Webseiten ohne Vorwissen über die Lücke, unter anderem blinde SQL-Injection _(Vertiefung)_.
- **[LLM Agents can Autonomously Exploit One-day Vulnerabilities](https://arxiv.org/abs/2404.08144)** · Fang et al. 2024, arXiv:2404.08144 · GPT-4 exploitet 87 Prozent von 15 realen CVEs allein aus der Beschreibung, das Standard-Referenzpaper _(Vertiefung)_.
- **[Hacking CTFs with Plain Agents](https://arxiv.org/abs/2412.02776)** · Turtayev et al. (Palisade Research) 2024, arXiv:2412.02776 · 95 Prozent auf InterCode-CTF mit einem simplen ReAct-Agenten, starkes Argument für den Eigenbau-gegen-Framework-Vergleich _(Vertiefung)_.

### Benchmarks für Cybersecurity-Agenten

- **[InterCode](https://arxiv.org/abs/2306.14898)** · Yang et al. 2023, arXiv:2306.14898, [Repo](https://github.com/princeton-nlp/intercode) · Container-basierte CTF-Umgebung, niedrigschwelliger Einstieg zum Laufenlassen eigener Agenten _(Einstieg)_.
- **[Cybench](https://arxiv.org/abs/2408.08926)** · Zhang et al. (Stanford) 2024 (ICLR 2025), arXiv:2408.08926 · 40 professionelle CTF-Aufgaben mit Subtask-Zerlegung, De-facto-Standard zur Einordnung von Agenten wie CAI _(Vertiefung)_.
- **[NYU CTF Bench](https://arxiv.org/abs/2406.05590)** · NYU 2024 (NeurIPS 2024), arXiv:2406.05590 · Erster CTF-Benchmark speziell für offensive Security-Agenten mit Tool-Anbindung _(Vertiefung)_.
- **[AutoPenBench](https://arxiv.org/abs/2410.03225)** · 2024, arXiv:2410.03225 · 33 verwundbare Systeme, kontrastiert vollautonome mit assistierten Agenten und quantifiziert die Grenzen autonomer Pentests _(Vertiefung)_.

## Slot 5: Frontier-Modelle, Fähigkeiten und Safety

Zu [Slot 5](../Slides/Slot-5-OpenAI-Hugging-Face-Vorfall-Serify-Master.pptx) und dem Sprachmodell als Entscheidungskern.

- **[Introducing the Frontier Safety Framework (Google DeepMind)](https://deepmind.google/blog/introducing-the-frontier-safety-framework/)** · "Critical Capability Levels" inklusive der Schwelle vollautomatisierter Cyberangriffe, liefert das Vokabular, ab wann ein stärkeres Modell zum Risiko wird ([Update](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/)) _(Einstieg)_.
- **[From Naptime to Big Sleep (Google Project Zero)](https://projectzero.google/2024/10/from-naptime-to-big-sleep.html)** · Erster öffentlich dokumentierter Fund einer echten unbekannten Speicherlücke in SQLite durch einen KI-Agenten, anschauliche defensive Perspektive _(Einstieg)_.
- **[Responsible Scaling Policy (Anthropic)](https://www.anthropic.com/responsible-scaling-policy)** · Definiert AI Safety Levels und Capability Thresholds unter anderem für autonome Cyberoperationen, der Rahmen hinter dem Entscheidungskern-Risiko _(Vertiefung)_.
- **[Preparedness Framework v2 (OpenAI)](https://openai.com/index/updating-our-preparedness-framework/)** · Konkrete Cyber-Fähigkeitsschwellen bis zu autonomer End-to-End-Angriffsstrategie, direkter Gegenpol zur Fallstudie, in der Ziel und Rechte gerade nicht begrenzt waren _(Vertiefung)_.
- **[Evaluating Frontier Models for Dangerous Capabilities](https://arxiv.org/abs/2403.13793)** · Phuong et al. (Google DeepMind) 2024, arXiv:2403.13793 · Erstes systematisches Programm für "dangerous capability evals", zeigt methodisch, wie man offensive KI-Fähigkeiten misst _(Vertiefung)_.
- **[A Framework for Evaluating Emerging Cyberattack Capabilities of AI](https://arxiv.org/abs/2503.11917)** · Rodriguez et al. (Google) 2025, arXiv:2503.11917 · Wertet über 12.000 reale Vorfälle aus und identifiziert, welche Angriffsphasen KI beschleunigt, verbindet Fähigkeitsschwellen mit realen Ketten _(Vertiefung)_.

## Slot 6: Prompt Injection, Multi-Agenten und hybride Bedrohungen

Zu [Slot 6](../Slides/Slot-6-Wenn-Agenten-auf-Agenten-treffen.pptx) und den Aufgaben zur Fallstudie im [Aufgabenblatt](../Challenges/Aufgabenblatt.md).

### Prompt Injection gegen den Analyseagenten

- **[The lethal trifecta for AI agents (Simon Willison)](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)** · Eingängiges Modell, wann ein Agent durch Prompt Injection wirklich gefährlich wird, idealer Einstieg vor der Demo mit dem defensiven Analyseagenten _(Einstieg)_.
- **[OWASP Top 10 for LLM Applications 2025 (PDF)](https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf)** · Prompt Injection auf Platz 1, erklärt warum Instruktionen und Daten im selben Kanal die Wurzel des Problems sind, plus Gegenmaßnahmen _(Einstieg)_.
- **[MITRE ATLAS](https://atlas.mitre.org/)** · ATT&CK-artige Wissensbasis mit Techniken gegen KI-Systeme wie Prompt Crafting und RAG Poisoning plus reale Case Studies, Landkarte für Angriffe auf den Entscheidungskern _(Einstieg)_.
- **[Not what you've signed up for (Indirect Prompt Injection)](https://arxiv.org/abs/2302.12173)** · Greshake et al. 2023, arXiv:2302.12173 · Die Referenzarbeit zu indirekter Prompt Injection, genau das Muster hinter dem manipulierten Erstbericht in Aufgabe 2/3 _(Vertiefung)_.
- **[AgentDojo](https://arxiv.org/abs/2406.13352)** · Debenedetti et al. 2024, arXiv:2406.13352 · 97 realistische Agenten-Tasks plus 629 Security-Testfälle, zeigt experimentell, wie Tool-Daten den Agenten kapern, anschlussfähig an Vertrauens- und Autoritätsgrenzen _(Vertiefung)_.

### Multi-Agenten-Systeme und Swarms

- **[LLM based Multi-Agents: A Survey of Progress and Challenges](https://arxiv.org/abs/2402.01680)** · Guo et al. 2024 (IJCAI), arXiv:2402.01680 · Überblick zu Kommunikation, Rollen und Koordination, Grundlage um agentische Swarms einzuordnen _(Einstieg)_.
- **[Teams of LLM Agents can Exploit Zero-Day Vulnerabilities (HPTSA)](https://arxiv.org/abs/2406.01637)** · Zhu, Fang et al. 2024, arXiv:2406.01637, [Code](https://github.com/uiuc-kang-lab/HPTSA) · Planungsagent orchestriert Subagenten und knackt reale Zero-Days besser als Einzelagenten, die konkrete Blaupause für Swarms in Slot 6 _(Vertiefung)_.
- **[A Survey on Trustworthy LLM Agents: Threats and Countermeasures](https://arxiv.org/abs/2503.09648)** · Zhang et al. 2025, arXiv:2503.09648 · Threat- und Defense-Taxonomie für Einzel- und Multi-Agenten inklusive Memory- und Koordinationsrisiken, vertieft Eskalation und Fehlerfortpflanzung _(Vertiefung)_.
- **[A Survey on Agentic Security: Applications, Threats and Defenses](https://arxiv.org/abs/2510.06445)** · Shahriar et al. 2025, arXiv:2510.06445 · Taxonomie aus über 260 Arbeiten zu Agenten in Cybersecurity, deckt Angriffs- und Verteidigungsseite ab _(Vertiefung)_.
- **[Large Language Models are Autonomous Cyber Defenders](https://arxiv.org/abs/2505.04843)** · Castro et al. 2025, arXiv:2505.04843 · LLMs als Verteidiger in einer Multi-Agenten-Umgebung (CybORG CAGE 4), direkte Entsprechung zur KI-gestützten Incident Response in Slot 6 _(Vertiefung)_.

### KI in Cyber und hybride Bedrohungen (reale Einordnung)

- **[Wie KI die Cyberbedrohungslandschaft verändert (BSI, deutsch)](https://www.bsi.bund.de/DE/Service-Navi/Presse/Pressemitteilungen/Presse2024/240430_Paper_Einfluss_KI_Cyberbedrohungslage.html)** · Deutsche Behördenperspektive, muttersprachliche Brücke für die Einordnung ohne Security-Vorwissen _(Einstieg)_.
- **[The near-term impact of AI on the cyber threat, now to 2027 (UK NCSC)](https://www.ncsc.gov.uk/report/impact-ai-cyber-threat-now-2027)** · KI macht Angriffe effektiver und senkt die Einstiegshürde, nüchterner Rahmen für die Bedrohungsdiskussion _(Einstieg)_.
- **[ENISA Threat Landscape 2025](https://www.enisa.europa.eu/publications/enisa-threat-landscape-2025)** · EU-Lagebild auf Basis von 4.875 Vorfällen, verbindet KI-Cyber mit hybriden und Influence-Aspekten _(Einstieg)_.
- **[Disrupting the first reported AI-orchestrated cyber espionage campaign (Anthropic)](https://www.anthropic.com/research/disrupting-AI-espionage)** · Realer Fall GTG-1002, in dem ein Agent 80 bis 90 Prozent der Angriffskette autonom ausführte, das reale Gegenstück zur fiktiven Fallstudie _(Einstieg)_.
- **[Adversarial Misuse of Generative AI (Google GTIG)](https://cloud.google.com/blog/topics/threat-intelligence/adversarial-misuse-generative-ai)** · Wie staatliche Akteure generative KI operativ nutzen, empirische Erdung für die Frage, was KI-Offensive heute real leistet _(Einstieg)_.
- **[From Prompting to Autonomy (Google GTIG, Nov 2025)](https://cloud.google.com/blog/topics/threat-intelligence/from-prompting-to-autonomy-the-evolution-of-adversarial-ai)** · Dokumentiert Malware, die zur Laufzeit LLM-APIs aufruft, belegt die Slot-5-These vom Strategiewechsel und längeren Zielverfolgung _(Vertiefung)_.
- **[3rd EEAS Report on FIMI Threats](https://www.eeas.europa.eu/sites/default/files/documents/2025/EEAS-3nd-ThreatReport-March-2025-05-Digital-HD.pdf)** · Analysiert die Infrastruktur staatlicher Desinformation samt KI-generierter Inhalte, deckt die hybride Informationsdimension ab, in der KI-Agenten Baustein einer Kampagne werden _(Einstieg)_.

## Zum Weiterüben (Slot-übergreifend)

Ihr habt im Workshop keine CTF-Erfahrung vorausgesetzt bekommen. Diese Plattformen bieten viele geführte Challenges zum selbstständigen Weiterüben.

- **[The CTF Primer (picoCTF)](https://primer.picoctf.com/)** · Erklärt das CTF-Format und die Aufgabenkategorien mit Walkthroughs, genau für den Einstieg ohne Vorerfahrung _(Einstieg)_.
- **[picoCTF (CMU)](https://picoctf.org/)** · Über 120 dauerhaft verfügbare, gestaffelte Challenges inklusive Web Exploitation, kostenloser Übungsplatz _(Einstieg)_.
- **[TryHackMe: OWASP Juice Shop](https://tryhackme.com/room/owaspjuiceshop)** · Halb geführter Raum mit gehosteter Juice-Shop-Instanz zu SQLi und Broken Access Control, direkte Brücke vom Workshop-Ziel _(Einstieg)_.
- **[OverTheWire: Bandit](https://overthewire.org/wargames/bandit/)** · Wargame für absolute Anfänger zu Linux- und Kommandozeilen-Grundlagen, die im Workshop kaum Platz hatten _(Einstieg)_.
- **[PortSwigger Web Security Academy](https://portswigger.net/web-security)** · Kostenlose, gestufte Labs zu jeder Web-Schwachstelle mit Lösungen, die tiefste frei verfügbare Web-Security-Ausbildung _(Vertiefung)_.
- **[Hack The Box Academy: Getting Started](https://academy.hackthebox.com/course/preview/getting-started)** · Strukturierter, praxisnaher Einstiegskurs, anspruchsvoller als TryHackMe und picoCTF, nächster Schritt für Motivierte _(Vertiefung)_.
- **[Root-Me](https://www.root-me.org/)** · Über 500 Challenges unter anderem zu Web-Server und Web-Client zum gezielten Weiterüben einzelner Kategorien _(Vertiefung)_.
- **[CTFtime](https://ctftime.org/)** · Kalender und Ranking aller weltweiten CTF-Wettbewerbe plus Writeup-Archiv, zeigt wo man live an echten CTFs teilnimmt _(Einstieg)_.

## Die vier Kernpaper

Wenn ihr nur vier Paper lest, dann diese, sie tragen die vier technischen Achsen des Workshops.

1. **[ReAct](https://arxiv.org/abs/2210.03629)** (Yao et al. 2022/2023): die Schleife aus Slot 2 und 3.
2. **[LLM Agents can Autonomously Exploit One-day Vulnerabilities](https://arxiv.org/abs/2404.08144)** (Fang et al. 2024): können Agenten autonom hacken, der Kern von Slot 4.
3. **[Not what you've signed up for](https://arxiv.org/abs/2302.12173)** (Greshake et al. 2023): indirekte Prompt Injection, der Angriff auf den Analyseagenten in Slot 6.
4. **[Teams of LLM Agents can Exploit Zero-Day Vulnerabilities](https://arxiv.org/abs/2406.01637)** (Zhu, Fang et al. 2024): agentische Swarms, die offene Frage aus Slot 5 und 6.
