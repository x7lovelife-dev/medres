from __future__ import annotations

from datetime import date
from typing import Any, Mapping

import requests


def search_clinical_trials(
    condition: str | None = None,
    intervention: str | None = None,
    phase: list[str] | None = None,
    status: list[str] | None = None,
    max_results: int = 25,
    base_url: str = "https://clinicaltrials.gov/api/v2/studies",
    timeout: int = 20,
) -> dict[str, Any]:
    """Search ClinicalTrials.gov API v2 and return flattened study records."""
    params: dict[str, Any] = {
        "pageSize": max(1, min(max_results, 100)),
        "format": "json",
    }
    terms = " ".join(part for part in [condition, intervention] if part)
    if terms:
        params["query.term"] = terms

    warnings: list[str] = []
    try:
        response = requests.get(base_url, params=params, timeout=timeout)
        response.raise_for_status()
        payload = response.json()
    except Exception as exc:
        return _result(condition, intervention, phase, status, max_results, [], [f"clinicaltrials.gov failed: {exc}"])

    requested_phases = {item.upper() for item in (phase or [])}
    requested_status = {item.upper() for item in (status or [])}
    items: list[dict[str, Any]] = []

    for study in payload.get("studies", []):
        item = _flatten_study(study)
        if requested_phases and not requested_phases.intersection({p.upper() for p in item["phase"]}):
            continue
        if requested_status and item["status"].upper() not in requested_status:
            continue
        items.append(item)
        if len(items) >= max_results:
            break

    return _result(condition, intervention, phase, status, max_results, items, warnings)


def _result(
    condition: str | None,
    intervention: str | None,
    phase: list[str] | None,
    status: list[str] | None,
    max_results: int,
    items: list[dict[str, Any]],
    warnings: list[str],
) -> dict[str, Any]:
    return {
        "query": {
            "condition": condition or "",
            "intervention": intervention or "",
            "phase": phase or [],
            "status": status or [],
            "max_results": max_results,
        },
        "retrieved_at": date.today().isoformat(),
        "source": "ClinicalTrials.gov API v2",
        "items": items,
        "warnings": warnings,
        "next_page": None,
    }


def _flatten_study(study: Mapping[str, Any]) -> dict[str, Any]:
    protocol = study.get("protocolSection", {})
    identification = protocol.get("identificationModule", {})
    status = protocol.get("statusModule", {})
    design = protocol.get("designModule", {})
    conditions = protocol.get("conditionsModule", {})
    arms = protocol.get("armsInterventionsModule", {})
    outcomes = protocol.get("outcomesModule", {})
    sponsor = protocol.get("sponsorCollaboratorsModule", {})

    nct_id = identification.get("nctId", "")
    interventions = [
        intervention.get("name", "")
        for intervention in arms.get("interventions", [])
        if intervention.get("name")
    ]
    primary_outcomes = [
        outcome.get("measure", "")
        for outcome in outcomes.get("primaryOutcomes", [])
        if outcome.get("measure")
    ]

    enrollment = design.get("enrollmentInfo", {}).get("count")
    return {
        "nct_id": nct_id,
        "title": identification.get("briefTitle") or identification.get("officialTitle") or "",
        "phase": design.get("phases", []),
        "condition": conditions.get("conditions", []),
        "intervention": interventions,
        "sponsor": sponsor.get("leadSponsor", {}).get("name", ""),
        "enrollment": enrollment,
        "primary_outcomes": primary_outcomes,
        "status": status.get("overallStatus", ""),
        "start_date": status.get("startDateStruct", {}).get("date", ""),
        "completion_date": status.get("completionDateStruct", {}).get("date", ""),
        "url": f"https://clinicaltrials.gov/study/{nct_id}" if nct_id else "",
        "evidence_role": "",
    }
