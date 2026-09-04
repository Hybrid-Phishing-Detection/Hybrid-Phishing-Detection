// File: frontend/app/page.tsx
"use client";

import { useState } from "react";
import axios from "axios";

export default function Home() {
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      // Docker Compose 환경에서 프론트엔드가 백엔드 API에 접근할 때의 URL
      const response = await axios.post("http://localhost:8000/api/analyze", {
        subject,
        body,
      });
      setResult(response.data);
    } catch (error) {
      console.error("API 호출 에러:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-4xl mx-auto font-sans">
      <h1 className="text-3xl font-bold mb-6">Hybrid Phishing Detection System</h1>
      <div className="mb-4">
        <label className="block mb-2 font-semibold">이메일 제목</label>
        <input 
          className="border border-gray-300 rounded w-full p-2" 
          value={subject} 
          onChange={(e) => setSubject(e.target.value)} 
          placeholder="이메일 제목을 입력하세요"
        />
      </div>
      <div className="mb-4">
        <label className="block mb-2 font-semibold">이메일 본문</label>
        <textarea 
          className="border border-gray-300 rounded w-full p-2 h-48" 
          value={body} 
          onChange={(e) => setBody(e.target.value)} 
          placeholder="이메일 본문을 입력하세요"
        />
      </div>
      <button 
        className="bg-blue-600 text-white font-bold px-6 py-2 rounded hover:bg-blue-700" 
        onClick={handleAnalyze}
        disabled={loading}
      >
        {loading ? "분석 중..." : "분석하기"}
      </button>

      {result && (
        <div className="mt-8 p-6 border rounded bg-gray-50">
          <h2 className="text-2xl font-bold mb-4">분석 결과</h2>
          <div className="text-xl font-bold text-red-600 mb-2">
            최종 위험도: {result.final_risk * 100}%
          </div>
          <div className="text-lg font-bold mb-6">
            분류: {result.classification.toUpperCase()}
          </div>
          
          <h3 className="text-xl font-bold mb-2 border-b pb-2">Email Analysis</h3>
          <p className="mb-6">텍스트 피싱 위험도: {result.email_risk * 100}%</p>

          <h3 className="text-xl font-bold mb-2 border-b pb-2">URL Analysis (발견된 URL: {result.urls.length}개)</h3>
          {result.urls.map((urlItem: any, idx: number) => (
            <div key={idx} className="mt-4 p-4 border bg-white rounded shadow-sm">
              <p className="font-semibold text-blue-600 mb-2">{urlItem.url}</p>
              <p>Machine Learning Risk: {urlItem.ml_risk * 100}%</p>
              <p>External Reputation Risk: {urlItem.reputation_risk * 100}%</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}