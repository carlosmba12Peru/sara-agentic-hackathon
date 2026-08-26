"""Pytest test configuration and fixtures."""

import pytest
from app.models.case import ExtortionCase, CitizenProfile
from app.models.threat_index import ThreatFactorScores


@pytest.fixture
def sample_scores_high():
    """Fixture providing high severity threat factor scores."""
    return ThreatFactorScores(
        coercion=90.0,
        persistence=80.0,
        artifacts=85.0,
        vulnerability=70.0,
    )


@pytest.fixture
def sample_scores_low():
    """Fixture providing low severity threat factor scores."""
    return ThreatFactorScores(
        coercion=15.0,
        persistence=10.0,
        artifacts=5.0,
        vulnerability=20.0,
    )


@pytest.fixture
def sample_case():
    """Fixture providing a mock extortion case."""
    citizen = CitizenProfile(
        phone_number="+51999888777",
        anonymous=False,
        alias="Victim_01",
        location_jurisdiction="Lima, Peru",
    )
    return ExtortionCase(
        citizen=citizen,
        source_channel="TEST_RUNNER",
    )
