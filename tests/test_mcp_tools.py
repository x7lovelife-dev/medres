from mcp_server.clinical_trials import search_clinical_trials
from mcp_server.patents import search_patents
from mcp_server.safety import search_adverse_events, search_drug_labels


class FakeResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")

    def json(self):
        return self._payload


def test_search_clinical_trials_flattens_study(monkeypatch):
    def fake_get(url, params=None, timeout=20):
        return FakeResponse(
            {
                "studies": [
                    {
                        "protocolSection": {
                            "identificationModule": {"nctId": "NCT123", "briefTitle": "Trial title"},
                            "statusModule": {"overallStatus": "COMPLETED", "startDateStruct": {"date": "2021-01"}},
                            "designModule": {"phases": ["PHASE3"], "enrollmentInfo": {"count": 500}},
                            "conditionsModule": {"conditions": ["Gastric Cancer"]},
                            "armsInterventionsModule": {"interventions": [{"name": "Drug A"}]},
                            "outcomesModule": {"primaryOutcomes": [{"measure": "Overall Survival"}]},
                            "sponsorCollaboratorsModule": {"leadSponsor": {"name": "Sponsor"}},
                        }
                    }
                ]
            }
        )

    monkeypatch.setattr("mcp_server.clinical_trials.requests.get", fake_get)
    result = search_clinical_trials(condition="gastric cancer", intervention="Drug A", phase=["PHASE3"])

    assert result["source"] == "ClinicalTrials.gov API v2"
    assert result["items"][0]["nct_id"] == "NCT123"
    assert result["items"][0]["url"] == "https://clinicaltrials.gov/study/NCT123"


def test_search_drug_labels_flattens_openfda_label(monkeypatch):
    def fake_get(url, params=None, timeout=20):
        return FakeResponse(
            {
                "results": [
                    {
                        "openfda": {"brand_name": ["BRAND"], "generic_name": ["drug"]},
                        "indications_and_usage": ["indication"],
                        "adverse_reactions": ["reaction"],
                        "set_id": "set-1",
                    }
                ]
            }
        )

    monkeypatch.setattr("mcp_server.safety.requests.get", fake_get)
    result = search_drug_labels("drug")

    assert result["items"][0]["brand_names"] == ["BRAND"]
    assert result["items"][0]["set_id"] == "set-1"


def test_search_adverse_events_returns_counts(monkeypatch):
    calls = []

    def fake_get(url, params=None, timeout=20):
        calls.append(params or {})
        if "count" in (params or {}):
            return FakeResponse({"results": [{"time": "20240101", "count": 7}]})
        return FakeResponse({"meta": {"results": {"total": 12}}})

    monkeypatch.setattr("mcp_server.safety.requests.get", fake_get)
    result = search_adverse_events("drug", "rash")

    assert result["items"][0]["count"] == 12
    assert result["items"][0]["yearly_counts"] == {"2024": 7}
    assert len(calls) == 2


def test_search_patents_flattens_patentsview(monkeypatch):
    def fake_post(url, json=None, timeout=20):
        return FakeResponse(
            {
                "patents": [
                    {
                        "patent_number": "1234567",
                        "patent_title": "Antibody composition",
                        "patent_abstract": "Abstract",
                        "patent_date": "2020-01-01",
                        "assignees": [{"assignee_organization": "Company"}],
                        "inventors": [{"inventor_first_name": "A", "inventor_last_name": "B"}],
                    }
                ]
            }
        )

    monkeypatch.setattr("mcp_server.patents.requests.post", fake_post)
    result = search_patents("antibody", jurisdictions=["US"])

    assert result["items"][0]["id"] == "1234567"
    assert result["items"][0]["assignees"] == ["Company"]
    assert result["items"][0]["url"] == "https://patents.google.com/patent/US1234567"
