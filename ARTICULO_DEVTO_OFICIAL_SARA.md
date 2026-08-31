---
title: Building SARA: A Sovereign Multi-Agent AI System on Google Cloud to Eliminate Extortion and Break the 99.88% Impunity Gap
published: true
tags: googlecloud, ai, gemini, python
cover_image: https://raw.githubusercontent.com/carlosmba12Peru/sara-agentic-hackathon/main/devto_cover_sara2.jpg
canonical_url: https://dev.to/carlosmba12peru/building-sara-a-sovereign-multi-agent-ai-system-on-google-cloud-to-eliminate-extortion-and-break-ac8
---

*This article is an official submission for the **Google Cloud & Devpost "All Things Agentic Hackathon 2026"**.*

---

## 🏆 Official Project Submission Links

- 🏛️ **Official Devpost Project Submission:** [https://devpost.com/software/sara-cognitive-extortion-response-agent](https://devpost.com/software/sara-cognitive-extortion-response-agent)
- 🌐 **Live Web Application (Google Cloud Run):** [https://sara-produccion-981735936523.us-central1.run.app/](https://sara-produccion-981735936523.us-central1.run.app/)
- 💻 **Public GitHub Repository:** [https://github.com/carlosmba12Peru/sara-agentic-hackathon](https://github.com/carlosmba12Peru/sara-agentic-hackathon)
- 🎥 **Full Video Pitch & Live Architecture Demo (YouTube):** [https://youtu.be/2kZfttRrb3M](https://youtu.be/2kZfttRrb3M)
- 🤖 **Citizen Telegram Bot:** [@kallpa_IA_asistente_bot](https://t.me/kallpa_IA_asistente_bot)

---

## 🚨 The Emergency: The 4-Level Extortion Impunity Funnel

In Peru and Latin America, violent extortion and criminal racketeering have paralyzed public transportation, small businesses, and urban safety. Cross-referencing 2026 data from the **Public Ministry (MPFN)**, **Ministry of the Interior (MININTER / SIDPOL)**, **Judiciary Flagrancy Courts**, and the **Peruvian Institute of Economics (IPE)** exposes the staggering reality of the **4-Level Extortion Impunity Funnel**:

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 1. Real Street Extortions: ~200,000 Attacks / Year (85% Dark Figure)   │
└────────────────────────────────────┬────────────────────────────────────┘
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 2. Police Stations (SIDPOL): ~19,000 Formal Reports (Paper Limbo)       │
└────────────────────────────────────┬────────────────────────────────────┘
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 3. Public Ministry (MPFN): ~26,000 Crimes / Year (12,634 1st Sem.)      │
└────────────────────────────────────┬────────────────────────────────────┘
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 4. Judiciary Flagrancy Courts: Only ~240 Judged (99.88% Impunity)       │
└────────────────────────────────────┬────────────────────────────────────┘
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 🚀 SOLUTION: SARA Sovereign Copilot — 1.8s Digital Forensic Dossiers    │
└─────────────────────────────────────────────────────────────────────────┘
```

1. **200,000 Real Extortions / Year:** Over **85% of victims remain in total silence** due to mortal terror of identity leaks and violent retaliation from contract killers (*"sicarios"*).
2. **19,000 Police Station Reports:** The few who report get trapped in 48 hours of manual paperwork without immediate digital forensic tracing.
3. **26,000 Crimes in Public Ministry Records:** Evidence arrives weeks late, long after the 48-hour constitutional flagrancy window expires.
4. **Only 240 Cases Judged in Flagrancy Courts:** Resulting in an appalling **0.12% real judicial resolution rate** and a **99.88% systemic impunity rate**.

To shatter this bottleneck, we engineered **SARA (Sistema Autónomo de Respuesta Anti-Extorsión)**: a sovereign, autonomous multi-agent cognitive copilot on **Google Cloud** that empowers citizens to report safely from their phones under a mathematical **Zero-PII guarantee (Code CUP)** in **5 indigenous languages + Spanish and English**, converting 48 hours of bureaucratic triage into **1.8 seconds of forensic intelligence** and digital transmission to the **Specialized Anti-Extortion Prosecution Office (FECOR - Legislative Decree No. 1735)**.

---

## 🏗️ Technical Architecture: Dual-Brain Multi-Agent Swarm

SARA is architected around an enterprise-grade **Parallel Multi-Agent Swarm** powered by **Google Agent Development Kit (ADK)** and the **Google GenAI Python SDK**:

```
                      ┌───────────────────────────────────────────────┐
                      │             CITIZEN INTAKE PORTAL             │
                      │  Web / WebRTC Voice (Quechua/Shipibo/Spanish) │
                      └───────────────────────┬───────────────────────┘
                                              │
                                              ▼
                      ┌───────────────────────────────────────────────┐
                      │           PRE-INGRESS SHIELD & VAD            │
                      │ CentinelaAgent (<300ms Anti-Spam D.S. 020)    │
                      └───────────────────────┬───────────────────────┘
                                              │
                                              ▼
                      ┌───────────────────────────────────────────────┐
                      │         SOVEREIGN ZERO-PII VAULT              │
                      │ Isolation HMAC-SHA256 + Code CUP Generation   │
                      └───────────────────────┬───────────────────────┘
                                              │
         ┌────────────────────────────────────┼────────────────────────────────────┐
         │                                    │                                    │
         ▼                                    ▼                                    ▼
┌──────────────────┐               ┌──────────────────┐               ┌──────────────────┐
│  BRANCH 0: VOZ   │               │ BRANCH 1: PIDE   │               │ BRANCH 2: SAATY  │
│  Amparo AI Agent │               │ Forensics & OCR  │               │ CalculoAgent AHP │
│  (Empathy <600ms)│               │ (OSIPTEL / RENIEC│               │ (IRCE Index 70%) │
└────────┬─────────┘               └────────┬─────────┘               └────────┬─────────┘
         │                                  │                                  │
         └──────────────────────────────────┼──────────────────────────────────┘
                                            │
                                            ▼
                      ┌───────────────────────────────────────────────┐
                      │    BRANCH 3: LEGAL ADVISOR & HITL GATEWAY     │
                      │   Subsumption Art. 200/200-A & Token CIP      │
                      └───────────────────────┬───────────────────────┘
                                              │
                                              ▼
                      ┌───────────────────────────────────────────────┐
                      │       FECOR FISCAL REMISSION (D.LEG. 1735)    │
                      │   SHA-256 Chain of Custody & Telegram Dispatch│
                      └───────────────────────────────────────────────┘
```

### 1. Dual-Brain Cognitive Routing
- **Tier FLASH_FAST (`gemini-2.5-flash` / `gemini-3.7-flash`):** Real-time Voice Activity Detection (VAD), acoustic anti-spam triage (<300ms latency), and empathetic voice dialogue in **Quechua, Shipibo-Konibo, Aimara, and Spanish**.
- **Tier PRO_REASONING (`gemini-3.7-pro`):** Deep multimodal forensic analysis, **OCR extraction** of handwritten threat letters, ammunition caliber classification (SUCAMEC), and statutory compliance checking (**Thinking Budget: 2048 tokens**, `temperature=0.1`).

### 2. Sovereign Cryptographic Zero-PII Vault
To guarantee absolute protection for victims:
- Citizen identity (National ID/DNI, Full Name, Phone Number, GPS Coordinates) is isolated at the edge.
- The system derives an anonymous **Unique Protection Code (CUP)** using **HMAC-SHA256 with CSPRNG salt** and Envelope Encryption with **Google Cloud KMS (HSM FIPS 140-3 Level 3)**.
- Downstream LLM agents strictly process the CUP code, making internal identity exfiltration mathematically impossible.

### 3. Formal AHP-Saaty Multicriteria Decision Model (IRCE)
Instead of relying on unexplainable black-box probabilities, SARA implements Thomas Saaty's **Analytic Hierarchy Process (AHP)** to compute the **Extortion Risk and Complexity Indicator (IRCE)**:

$$\text{IRCE} = (0.70 \times D_{\text{certeza}}) + (0.30 \times D_{\text{inminencia}})$$

- **High (81–100%):** Immediate 3-hour IMEI cutoff (Law 32303) and 24-hour preventive bank freeze (D.Leg. 1735).
- **Moderate (51–80%):** Intelligence monitoring and preventive patrol dispatch.
- **Low (26–50%):** Information registration.
- **Dismissal ($\le$ 25%):** Archive with audit log.

### 4. Human-in-the-Loop (HITL) Sovereign Governance (Law No. 31814)
In compliance with **Peruvian AI Law No. 31814** and **ISO/IEC 42001**:
- AI never executes coercive police powers autonomously.
- A verified human police commander audits the evidence, validates the legal qualification, selects tactical measures, and cryptographically signs the dossier with their **Official Police Digital Token (CIP)** into **SIDPOL**.
- With one click, the dossier is transmitted to the **Specialized Anti-Extortion Prosecution Office (FECOR)** and the citizen receives instant confirmation on **Telegram**.

---

## 🧪 Comprehensive Automated Test Suite

SARA has undergone rigorous validation with **17/17 passing integration unit tests in PyTest**:
- `test_i18n_optimization.py`: Validates multi-language token caching and low-latency translation.
- `test_shipibo_renitli_telegram_flow.py`: Verifies Amazonian language intake and automated Telegram webhook notifications.
- `test_security_hardening.py`: Validates prompt injection defense, Zero-PII anonymization, and SHA-256 custody chain immutability.
- `test_flujo_completo_hackathon.py`: Validates the end-to-end 1.8-second execution across all 17 agents.

---

## ☁️ Google Cloud Infrastructure Stack

- **Google Cloud Run:** Serverless containerized deployment in `us-central1` with automatic scale-to-zero.
- **Google Cloud KMS:** Hardware Security Module (HSM FIPS 140-3) for master key envelope encryption.
- **Google Secret Manager:** Secure programmatic retrieval of API keys and webhook tokens.
- **Google BigQuery GIS:** Territorial geospatial clustering across Peru's 25 regional departments.
- **Google Agent Development Kit (ADK) & GenAI SDK:** Swarm execution pool and dual-brain cognitive routing.

---

## ⚠️ Institutional Independence & Synthetic Data Notice

> **SARA is an independent research and demonstrative software prototype designed and developed exclusively by the SARA AI Core & Research Lab for the Google Cloud & Devpost "All Things Agentic Hackathon 2026".**  
> It is not an official system of the Peruvian National Police (PNP), the Ministry of the Interior, or the Public Ministry. All public datasets, legal norms, and institutional frameworks are referenced strictly for realistic engineering modeling.  
>  
> 🔒 **Synthetic Data Disclosure (Law No. 29733):** All citizen names, IDs, phone numbers, and financial accounts used in demonstration cases are 100% fictitious, synthetic, and procedurally generated for AI benchmarking.
