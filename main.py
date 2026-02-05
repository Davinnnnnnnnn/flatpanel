import flet as ft

def main(page: ft.Page):
    # 1. 화면 설정 (텍스트 성공했던 설정 그대로 유지)
    page.bgcolor = "black"
    page.title = "Block UI"
    page.padding = 0
    page.spacing = 0
    
    # 테마 강제 설정 (충돌 방지)
    page.theme_mode = ft.ThemeMode.DARK

    # 2. 상태값
    state = {
        "size": 300,
        "bright": 100,
        "flash": False
    }

    # =================================================================
    # 3. "가짜 버튼" 공장 (Container로 버튼 만들기)
    # 위젯을 쓰지 않으므로 충돌 확률 0%
    # =================================================================
    def create_block_btn(text, color, func):
        return ft.Container(
            content=ft.Text(text, color="black", weight="bold", size=16),
            bgcolor=color,
            width=100,
            height=60,
            alignment=ft.alignment.center,
            border_radius=8,
            on_click=func, # 클릭 이벤트는 컨테이너에 직접 연결
            padding=5
        )

    # =================================================================
    # 4. 화면 요소
    # =================================================================
    
    # 정보창 (텍스트는 성공했으니 안심하고 사용)
    info_text = ft.Text("상태: 크기 300 / 밝기 100%", size=18, color="white")

    # 중앙 원 (단순 컨테이너)
    the_circle = ft.Container(
        width=300,
        height=300,
        bgcolor="white",
        border_radius=150,
        alignment=ft.alignment.center
    )

    # =================================================================
    # 5. 로직 함수
    # =================================================================
    def update_screen():
        # 원 상태 반영
        the_circle.width = state["size"]
        the_circle.height = state["size"]
        the_circle.border_radius = state["size"] / 2
        the_circle.opacity = state["bright"] / 100.0
        
        # 텍스트 반영
        info_text.value = f"상태: 크기 {state['size']} / 밝기 {state['bright']}%"
        
        page.update()

    def click_size_up(e):
        if state["size"] < 1000: state["size"] += 50
        update_screen()

    def click_size_down(e):
        if state["size"] > 50: state["size"] -= 50
        update_screen()

    def click_bright_up(e):
        if state["bright"] < 100: state["bright"] += 10
        update_screen()

    def click_bright_down(e):
        if state["bright"] > 10: state["bright"] -= 10
        update_screen()

    def toggle_flash(e):
        state["flash"] = not state["flash"]
        if state["flash"]:
            # 플래시 모드: 배경 흰색, 나머지 숨김
            page.bgcolor = "white"
            controls.visible = False
            the_circle.visible = False
        else:
            # 복구
            page.bgcolor = "black"
            controls.visible = True
            the_circle.visible = True
        page.update()

    # =================================================================
    # 6. 레이아웃 조립 (안전한 Column 사용)
    # =================================================================
    
    # 컨트롤 패널 조립
    controls = ft.Column(
        controls=[
            ft.Container(height=20), # 여백
            info_text,
            ft.Container(height=20), # 여백
            
            ft.Text("크기 조절", color="grey"),
            ft.Row(
                [
                    create_block_btn("- 작게", "orange", click_size_down),
                    create_block_btn("+ 크게", "orange", click_size_up)
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            
            ft.Container(height=20), # 여백
            
            ft.Text("밝기 조절", color="grey"),
            ft.Row(
                [
                    create_block_btn("- 어둡게", "cyan", click_bright_down),
                    create_block_btn("+ 밝게", "cyan", click_bright_up)
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            
            ft.Container(height=40), # 여백
            
            # 플래시 버튼 (가장 큼)
            ft.Container(
                content=ft.Text("플래시 모드 (흰 화면)", size=20, weight="bold"),
                bgcolor="yellow",
                width=250,
                height=80,
                alignment=ft.alignment.center,
                border_radius=12,
                on_click=toggle_flash
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # 메인 페이지 추가
    page.add(
        ft.Column(
            controls=[
                ft.Container(height=50), # 상단 여백
                
                # 원 영역 (높이 고정해서 밀림 방지)
                ft.Container(
                    content=the_circle,
                    alignment=ft.alignment.center,
                    height=500, 
                    bgcolor=ft.colors.with_opacity(0.1, "white") # 영역 확인용 살짝 표시
                ),
                
                controls
            ],
            scroll=ft.ScrollMode.AUTO, # 화면 넘치면 스크롤
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
