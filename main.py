import flet as ft
import logging

# 로깅 활성화 (내부에서 멈추는지 확인용, 필수는 아니지만 안전장치)
logging.basicConfig(level=logging.INFO)

def main(page: ft.Page):
    # 1. 페이지 초기화 (배경색 지정으로 렌더링 시작 신호 줌)
    page.title = "Connection Test"
    page.bgcolor = "white"
    
    # 2. 정렬 설정 (이게 없으면 때로 화면 구석에 처박힘)
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    # 3. 아주 단순한 텍스트
    # 폰트나 스타일도 기본값 사용 (에러 요인 제거)
    t = ft.Text(
        value="화면이 보이면 성공입니다!",
        color="black",
        size=30,
        weight="bold"
    )

    # 4. 강제 업데이트
    # add() 만으로는 안드로이드에서 즉시 반영 안 될 때가 있음
    page.add(t)
    page.update()
    
    print("App Loaded Successfully")

if __name__ == "__main__":
    # 안드로이드에서는 웹 렌더러 설정을 건드리지 않고 기본값으로 둡니다.
    ft.app(target=main)
