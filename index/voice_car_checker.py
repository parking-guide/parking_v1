
"""
🎤 주차 차량 확인기 (Python 음성인식 버전)
- Android에서는 'Pydroid 3' 앱에서 실행 가능(마이크 권한 필요)
- PC/Mac에서는 일반 Python 환경에서 실행 가능
- 음성으로 2~4자리 숫자를 말하면 차량 정보를 찾아서 출력하고, (옵션) 음성으로도 안내합니다.
"""
import json
import re
import sys
from pathlib import Path

# ====== 설정 ======
DATA_PATH = Path(__file__).with_name("car_data.json")

# 음성 인식
USE_SPEECH = True  # 음성 인식 사용 여부 (터미널 입력만 쓰려면 False)
LANG = "ko-KR"

# 음성 출력 (TTS): gTTS 사용 (인터넷 필요). 오프라인만 원하면 TTS_OFF = True
TTS_OFF = False
TTS_LANG = "ko"
TTS_TMP_MP3 = Path(__file__).with_name("_tts_tmp.mp3")

def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def normalize_digits(text: str) -> str:
    """문자열에서 숫자만 추출 → 4자리로 패딩"""
    num = re.sub(r"\D", "", text or "")
    if not num:
        return ""
    num = num[-4:]  # 뒤 4자리 기준
    return num.zfill(4)

def lookup_car(data, num4: str):
    for row in data:
        if row.get("번호") == num4:
            return row
    return None

def say(text: str):
    """간단한 TTS (gTTS + playsound) — 네트워크 필요"""
    if TTS_OFF:
        return
    try:
        from gtts import gTTS
        from playsound import playsound
    except Exception as e:
        print("[TTS] gTTS/playsound 미설치 또는 오류로 음성출력을 건너뜁니다.", e)
        return
    try:
        gTTS(text=text, lang=TTS_LANG).save(str(TTS_TMP_MP3))
        playsound(str(TTS_TMP_MP3))
    except Exception as e:
        print("[TTS] 실행 실패:", e)

def recognize_once() -> str:
    """마이크에서 1회 음성 인식하여 텍스트 반환"""
    try:
        import speech_recognition as sr
    except Exception as e:
        print("speech_recognition 모듈이 설치되지 않았습니다:", e)
        return ""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ 번호(2~4자리)를 말씀하세요... (조용한 환경 권장)")
        r.adjust_for_ambient_noise(source, duration=0.6)
        audio = r.listen(source, phrase_time_limit=4)  # 짧은 발화 권장
    try:
        text = r.recognize_google(audio, language=LANG)
        print("🗣️ 인식결과:", text)
        return text
    except Exception as e:
        print("❌ 인식 실패:", e)
        return ""

def main():
    data = load_data()
    print("=== 🎤 주차 차량 확인기 (Python) ===")
    print(" - 음성으로 말하거나, 키보드로 직접 입력할 수 있습니다.")
    print(" - 종료: 빈 입력 후 Enter")
    while True:
        spoken = ""
        if USE_SPEECH:
            spoken = recognize_once()

        raw = input("키보드 입력(건너뛰려면 Enter): ").strip()
        text = raw or spoken

        if not text:
            print("종료합니다.")
            break

        num4 = normalize_digits(text)
        if not num4:
            msg = "번호를 인식하지 못했습니다. 2~4자리 숫자를 말씀하거나 입력하세요."
            print("⚠️", msg)
            say(msg)
            continue

        found = lookup_car(data, num4)
        if found:
            msg = f"{num4}번 차량은 {found['색상']} {found['차종']}, 주차스티커 {found['주차스티커']} 입니다."
            print("✅", msg)
            say(msg)
        else:
            msg = f"{num4}번 차량은 등록되지 않았습니다."
            print("🚫", msg)
            say(msg)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n종료합니다.")
