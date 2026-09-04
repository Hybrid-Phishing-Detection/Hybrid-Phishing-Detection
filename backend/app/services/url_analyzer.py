# File: backend/app/services/url_analyzer.py
import re
import math
import numpy as np
import pandas as pd
import lightgbm as lgb
from urllib.parse import urlparse
from typing import List, Dict

def extract_urls(text: str) -> List[str]:
    url_pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[^\s]*')
    return list(set(url_pattern.findall(text)))

def calculate_entropy(text: str) -> float:
    if not text:
        return 0.0
    entropy = 0.0
    for x in set(text):
        p_x = float(text.count(x)) / len(text)
        entropy += - p_x * math.log2(p_x)
    return entropy

def extract_url_features(url: str) -> Dict[str, float]:
    parsed = urlparse(url)
    domain = parsed.netloc

    features = {
        'url_length': float(len(url)),
        'domain_length': float(len(domain)),
        'path_length': float(len(parsed.path)),
        'query_length': float(len(parsed.query)),
        'subdomain_count': float(domain.count('.')),
        'digit_count': float(sum(c.isdigit() for c in url)),
        'special_char_count': float(sum(not c.isalnum() for c in url)),
        'dot_count': float(url.count('.')),
        'slash_count': float(url.count('/')),
        'hyphen_count': float(url.count('-')),
        'has_at_symbol': 1.0 if '@' in url else 0.0,
        'has_ip': 1.0 if re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b').search(domain) else 0.0,
        'has_https': 1.0 if parsed.scheme == 'https' else 0.0
    }

    suspicious_keywords = ['login', 'verify', 'update', 'secure', 'account']
    features['suspicious_keyword_count'] = float(sum(url.lower().count(kw) for kw in suspicious_keywords))
    features['digit_ratio'] = features['digit_count'] / len(url) if len(url) > 0 else 0.0
    features['special_char_ratio'] = features['special_char_count'] / len(url) if len(url) > 0 else 0.0
    features['entropy'] = calculate_entropy(url)

    return features

class LightGBMAnalyzer:
    def __init__(self):
        # 파인튜닝 전 파이프라인 에러 방지를 위해 임의의 데이터로 모델을 초기 학습시킵니다.
        dummy_features = extract_url_features("http://example.com")
        feature_names = list(dummy_features.keys())
        
        dummy_X = pd.DataFrame(np.random.rand(10, len(feature_names)), columns=feature_names)
        dummy_y = np.random.randint(0, 2, 10)
        
        self.model = lgb.LGBMClassifier(verbose=-1)
        self.model.fit(dummy_X, dummy_y)

    def analyze(self, url: str) -> float:
        features = extract_url_features(url)
        feature_df = pd.DataFrame([features])
        probabilities = self.model.predict_proba(feature_df)
        return float(probabilities[0][1])

url_ml_analyzer = LightGBMAnalyzer()