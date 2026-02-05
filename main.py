import flet as ft

def main(page: ft.Page):
    # 1. 화면 초기화 (아무것도 넣지 않음)
    page.title = "Flash Button"
    page.bgcolor = "black"
    
    # [핵심] 레이아웃 위젯(Column/Row)을 아예 쓰지 않음!
    # page.add(...) 자체를 생략하거나 단순 텍스트만 넣음
    page.add(ft.Text("우측 하단 버튼을 눌러보세요.", color="grey"))

    # 2. 상태값
    state = {"is_white": False}

    # 3. 기능: 배경색 바꾸기
    def toggle_flash(e):
        state["is_white"] = not state["is_white"]
        
        if state["is_white"]:
            page.bgcolor = "white"
            # 버튼 아이콘 변경 (검은색 아이콘)
            page.floating_action_button.icon = ft.icons.FLASHLIGHT_OFF
            page.floating_action_button.bgcolor = "black"
            page.floating_action_button.icon_color = "white"
        else:
            page.bgcolor = "black"
            # 버튼 아이콘 변경 (흰색 아이콘)
            page.floating_action_button.icon = ft.icons.FLASHLIGHT_ON
            page.floating_action_button.bgcolor = "white"
            page.floating_action_button.icon_color = "black"
        
        page.update()

    # 4. [핵심] FloatingActionButton 사용
    # 이건 화면 레이아웃(Stack/Column)과 별개로 렌더링되므로 충돌 안 남
    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.icons.FLASHLIGHT_ON,
        bgcolor="white",
        icon_color="black",
        on_click=toggle_flash
    )

    # 강제 업데이트
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
