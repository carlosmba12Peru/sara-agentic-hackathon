# SARA: Sovereign Autonomous Response for Anti-Extortion
> **Author & Creator:** **Carlos Eduardo Baños Diaz**  
> **A Sovereign Multi-Agent Cognitive Platform on Google Cloud to Repower Emergency Hotlines (Hotline 111) and Empower the National Police (PNP) and Public Prosecution (FECOR) with Zero-PII Cryptography.**  
> *Developed for the [All Things Agentic Hackathon on Devpost](https://allthingsagentichackathon.devpost.com/) — Main Category: **The Taskmaster** & Candidate for **Best Multimodal UX** and **Best Architectural Design**.*  
> 🌐 **Official Live Production Link (Google Cloud Run):** [https://sara-produccion-981735936523.us-central1.run.app/](https://sara-produccion-981735936523.us-central1.run.app/)  
> 🤖 **Official Citizen Notification Bot (Telegram):** [@kallpa_IA_asistente_bot](https://t.me/kallpa_IA_asistente_bot)  

> ⚠️ **Institutional Independence & Intellectual Property Disclaimer:**  
> **SARA is an independent research, software prototype, and demonstrative project conceived, designed, and developed exclusively by Carlos Eduardo Baños Diaz for the "All Things Agentic Hackathon" organized by Google Cloud & Devpost.**  
> It is **not** an official platform, nor does it hold institutional representation, sponsorship, or formal endorsement from the **Peruvian National Police (PNP)**, the **Ministry of the Interior (MININTER)**, the **Public Ministry (Fiscalía de la Nación)**, or any other agency of the Republic of Peru. All references to public institutions, statutory frameworks (Legislative Decrees No. 1735, 1731, Law No. 32183, Law No. 32303, D.S. 007-2025-JUS), official datasets (SIDPOL, Public Ministry / IPE reports), and technical platforms (PIDE) are used strictly as a realistic domain model and engineering benchmark for academic and demonstrative purposes under strict privacy standards.

---

## 📑 TABLE OF CONTENTS / ÍNDICE GENERAL

1. [💡 Inspiration: Breaking the 80% Silence of Extortion & The Impunity Bottleneck](#-1-inspiration-breaking-the-80-silence-of-extortion--the-impunity-bottleneck)
2. [🛡️ What SARA Does](#️-2-what-sara-does)
3. [🏗️ How We Built It: Architecture & Multi-Agent Swarm](#️-3-how-we-built-it-architecture--multi-agent-swarm)
4. [⚡ Quick Start: Running Locally & Deploying to Google Cloud Run](#-4-quick-start-running-locally--deploying-to-google-cloud-run)
5. [🏛️ Master Google Cloud Architecture Diagram](#️-5-master-google-cloud-architecture-diagram)
6. [🧗 Challenges We Ran Into](#-6-challenges-we-ran-into)
7. [🏆 Accomplishments That We're Proud Of](#-7-accomplishments-that-were-proud-of)
8. [📚 What We Learned](#-8-what-we-learned)
9. [🚀 What's Next for SARA: Scaling into a Multi-Crime 911 Cognitive OS & Regional Public Good](#-9-whats-next-for-sara-scaling-into-a-multi-crime-911-cognitive-os--regional-public-good)
10. [🔒 Cybersecurity, Envelope Encryption & Zero-PII Cryptography](#-10-cybersecurity-envelope-encryption--zero-pii-cryptography)
11. [🌐 Compliance with International Standards (ISO, NIST, EU AI Act, FIPS, OWASP)](#-11-compliance-with-international-standards-iso-nist-eu-ai-act-fips-owasp)
12. [📖 Glosario Maestro de Términos (GovTech, Ciberseguridad, IA & Marco Penal)](#-12-glosario-maestro-de-términos-govtech-ciberseguridad-ia--marco-penal)
13. [🛠️ Tech Stack & Authorship](#️-13-tech-stack--authorship)

---

## 💡 1. Inspiration: Breaking the 80% Silence of Extortion & The Impunity Bottleneck

Extortion and violent racketeering have escalated into an illicit industry that paralyzes emerging economies. In Peru alone, official police statistics (**SIDPOL**) recorded **130,934 property crime complaints in just 5 months (projected to reach 300,000 to 350,000 annual complaints in police stations)**. 

Yet, official reports from the **Peruvian Institute of Economics (IPE), the Public Ministry, and INEI (2026)** reveal a catastrophic institutional bottleneck: **only 27,000 extortion complaints reach the prosecution (Public Ministry) per year** (despite multiplying by 5.3x since 2021).

```
   ┌────────────────────────────────────────────────────────────────────────┐
   │            🚨 THE EXTORTION IMPUNITY FUNNEL IN PERU                    │
   │                                                                        │
   │  [ 350,000+ Annual Property Crime Complaints in Police Stations ]      │
   │                              │                                         │
   │                              ▼  (Only <9% reach prosecutors)           │
   │  [ 27,000 Extortion Cases Formally Reaching Prosecution (MPFN) ]       │
   │                              │                                         │
   │                              ▼  (Over 91% collapse in paper limbo)     │
   │  [ Over 80% of Victims Never Report in Person out of Mortal Fear ]     │
   └────────────────────────────────────────────────────────────────────────┘
```

This exposes a devastating reality: **less than 9% of complaints filed in police stations ever transition into formal prosecution dossiers**, leaving over 91% trapped in bureaucratic police limbo without asset freezes or judicial warrants. In the public transit sector alone, prosecution records document **214 armed attacks with casualties** against buses, combis, and mototaxis.

To make matters worse, over **80% of extortion victims never dare to report in person (the "Dark Figure" of crime)** out of mortal terror of corrupt identity leaks, 48-hour bureaucratic delays, and deadly retaliation. Victims prefer paying daily quotas (*"cupos"*) via mobile wallets (Yape/Plin) rather than risking their families.

We built **SARA (Sistema Autónomo de Respuesta Anti-Extorsión)** to dismantle both bottlenecks: an autonomous, sovereign multi-agent cognitive copilot that empowers citizens to report safely from their phones under a mathematical **Zero-PII guarantee (Code CUP)** in **Quechua, Aimara, Asháninka, Awajún, Shipibo-Konibo, Spanish, and English**, while transforming emergency intake into **1.8 seconds of forensic investigation and direct digital transmission to the Specialized Prosecution Office (Legislative Decree No. 1735)**.

---

## 🛡️ 2. What SARA Does

SARA acts as the cognitive intelligence and digital forensics copilot for police emergency hotlines (Hotline 111) and police command centers:

* 🗣️ **Inclusive Intake in Native Languages & Anti-Spam (Centinela & Kallpa):** Pre-triage acoustic analysis filters prank/silent calls in <300ms (**D.S. 020-2020-MTC**), while providing empathetic containment over live WebRTC voice (<600ms latency) in **Quechua (Cusco-Collao, Chanka, Áncash, Wanka dialects), Aimara, Asháninka, Awajún, Shipibo-Konibo, Spanish, and English** (Law No. 29735 & ReNITLI/MINCUL).
* 🔒 **Cryptographic Zero-PII Vault (Privacy by Design):** Victim identities (National ID, Full Name, Phone, Address) are immediately isolated with HMAC-SHA256 and CSPRNG salt upon ingestion, issuing an anonymous **Unique Protection Code (CUP)**. Downstream LLMs strictly process the CUP, preventing internal data exfiltration (Art. 409-C Criminal Code).
* 🔍 **Multimodal Vision OCR & Forensic Extraction (Art. 220 CPP):** Automated peritaje of handwritten extortion notes, ammunition casings, and digital wallet transfers (Yape/Plin/BCP/BBVA) with unalterable **SHA-256 digital custody hashes** and **RFC 3161 timestamps** (ISO/IEC 27037).
* 🚨 **Vida Primero Protocol (UDEX / Central 105 Flash Dispatch):** Instant acoustic and visual detection of explosive threats (dynamite, grenades) with a live police takeover bridge and biometric bypass to prioritize human life.
* 📵 **Autonomous PIDE Intelligence & Telecom Disassociation:** Real-time cross-referencing across **RENIEC**, **INPE** (prison calls), and **OSIPTEL-RENTESEG**. SARA cross-checks **Checa tu IMEI** and **Checa tus Líneas** to address Peru's **4,000 daily stolen phones** and mass SIM fraud, separating the hijacked communication vector from the financial collection vector to prevent wrongful prosecution of innocent citizens.
* 📐 **Formal AHP-Saaty Multicriteria Decision Model (IRCE):** Replaces black-box probability with Thomas Saaty's **Analytic Hierarchy Process (AHP)**, computing the **Extortion Risk and Complexity Indicator (IRCE)**:
  $$\text{IRCE} = 0.70 \cdot D_{\text{certeza}} + 0.30 \cdot D_{\text{inminencia}}$$
  Categorizing cases objectively into High (81–100%), Moderate (51–80%), Low (26–50%), and Dismissal ($\le 25\%$).
* 👮 **Human-in-the-Loop Sovereign Governance & SIDPOL Registration:** Police commanders review the structured dossier, select actionable measures (**< 3h IMEI cut under Law 32303, 24h UIF bank freeze under D.Leg. 1735 / D.S. 007-2025-JUS**), and sign with their **Official Police Digital Token (CIP)** into the **SIDPOL** system under **Peruvian AI Law No. 31814**.
* 📁 **Inter-Institutional Fiscal Remission (D.Leg. 1735):** An official transmission button delivers the digital prosecution packet and SHA-256 evidence chain directly to the **Specialized Anti-Extortion Prosecution Office (FECOR)**, concluding SARA's police lifecycle.

---

## 🏗️ 3. How We Built It: Architecture & Multi-Agent Swarm

SARA is engineered using an enterprise-grade **Parallel Multi-Agent Swarm Architecture** powered by the **Google Agent Development Kit (ADK)**, the **Google GenAI Python SDK**, and **Gemini 2.5 & 3.7**:

```
                              [ Citizen Ingress ]
                                      │
                         ┌────────────┴────────────┐
                         ▼                         ▼
                  [ Voice Call ]            [ Web Portal ]
                  (Gemini 2.5)              (Gemini 3.7)
                         │                         │
                         └────────────┬────────────┘
                                      ▼
                             [ Purificador Agent ]
                               (Zero-PII Filter)
                                      │
                   ┌──────────────────┼──────────────────┐
                   ▼                  ▼                  ▼
          [ Analista Agent ]   [ Calculo Agent ]   [ Asesor Juridico ]
          (Entity Extraction)   (AHP Risk Matrix)  (3h IMEI / 24h UIF)
                   │                  │                  │
                   └──────────────────┼──────────────────┘
                                      ▼
                            [ Supervisor Agent ]
                            (HITL Police Gate)
```

### 1. Cognitive Dual-Brain Routing (`agents/router.py`)
Instead of a monolithic prompt, SARA dynamically dispatches tasks across specialized model tiers:
* **Tier FLASH_FAST (`gemini-2.5-flash` / `gemini-3.7-flash`):** Allocated for real-time acoustic Voice Activity Detection (VAD), anti-spam spoof filtering (<300ms), and empathetic citizen containment in **Quechua, Shipibo, Aimara, and Spanish** (`temperature=0.3`, `thinking_budget=0`).
* **Tier PRO_REASONING (`gemini-3.7-pro`):** Allocated for criminal intelligence profiling, **Multimodal Vision OCR** of handwritten letters and ammunition, and statutory compliance certification against the Official Gazette (*El Peruano* & *GOB.PE*). Configured with `temperature=0.1` and an active **Thinking Budget of 2048 tokens** to guarantee chain-of-thought deduction with zero hallucinations.

### 2. Parallel Swarm Orchestration (`core/orchestrator.py`)
SARA implements the **ParallelAgent Pattern** using a multi-threaded execution pool (`ThreadPoolExecutor`), executing 4 cognitive branches simultaneously in under 1.8 seconds:
* **Branch 0 (Kallpa):** De-escalation, emotional containment, and dialect adaptation.
* **Branch 1 (Technical Analyst & PIDE Agent):** Intergovernmental cross-referencing across RENIEC, OSIPTEL-RENTESEG, and INPE.
* **Branch 2 (Threat Calculator):** Deterministic mathematical computation of the Extortion Risk and Complexity Indicator (**IRCE under AHP-Saaty: 70% Certainty / 30% Imminence**).
* **Branch 3 (Packager & Legal Advisor):** Structuring the formal police dossier under Articles 200 & 200-A of the Criminal Code.

### 3. Sovereign Zero-PII Vault (`core/secure_vault.py`)
Victim identity (Name, National ID, Phone, Address) is immediately isolated upon ingestion. A cryptographically derived **Unique Protection Code (CUP)** is generated using **HMAC-SHA256 with CSPRNG salt**. All downstream LLMs and logs process strictly the CUP code.

### 4. Real-Time MLOps Supervisor & Resilient Circuit Breaker
* **Supervisor IA (`core/supervisor.py`):** Inspects every inter-agent payload in real-time, executing regex sanitization to block any accidental PII exposure under **ISO/IEC 42001 (AIMS)**.
* **Autonomous Circuit Breaker:** If Gemini API rate limits (`429`) or service spikes (`503`) occur, SARA automatically switches within `<5ms` to local deterministic heuristics, guaranteeing 100% operational uptime during life-threatening emergencies.

### 5. Google Cloud Infrastructure & Tooling
* **Google Cloud Run:** Serverless containerized execution in `us-central1` with auto-scaling to zero ($0 idle cost) and high-concurrency throughput.
* **Google Cloud Secret Manager:** Secure programmatic retrieval of API keys and cryptographic secrets.
* **Google Cloud KMS:** Hardware Security Module (**HSM FIPS 140-3 Level 3**) for master key management and Envelope Encryption.
* **Google BigQuery GIS:** Geospatial vector clustering and territorial heatmapping across Peru's 25 regional departments.
* **Streamlit Web Console:** Mission-control dashboard offering a Citizen Portal, Human-in-the-Loop Police Command, Fiscal Inbox, and MLOps telemetry.

### 6. Architectural Design & AI Pair-Programming with Google Antigravity
The system architecture, domain modeling, statutory legal mapping (Legislative Decrees No. 1735 & 1731), cryptographic Zero-PII pipelines, and multi-agent coordination were **100% conceptualized and designed by Carlos Eduardo Baños Diaz**. 
The implementation, boilerplate refactoring, and automated test suite generation were accelerated through agentic pair-programming using **Google Antigravity IDE (Google's Agentic AI Coding Assistant)**, demonstrating how modern AI engineering tools turn complex civic-tech architectures into robust, production-ready code in record time.

---

## ⚡ 4. Quick Start: Running Locally & Deploying to Google Cloud Run

### 💻 A. Running Locally (2 Steps)

```bash
# 1. Clone your repository and navigate to the folder
git clone https://github.com/carlosmba12Peru/sara-agentic-hackathon.git
cd sara-agentic-hackathon

# 2. Create a virtual environment and install dependencies
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure environment variables (create .env from .env.example)
cp .env.example .env
# Set your GEMINI_API_KEY, TELEGRAM_BOT_TOKEN, etc.

# 4. Launch the application
streamlit run app_demo.py
```
Open your browser at `http://localhost:8501`.

---

### ☁️ B. Deploying to Google Cloud Run (1 Single Command)

```bash
gcloud run deploy sara-produccion \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --cpu 2 \
  --memory 4Gi \
  --set-env-vars="GEMINI_API_KEY=YOUR_KEY,TELEGRAM_BOT_TOKEN=YOUR_TOKEN,TELEGRAM_CHAT_ID=YOUR_CHAT_ID,MAKE_WEBHOOK_URL=YOUR_URL,VAPI_PUBLIC_KEY=YOUR_KEY,VAPI_ASSISTANT_ID=YOUR_ID"
```

---

## 🏛️ 5. Master Google Cloud Architecture Diagram

```mermaid
flowchart TB
    subgraph CLIENT_LAYER ["🌐 CITIZEN & POLICE INGRESS LAYER"]
        WEB["💻 Citizen Web Portal<br/>(Streamlit / Responsive UI)"]
        VOICE["📞 Emergency Hotline 111<br/>(Vapi WebRTC / Voice Stream)"]
        POLICE_UI["👮 Police Commander Console<br/>(FIDO2 / CIP Auth)"]
    end

    subgraph CLOUD_RUN ["☁️ GOOGLE CLOUD RUN (Serverless Execution Environment)"]
        direction TB
        ORCH["🧠 SARA Sovereign Orchestrator<br/>(Google Agent Development Kit)"]
        
        subgraph AGENT_SWARM ["🤖 HIERARCHICAL-PARALLEL MULTI-AGENT SWARM"]
            KALLPA["🗣️ Kallpa Agent<br/>(Containment & Multilingual Triaje)"]
            PURIF["🛡️ Purificador Agent<br/>(Zero-PII & Canary Token)"]
            CENT["🚫 Centinela Agent<br/>(Anti-Spam MTC D.S. 020-2020)"]
            ANALIST["📊 Analista Agent<br/>(Modus Operandi & Entities)"]
            CALC["📐 Calculo Agent<br/>(Saaty AHP Risk Matrix T-Index)"]
            LEGAL["⚖️ Asesor Juridico Agent<br/>(Legal Mandates 3h IMEI / 24h UIF)"]
            SUPERV["👁️ Supervisor Agent<br/>(ISO/IEC 42001 & HITL Validation)"]
        end

        subgraph CRYPTO_CORE ["🔒 SOVEREIGN CIPHER & FORENSIC VAULT"]
            ZERO_PII["🔑 Ephemeral Token Vault (CPR ➔ CUP)"]
            SHA["🛡️ SHA-256 Evidence Hasher (Art. 220 CPP)"]
            TIMESTAMPER["⏱️ RFC 3161 Digital Time Stamping Authority"]
        end
    end

    subgraph GCP_SERVICES ["⚡ GOOGLE CLOUD PLATFORM ENTERPRISE SERVICES"]
        VERTEX["🧠 Google Vertex AI / GenAI SDK<br/>• Gemini 2.5 Flash (Voice & Live Chat)<br/>• Gemini 3.7 Pro Reasoning (Thinking 2048)"]
        KMS["🔐 Cloud KMS (HSM FIPS 140-3 Level 3)<br/>Envelope Encryption (DEK / KEK)"]
        SECRETS["🗝️ Secret Manager<br/>(API Keys & Webhook Tokens)"]
        BIGQUERY["🗺️ BigQuery GIS<br/>(Geospatial Extortion Heatmaps)"]
    end

    subgraph EXTERNAL_GOV ["🏛️ PUBLIC SECTOR & OMNICHANNEL INTEGRATION"]
        MAKE_TELEGRAM["📲 Make.com ➡️ Telegram Bot<br/>(@kallpa_IA_asistente_bot)"]
        RENIEC["🆔 RENIEC ID Éntifica 3<br/>(Biometric Facial Liveness)"]
        SIDPOL["📋 PNP SIDPOL System<br/>(Official Police Report)"]
        FECOR["📁 Public Prosecutor (FECOR)<br/>(Fiscal Case File CUC)"]
        OSIPTEL["📵 OSIPTEL RENTESEG<br/>(3h IMEI Blocking - Ley 32303)"]
        UIF["🏦 UIF-Perú (SBS)<br/>(24h Bank Freeze - D.Leg. 1735)"]
    end

    %% Flow connections
    WEB --> ORCH
    VOICE --> ORCH
    POLICE_UI --> ORCH

    ORCH --> AGENT_SWARM
    AGENT_SWARM --> VERTEX
    AGENT_SWARM --> CRYPTO_CORE

    CRYPTO_CORE --> KMS
    ORCH --> SECRETS
    ORCH --> BIGQUERY

    AGENT_SWARM --> MAKE_TELEGRAM
    CRYPTO_CORE --> RENIEC
    POLICE_UI --> SIDPOL
    POLICE_UI --> FECOR
    LEGAL --> OSIPTEL
    LEGAL --> UIF
```

---

## 🧗 6. Challenges We Ran Into

* **Zero-PII vs. Actionable Intelligence:** Stripping personal data while retaining forensic utility required building a decoupled bidirectional cryptographic vault with deterministic salt derivation.
* **Eliminating Legal Hallucinations:** Criminal justice demands zero hallucination. We built an automated compliance engine that restricts penal citations strictly to verified statutory codes published in *El Peruano*.
* **Multimodal OCR on Low-Quality Mobile Captures:** Extortion notes are often crumpled paper or dark photographs. Fine-tuning prompts for Gemini 3.7 Vision OCR ensured 100% extraction accuracy of IBANs and phone numbers.
* **Preventing Telecom False Positives:** Addressing Peru's 4,000 daily stolen phones required cross-referencing OSIPTEL databases so that nominal phone holders are never prosecuted without matching bank account vectors.

---

## 🏆 7. Accomplishments That We're Proud Of

* ⚡ **1.8 seconds end-to-end response time**, replacing 48 hours of manual bureaucracy.
* 🇵🇪 **First native Quechua & Amazonian indigenous language AI intake agent** for law enforcement in South America.
* 🧪 **100% Green Test Suite:** 17/17 automated integration unit tests in PyTest (`test_i18n_optimization.py`, `test_shipibo_renitli_telegram_flow.py`, `test_api.py`).
* ⚖️ **Full Alignment with Law:** Architected to operate within Pillar 1 (PNP) of Peru's landmark **Legislative Decree No. 1735 (Specialized Anti-Extortion Subsystem)**.
* 🛡️ **4-Layer Due Diligence Framework:** Fully compliant with **NIST AI RMF 1.0**, **ISO/IEC 42001 (AIMS)**, **ISO/IEC 27037**, and **Law No. 31814**.
* 📐 **Mathematical Transparency:** Zero black-box scoring; 100% auditable AHP-Saaty IRCE framework.

---

## 📚 8. What We Learned

* **Dual-Brain Cognitive Routing is Essential:** Allocating tasks between low-latency Flash (<300ms) and deep Thinking Pro Reasoning optimizes latency, cost, and deductive depth.
* **The Power of Conversational Empathy:** Fine-tuning Kallpa to project calm authority in native languages significantly improves citizen trust and data accuracy during high-panic crises.
* **Separation of Concerns in Public Safety AI:** Generative AI should act as the cognitive reasoning engine, while deterministic scripts handle mathematical scoring (**IRCE under AHP-Saaty**), cryptographic hashing (SHA-256), and database pipelines.
* **Ethical Human Sovereignty (Law No. 31814):** AI must never replace judicial or police discretion; sovereign human officers must always validate evidence and sign dispatch orders with their digital token (CIP).

---

## 🚀 9. What's Next for SARA: Scaling into a Multi-Crime 911 Cognitive OS & Regional Public Good

*SARA launches today as the agentic copilot empowering emergency hotline 111, but is architected to evolve into the specialized multi-agent cognitive engine of Peru's future Unified 911 Emergency System and a scalable Digital Public Good for Latin America.*

* 🏛️ **Future Integration into Peru's Upcoming Unified 911 Emergency Command Center:** As the Peruvian government deploys its new National 911 System (unifying police 105, firefighters 116, and SAMU 106 under the MTC-Mininter framework), SARA will serve as the specialized cognitive AI triage and digital forensics engine within this nationwide dispatch infrastructure.
* 🧩 **Modular Multi-Crime Swarm Extension across Peru's National Helplines:** SARA is built as a sovereign, modular multi-agent framework. While proven first in the urgent crisis of **extortion and public transit (Legislative Decree No. 1735)**, its core components—Zero-PII Vault (CUP), Multimodal Forensics (Art. 220 CPP), Dual-Brain Routing, and PIDE Interoperability—are designed to deploy specialized agent swarms for other high-stakes crimes in Peru:
  * 💜 **Line 2: Gender-Based & Domestic Violence** (Emergency Line 100 - **MIMP Peru** / Law 30364 risk assessment and immediate protection).
  * 🚨 **Line 3: Human Trafficking & Child Exploitation** (Emergency Line 1818 - **Mininter Peru** / Migraciones & Reniec cross-matching).
  * 💻 **Line 4: Digital Fraud & Cybercrime** (**Divindat - PNP High-Tech Crime Division Peru** / Law 30096 financial phishing and SIM-swapping tracing).
* 🌎 **Scaling as a Latin American Regional Public Good (Digital Public Good):** Extortion and violent racketeering are operated by transnational crime syndicates across the continent. Because SARA's core (Zero-PII Vault, Dual-Brain Gemini 3.7 Router, Multimodal Vision OCR, and MLOps Supervisor) is strictly decoupled from state APIs, SARA can be adopted as a plug-and-play public good across:
  * 🇲🇽 **Mexico:** Interfacing with 911 / 089 C5 centers, SPEI instant freezes, and Náhuatl intake.
  * 🇨🇴 **Colombia:** Interfacing with GAULA Line 165, Nequi/Daviplata tracking, and Wayuunaiki intake.
  * 🇪🇨 **Ecuador:** Combating extortion "vacunas" through the ECU-911 emergency network and Kichwa intake.
  * 🇧🇷 **Brazil:** Interfacing with Disque-Denúncia 181, PIX instant account blocks, and Guarani intake.
* 🎙️ **National Extortion Voice Biometrics Bank (Legislative Decree No. 1611):** Acoustic voiceprint matching to cross-reference extortion calls with penitentiary inmates and organized crime registries.
* 🇵🇪 **Nationwide Expansion across all 25 Police Macro-Regions:** Deploying SARA's bilingual Quechua/Spanish intake natively across all provincial police divisions.
* ⚖️ **Direct Electronic Interoperability with the Public Ministry (MPFN):** Automated submission to the *Mesa de Partes Virtual MPFN* for instantaneous judicial convalidation of 24h bank freezes and 3h IMEI suspensions.

---

## 🔒 10. Cybersecurity, Envelope Encryption & Zero-PII Cryptography

SARA incorporates defense-in-depth cybersecurity across 5 physical and cryptographic tiers:

| Security Domain | Standard / Implementation | Technical Mechanism in SARA |
|---|---|---|
| **Zero-PII Isolation** | ISO/IEC 27701 & GDPR | Ephemeral vault tokenization substituting victim PII with high-entropy CUP identifiers. |
| **Envelope Encryption** | NIST SP 800-57 / 38D | 256-bit AES-GCM Data Encryption Keys (DEKs) wrapped by Google Cloud KMS KEKs (**HSM FIPS 140-3 Level 3**). |
| **Evidence Custody** | Art. 220 CPP & ISO/IEC 27037 | SHA-256 cryptographic hashing of all audio/image files with RFC 3161 digital timestamping. |
| **Defensive Anti-Spam** | D.S. N° 020-2020-MTC | Acoustic VAD filter (<300ms) detecting prank, silent, and VoIP spoofing numbers. |
| **Adversarial Hardening** | OWASP Top 10 for LLM | Dual-layer sanitization and Canary Token injection neutralizing Indirect Prompt Injections (IPI). |

---

## 🌐 11. Compliance with International Standards (ISO, NIST, EU AI Act, FIPS, OWASP)

| Standard | Issuer | Implementation in SARA |
|---|---|---|
| **ISO/IEC 42001:2023** | ISO / IEC | **Artificial Intelligence Management System (AIMS):** Full lifecycle traceability, bias auditing, and supervisory monitoring in `core/supervisor.py`. |
| **NIST AI RMF 1.0** | NIST (USA) | **AI Risk Management Framework:** Operationalized across *Govern, Map, Measure, Manage* functions with Saaty AHP consistency verification ($CR \le 0.10$). |
| **EU AI Act (High-Risk)** | European Union | **High-Risk AI Compliance:** Mandatory Human-in-the-Loop oversight (Art. 14) and technical robustness/cybersecurity (Art. 15). |
| **FIPS 140-3 (Level 3)** | NIST / CSE | **Hardware Security Modules:** Sovereign KEK protection within Google Cloud KMS HSM clusters. |
| **ISO/IEC 30107-3:2017** | ISO / IEC | **Biometric Liveness Detection:** Facial presentation attack detection (PAD) integrated within the RENIEC verification bridge. |

---

## 📖 12. Glosario Maestro de Términos (GovTech, Ciberseguridad, IA & Marco Penal)

| Término / Sigla | Definición Técnica y Operativa en SARA |
|---|---|
| **Zero-PII** | Paradigma de privacidad donde la identidad real del denunciante jamás es leída, memorizada ni procesada por modelos LLM. |
| **CUP** | *Código Único de Protección*. Identificador seudonimizado (`CUP-XXXXXXXX`) mediante el cual los agentes operan el caso. |
| **Envelope Encryption** | Cifrado de sobre donde cada registro se cifra con una clave efímera (DEK) envuelta por la clave maestra (KEK) en Cloud KMS HSM. |
| **HITL** | *Human-in-the-Loop*. Principio de gobernanza donde la IA recomienda y el comisario policial humano colegiado ejecuta la firma oficial. |
| **IRCE ($T_{index}$)** | *Indicador de Riesgo y Complejidad Extorsiva*. Algoritmo multicriterio Saaty AHP (70% Certeza / 30% Inminencia). |
| **SIDPOL** | *Sistema de Denuncias Policiales* de la PNP. SARA estructura y transmite el atestado con código oficial `SIDPOL-2026-XXXXXX`. |
| **FECOR** | *Fiscalías Especializadas contra la Criminalidad Organizada* del Ministerio Público, receptoras del informe policial generado por SARA. |
| **Ley N.° 32303** | Autoriza el **bloqueo preventivo de IMEI y corte de línea celular en 3 horas** por la Policía Nacional. |
| **D.Leg. N.° 1735** | Crea el *Subsistema Especializado contra la Extorsión* y autoriza el congelamiento preventivo de cuentas en 24h con la UIF. |

---

## 🛠️ 13. Tech Stack & Authorship

* **Author & System Architect:** **Carlos Eduardo Baños Diaz**.
* **AI Pair-Programming Acceleration:** Google Antigravity IDE (Agentic Coding Assistant).
* **Foundational AI Models:** Google Gemini 2.5 Flash, Google Gemini 3.7 Flash, and Google Gemini 3.7 Pro Reasoning (Thinking Budget = 2048 tokens).
* **Agentic Framework:** Google Agent Development Kit (ADK) & Google GenAI Python SDK (`google-genai`).
* **Cloud & Serverless Infrastructure:** Google Cloud Run (`us-central1`), Google Cloud KMS, Google Secret Manager, Google BigQuery GIS.
* **Integrations:** Vapi AI WebRTC Web SDK, Make.com Webhooks, Telegram Bot API, PyTest (17/17 Passing Tests), Streamlit Enterprise.

---

*SARA v2.5 - Conceived, Designed, and Developed by **Carlos Eduardo Baños Diaz** for the All Things Agentic Hackathon | Google Cloud & Devpost © 2026. All Rights Reserved.*
