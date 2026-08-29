"""
Módulo Oficial del Enjambre de 16 Agentes Especializados de SARA.
Sistema Autónomo de Respuesta Anti-Extorsión (Hackathon Google DeepMind / AGY SDK 2026).
"""

from agents.kallpa import amparo_agent, kallpa_agent, AmparoAgent, KallpaAgent
from agents.purificador import purificador_agent, PurificadorAgent
from agents.centinela import centinela_agent, CentinelaAgent
from agents.forense_extractor import SubAgenteForenseExtractor, forense_extractor_agent
from agents.auditor_forense import auditor_forense_agent, AuditorForenseAgent
from agents.perito_grafotecnico import perito_grafotecnico_agent, PeritoGrafotecnicoAgent
from agents.analista import analista_agent, AnalistaAgent
from agents.correlacionador_forense import correlacionador_forense_agent, CorrelacionadorForenseAgent
from agents.calculo import calculo_agent, CalculoAgent
from agents.asesor_juridico import asesor_juridico_agent, AsesorJuridicoAgent
from agents.vigia_normativo import vigia_normativo_agent, VigiaNormativoAgent
from agents.radar_criminologico import radar_criminologico_agent, RadarCriminologicoAgent
from agents.pide_agent import pide_agent, PIDEAgent
from agents.renitli_agent import renitli_agent, ReNITLIAgent, PADRON_OFICIAL_RENITLI
from agents.traductor_originario import yachaq_agent, traductor_originario_agent, AgenteTraductorOriginarias
from agents.yachaq import YachaqAgent
from agents.empaquetador import empaquetador_agent, EmpaquetadorAgent
from agents.ai_threat_intel_agent import ai_threat_intel_agent, AIThreatIntelAgent
from agents.router import agent_router, AgentRouter

__all__ = [
    "amparo_agent",
    "kallpa_agent",
    "AmparoAgent",
    "KallpaAgent",
    "purificador_agent",
    "PurificadorAgent",
    "centinela_agent",
    "CentinelaAgent",
    "forense_extractor_agent",
    "SubAgenteForenseExtractor",
    "auditor_forense_agent",
    "AuditorForenseAgent",
    "perito_grafotecnico_agent",
    "PeritoGrafotecnicoAgent",
    "analista_agent",
    "AnalistaAgent",
    "correlacionador_forense_agent",
    "CorrelacionadorForenseAgent",
    "calculo_agent",
    "CalculoAgent",
    "asesor_juridico_agent",
    "AsesorJuridicoAgent",
    "vigia_normativo_agent",
    "VigiaNormativoAgent",
    "radar_criminologico_agent",
    "RadarCriminologicoAgent",
    "pide_agent",
    "PIDEAgent",
    "renitli_agent",
    "ReNITLIAgent",
    "PADRON_OFICIAL_RENITLI",
    "yachaq_agent",
    "traductor_originario_agent",
    "AgenteTraductorOriginarias",
    "empaquetador_agent",
    "EmpaquetadorAgent",
    "ai_threat_intel_agent",
    "AIThreatIntelAgent",
    "agent_router",
    "AgentRouter"
]
