
# 🎤 주차 차량 확인기 (Python 버전)

HTML(Web Speech API) 대신 **Python**으로 음성인식 및 조회를 수행합니다.  
데이터는 `car_data.json` 파일에 들어있습니다.

## 1) 실행 방법

### A. Android (Pydroid 3 권장)
1. Play 스토어에서 **Pydroid 3** 설치
2. 이 저장소(또는 아래 다운로드 파일)를 Pydroid 3의 `Download` 폴더로 복사
3. Pydroid 3에서 **Pip** 열고 다음 패키지 설치
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
   - `speechrecognition`, `gTTS`, `playsound`가 설치됩니다.
   - `pyaudio`는 Android에선 없어도 됩니다.
4. **마이크 권한 허용**
5. 실행
   ```bash
   python voice_car_checker.py
   ```
6. 안내에 따라 **말하거나(2~4자리 번호)**, 키보드로 **직접 입력**하세요.

> ⚠️ Android 기기/환경에 따라 마이크 접근 방식이 달라 인식이 어려울 수 있습니다. 그 경우 **키보드 입력** 모드로 사용하세요.

### B. PC/Mac
```bash
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python voice_car_checker.py
```

## 2) 사용법
- 음성: 2~4자리 숫자 예) "공일일사(0114)", "오구팔이(0982)"
- 키보드: 숫자만 입력, 또는 혼합 문자열(자동으로 숫자만 추출)
- 프로그램은 뒤 **4자리** 기준으로 조회하며, 4자리가 안 되면 **패딩**합니다.

## 3) 데이터 수정
- `car_data.json`을 열어 항목을 추가/수정하세요.
- CSV를 쓰고 싶으면 `car_data.csv` 참고.

## 4) 라이선스/주의
- 음성 인식은 Google Web Speech API를 사용하므로 **인터넷 연결**이 필요합니다.
- TTS는 gTTS를 사용합니다(필요 없으면 `TTS_OFF = True`).

