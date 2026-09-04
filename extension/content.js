// File: extension/content.js
(function() {
  if (document.getElementById("phishing-detector-widget")) return;

  // 1. 위젯 DOM 생성
  const widget = document.createElement("div");
  widget.id = "phishing-detector-widget";
  
  widget.innerHTML = `
    <div id="pd-header">Phishing Detector</div>
    <div id="pd-content">
      <div class="pd-btn-group">
        <button id="pd-btn-start" class="pd-btn pd-btn-start">작동</button>
        <button id="pd-btn-stop" class="pd-btn pd-btn-stop">중지</button>
      </div>
      <div id="pd-status">대기 중...</div>
      
      <button id="pd-btn-toggle" class="pd-btn pd-btn-toggle">수동 입력 열기 ▼</button>
      
      <div id="pd-manual-section">
        <input type="text" id="pd-manual-subject" class="pd-input" placeholder="이메일 제목">
        <textarea id="pd-manual-body" class="pd-input" rows="4" placeholder="이메일 본문"></textarea>
        <button id="pd-btn-manual-analyze" class="pd-btn pd-btn-manual">분석시작</button>
      </div>
    </div>
  `;
  document.body.appendChild(widget);

  // 2. 드래그 기능 구현
  const header = document.getElementById("pd-header");
  let isDragging = false;
  let offsetX, offsetY;

  header.addEventListener("mousedown", (e) => {
    isDragging = true;
    offsetX = e.clientX - widget.getBoundingClientRect().left;
    offsetY = e.clientY - widget.getBoundingClientRect().top;
  });

  document.addEventListener("mousemove", (e) => {
    if (!isDragging) return;
    widget.style.left = (e.clientX - offsetX) + "px";
    widget.style.top = (e.clientY - offsetY) + "px";
    widget.style.right = "auto"; 
  });

  document.addEventListener("mouseup", () => {
    isDragging = false;
  });

  // 3. UI 요소 참조
  const btnStart = document.getElementById("pd-btn-start");
  const btnStop = document.getElementById("pd-btn-stop");
  const btnToggle = document.getElementById("pd-btn-toggle");
  const btnManualAnalyze = document.getElementById("pd-btn-manual-analyze");
  const manualSection = document.getElementById("pd-manual-section");
  const statusDiv = document.getElementById("pd-status");
  
  let autoScanInterval = null;

  // 4. 백엔드 통신 함수
  function requestAnalysis(subject, body) {
    statusDiv.innerHTML = "분석 중...";
    chrome.runtime.sendMessage(
      { type: "ANALYZE_EMAIL", payload: { subject, body } },
      (response) => {
        if (response && response.success) {
          const data = response.data;
          const riskPercent = (data.final_risk * 100).toFixed(1);
          statusDiv.innerHTML = `
            <strong>상태:</strong> ${data.classification.toUpperCase()}<br>
            <strong>위험도:</strong> ${riskPercent}%<br>
            <strong>URL 수:</strong> ${data.urls.length}개
          `;
        } else {
          statusDiv.innerHTML = "분석 실패 (서버 오류)";
        }
      }
    );
  }

  // 5. 자동 추출 로직 (현재는 임시로 화면 전체 텍스트를 읽어옴)
  // 실제 이메일 서비스(Gmail 등)의 DOM 구조에 맞춘 파싱 로직으로 대체 필요
  function autoExtractAndAnalyze() {
    const subject = document.title;
    const body = document.body.innerText.substring(0, 500); // 부하 방지를 위해 500자로 제한
    requestAnalysis(subject, body);
  }

  // 6. 이벤트 리스너 등록
  btnStart.addEventListener("click", () => {
    if (autoScanInterval) return;
    statusDiv.innerHTML = "자동 감시 시작됨";
    // 5초 주기로 화면을 읽어 분석 요청
    autoScanInterval = setInterval(autoExtractAndAnalyze, 5000);
    autoExtractAndAnalyze(); 
  });

  btnStop.addEventListener("click", () => {
    if (autoScanInterval) {
      clearInterval(autoScanInterval);
      autoScanInterval = null;
      statusDiv.innerHTML = "자동 감시 중지됨";
    }
  });

  btnToggle.addEventListener("click", () => {
    const isHidden = manualSection.style.display === "none" || manualSection.style.display === "";
    manualSection.style.display = isHidden ? "block" : "none";
    btnToggle.innerText = isHidden ? "수동 입력 닫기 ▲" : "수동 입력 열기 ▼";
  });

  btnManualAnalyze.addEventListener("click", () => {
    const subject = document.getElementById("pd-manual-subject").value;
    const body = document.getElementById("pd-manual-body").value;
    
    if (!subject && !body) {
      statusDiv.innerHTML = "내용을 입력하세요.";
      return;
    }
    requestAnalysis(subject, body);
  });

})();