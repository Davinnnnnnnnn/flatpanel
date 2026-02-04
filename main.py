import flet as ft

def main(page: ft.Page):
    # 1. 안전 제일 설정
    page.title = "FlatPanel Button"
    page.bgcolor = "black"
    page.padding = 0
    page.spacing = 0
    page.safe_area_top = True
    
    # 2. 상태값
    state = {
        "diameter": 300,  # 정수형 사용 (안전)
        "brightness": 100, # 0~100 정수 (안전)
        "is_flash": False
    }

    # =================================================================
    # 안전한 컴포넌트 (복잡한 속성 제거)
    # =================================================================
    
    # 중앙 원
    the_circle = ft.Container(
        width=300,
        height=300,
        bgcolor=ft.colors.WHITE,
        border_radius=150,
        alignment=ft.alignment.center,
        opacity=1.0 # 1.0 = 100%
    )
    
    # 상태 표시 텍스트
    txt_info = ft.Text(
        value="D: 300px | B: 100%", 
        color="white", 
        size=20, 
        weight="bold"
    )

    # =================================================================
    # 로직 (단순 클릭 이벤트)
    # =================================================================
    def update_view():
        # 원 속성 적용
        the_circle.width = state["diameter"]
        the_circle.height = state["diameter"]
        the_circle.border_radius = state["diameter"] / 2
        the_circle.opacity = state["brightness"] / 100.0
        
        # 텍스트 업데이트
        txt_info.value = f"D: {state['diameter']}px | B: {state['brightness']}%"
        
        # 화면 갱신
        the_circle.update()
        txt_info.update()

    def change_size(delta):
        # 크기 조절 (최소 50 ~ 최대 1200)
        new_size = state["diameter"] + delta
        if 50 <= new_size <= 1200:
            state["diameter"] = new_size
            update_view()

    def change_bright(delta):
        # 밝기 조절 (최소 10 ~ 최대 100)
        new_bright = state["brightness"] + delta
        if 10 <= new_bright <= 100:
            state["brightness"] = new_bright
            update_view()

    def toggle_mode(e):
        state["is_flash"] = not state["is_flash"]
        if state["is_flash"]:
            page.bgcolor = "white"
            controls_stack.visible = False
            the_circle.visible = False # 원도 숨김 (완전 흰색)
        else:
            page.bgcolor = "black"
            controls_stack.visible = True
            the_circle.visible = True
        page.update()

    # =================================================================
    # 버튼 생성기 (반복 코드 줄이기)
    # =================================================================
    def create_btn(icon, func, data):
        return ft.IconButton(
            icon=icon, 
            icon_color="white", 
            icon_size=30,
            on_click=lambda e: func(data),
            style=ft.ButtonStyle(
                bgcolor=ft.colors.with_opacity(0.2, "grey"), 
                shape=ft.CircleBorder(),
                padding=15
            )
        )

    # 버튼들
    btn_size_up = create_btn(ft.icons.ADD, change_size, 50)     # 50px씩 증가
    btn_size_down = create_btn(ft.icons.REMOVE, change_size, -50) # 50px씩 감소
    
    btn_bright_up = create_btn(ft.icons.BRIGHTNESS_7, change_bright, 10)   # 10% 증가
    btn_bright_down = create_btn(ft.icons.BRIGHTNESS_5, change_bright, -10) # 10% 감소

    btn_mode = ft.IconButton(
        icon=ft.icons.FLASHLIGHT_ON, 
        icon_color="yellow", 
        icon_size=30,
        on_click=toggle_mode
    )

    # =================================================================
    # 레이아웃: Stack을 이용한 절대 위치 배치
    # (Row/Column 계산 오류 방지)
    # =================================================================
    
    # 컨트롤 패널 덩어리
    controls_stack = ft.Stack(
        controls=[
            # 상단 정보 텍스트
            ft.Container(content=txt_info, top=0, left=0, right=0, alignment=ft.alignment.center),
            
            # 크기 조절 버튼 (왼쪽)
            ft.Container(content=btn_size_down, bottom=0, left=20),
            ft.Container(content=btn_size_up, bottom=0, left=100),
            ft.Container(content=ft.Text("Size", color="grey"), bottom=60, left=50),

            # 밝기 조절 버튼 (오른쪽)
            ft.Container(content=btn_bright_down, bottom=0, right=100),
            ft.Container(content=btn_bright_up, bottom=0, right=20),
            ft.Container(content=ft.Text("Bright", color="grey"), bottom=60, right=45),
        ],
        width=400, # 패널 너비 제한
        height=150,
    )

    # 최종 화면 구성
    # Stack으로 쌓아서 위치 고정
    page.add(
        ft.Stack(
            controls=[
                # 1. 중앙 원
                ft.Container(content=the_circle, alignment=ft.alignment.center),
                
                # 2. 모드 버튼 (좌측 상단 고정)
                ft.Container(content=btn_mode, top=20, left=20),
                
                # 3. 컨트롤러 (하단 중앙 고정)
                ft.Container(
                    content=controls_stack, 
                    bottom=20, 
                    left=0, 
                    right=0, 
                    alignment=ft.alignment.bottom_center
                )
            ],
            expand=True
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
