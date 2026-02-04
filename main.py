import flet as ft

def main(page: ft.Page):
    # 1. 페이지 설정 (최적화)
    page.title = "FlatPanel Native"
    page.bgcolor = "black"
    page.padding = 0
    page.spacing = 0
    
    # 2. 안전 영역 확보
    page.safe_area_top = True
    page.safe_area_bottom = True

    # 3. 상태값
    state = {
        "diameter": 300.0,
        "brightness": 1.0,
        "is_flash": False
    }

    # =================================================================
    # UI 컴포넌트 (순정 부품 사용)
    # =================================================================

    # [중앙 원]
    # 애니메이션과 그림자를 뺐습니다. (안정성 최우선)
    the_circle = ft.Container(
        width=300,
        height=300,
        bgcolor=ft.colors.WHITE,
        border_radius=150,
        alignment=ft.alignment.center,
    )

    # [값 표시 텍스트]
    txt_size = ft.Text("Diameter: 300px", color="white", size=14)
    txt_bright = ft.Text("Brightness: 100%", color="white", size=14)

    # [이벤트 핸들러]
    def update_ui():
        # 원 업데이트
        the_circle.width = state["diameter"]
        the_circle.height = state["diameter"]
        the_circle.border_radius = state["diameter"] / 2
        the_circle.opacity = state["brightness"]
        the_circle.update()
        
        # 텍스트 업데이트
        txt_size.value = f"Diameter: {int(state['diameter'])}px"
        txt_bright.value = f"Brightness: {int(state['brightness']*100)}%"
        txt_size.update()
        txt_bright.update()

    def on_size_change(e):
        state["diameter"] = float(e.control.value)
        update_ui()

    def on_bright_change(e):
        state["brightness"] = float(e.control.value)
        update_ui()

    # [모드 전환 로직]
    # 복잡한 Overlay 대신, 페이지 배경색을 바꿔버리는 가장 확실한 방법 사용
    def toggle_mode(e):
        state["is_flash"] = not state["is_flash"]
        
        if state["is_flash"]:
            # 플래시 모드: 배경 흰색, 컨트롤 숨김
            page.bgcolor = "white"
            ctrl_panel.visible = False
            btn_mode.icon = "flashlight_off"
            btn_mode.icon_color = "black"
            # 원도 숨겨야 완벽한 흰색이 됨 (혹은 원을 꽉 채우거나)
            the_circle.visible = False 
        else:
            # 컨트롤 모드: 배경 검정, 컨트롤 보임
            page.bgcolor = "black"
            ctrl_panel.visible = True
            btn_mode.icon = "flashlight_on"
            btn_mode.icon_color = "white"
            the_circle.visible = True

        page.update()
        btn_mode.update()
        the_circle.update()
        ctrl_panel.update()

    # =================================================================
    # 컨트롤 패널 (Native Slider 사용)
    # =================================================================
    
    # 1. 밝기 슬라이더 (순정)
    slider_bright = ft.Slider(
        min=0.1, max=1.0, value=1.0, 
        divisions=20, 
        label="{value}", 
        on_change=on_bright_change
    )
    
    # 2. 크기 슬라이더 (순정)
    slider_size = ft.Slider(
        min=50, max=900, value=300, 
        divisions=50, 
        label="{value}", 
        on_change=on_size_change
    )

    # 패널 조립 (우측 사이드바 형태)
    ctrl_panel = ft.Container(
        width=250,
        bgcolor=ft.colors.with_opacity(0.1, "white"),
        padding=20,
        border_radius=10,
        content=ft.Column(
            controls=[
                ft.Text("CONTROLS", color="grey", weight="bold"),
                ft.Divider(color="grey"),
                
                ft.Text("Brightness", color="white"),
                slider_bright,
                txt_bright,
                
                ft.Divider(height=20, color="transparent"), # 여백
                
                ft.Text("Diameter", color="white"),
                slider_size,
                txt_size,
            ],
            scroll=ft.ScrollMode.AUTO # 화면 넘치면 스크롤
        )
    )

    # 모드 버튼
    btn_mode = ft.IconButton(
        icon="flashlight_on", 
        icon_color="white", 
        icon_size=30,
        on_click=toggle_mode
    )

    # =================================================================
    # 최종 레이아웃 (Row 사용)
    # Stack 대신 Row를 사용하여 렌더링 충돌을 방지합니다.
    # =================================================================
    
    # 왼쪽: 원이 있는 공간 (꽉 채움)
    left_area = ft.Container(
        content=the_circle,
        alignment=ft.alignment.center,
        expand=True # 남은 공간 다 쓰기
    )

    # 오른쪽: 컨트롤 패널 + 버튼
    right_area = ft.Column(
        controls=[
            ft.Container(content=btn_mode, alignment=ft.alignment.center_right, padding=10),
            ctrl_panel,
            ft.Container(height=20) # 하단 여백
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.END
    )

    # 전체 배치
    page.add(
        ft.Row(
            controls=[left_area, right_area],
            expand=True
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
