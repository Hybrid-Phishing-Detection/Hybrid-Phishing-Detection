# File: backend/app/services/email_analyzer.py
import torch
from transformers import XLMRobertaTokenizer, XLMRobertaForSequenceClassification
import logging

logging.getLogger("transformers").setLevel(logging.ERROR)

class XLMRoBERTaAnalyzer:
    def __init__(self):
        # 파인튜닝 전 기본 모델 로드 (최초 실행 시 다운로드 진행됨)
        self.model_name = "xlm-roberta-base"
        self.tokenizer = XLMRobertaTokenizer.from_pretrained(self.model_name)
        self.model = XLMRobertaForSequenceClassification.from_pretrained(self.model_name, num_labels=2)
        self.model.eval()

    def analyze(self, subject: str, body: str) -> float:
        text = f"{subject} {body}"
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            probabilities = torch.softmax(outputs.logits, dim=1)
            # 분류 헤드 학습 전이므로 반환되는 값은 무작위성이 강합니다.
            return probabilities[0][1].item()

email_analyzer = XLMRoBERTaAnalyzer()