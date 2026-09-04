# File: backend/app/services/reputation.py
import os
import requests
from abc import ABC, abstractmethod

class ReputationProvider(ABC):
    @abstractmethod
    def check_url(self, url: str) -> float:
        pass

class NordVPNProvider(ReputationProvider):
    def __init__(self):
        self.api_url = os.environ.get(
            "NORDVPN_API_URL", 
            "https://link-checker.nordvpn.com/v1/public-url-checker/check-url"
        )
        self.timeout = 10.0

    def check_url(self, url: str) -> float:
        try:
            response = requests.post(self.api_url, json={"url": url}, timeout=self.timeout)
            response.raise_for_status()
            
            json_data = response.json()
            risk_data = json_data.get("data", {})
            if not risk_data:
                risk_data = json_data
                
            score = risk_data.get("risk", {}).get("score", 0)
            return float(score) / 100.0
            
        except requests.exceptions.RequestException:
            return 0.0

def get_reputation_provider() -> ReputationProvider:
    return NordVPNProvider()