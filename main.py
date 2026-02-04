import flet as ft

def main(page: ft.Page):
    # 1. 기본 설정
    page.title = "Text Controls"
    page.bgcolor = "black"
    page.scroll = ft.ScrollMode.AUTO # 스크롤 켜서 잘림 방지
    page.padding = 20

    # 2. 상태값
    state = {
        "size": 300,
        "bright": 100,
        "mode_flash": False
    }

    # =================================================================
    # UI 컴포넌트 (아이콘 절대 사용 금지)
    # =================================================================

    # [상태 텍스트]
    txt_info = ft.Text(
        value="크기: 300px | 밝기: 100%", 
        color="white", 
        size=20
    )

    # [중앙 원]
    the_circle = ft.Container(
        width=300,
        height=300,
        bgcolor=ft.colors.WHITE,
        border_radius=150, # 원 모양
        alignment=ft.alignment.center,
    )

    # =================================================================
    # 로직
    # =================================================================
    def update_view():
        # 1. 원 업데이트
        the_circle.width = state["size"]
        the_circle.height = state["size"]
        the_circle.border_radius = state["size"] / 2
        the_circle.opacity = state["bright"] / 100.0
        
        # 2. 텍스트 업데이트
        txt_info.value = f"크기: {state['size']}px | 밝기: {state['bright']}%"
        
        # 3. 화면 반영
        the_circle.update()
        txt_info.update()

    # 버튼 이벤트들
    def size_up(e):
        if state["size"] < 1000:
            state["size"] += 50
            update_view()

    def size_down(e):
        if state["size"] > 50:
            state["size"] -= 50
            update_view()

    def bright_up(e):
        if state["bright"] < 100:
            state["bright"] += 10
            update_view()

    def bright_down(e):
        if state["bright"] > 10:
            state["bright"] -= 10
            update_view()

    def toggle_flash(e):
        state["mode_flash"] = not state["mode_flash"]
        if state["mode_flash"]:
            page.bgcolor = "white"
            controls.visible = False # 컨트롤 숨김
            the_circle.visible = False # 원 숨김 (완전 흰색)
        else:
            page.bgcolor = "black"
            controls.visible = True
            the_circle.visible = True
        page.update()

    # =================================================================
    # 컨트롤 패널 (순수 텍스트 버튼 사용)
    # =================================================================
    
    # [스타일] 잘 보이는 큰 버튼
    def make_btn(text, func, color="blue"):
        return ft.ElevatedButton(
            text=text, 
            on_click=func,
            bgcolor=color,
            color="white",
            height=50,
            width=80
        )

    # 컨트롤 영역
    controls = ft.Column(
        controls=[
            ft.Divider(color="grey"),
            txt_info,
            ft.Divider(color="transparent", height=10),
            
            ft.Text("크기 조절", color="grey"),
            ft.Row(
                [make_btn("- 작게", size_down), make_btn("+ 크게", size_up)], 
                alignment=ft.MainAxisAlignment.CENTER
            ),
            
            ft.Divider(color="transparent", height=10),
            
            ft.Text("밝기 조절", color="grey"),
            ft.Row(
                [make_btn("- 어둡게", bright_down), make_btn("+ 밝게", bright_up)], 
                alignment=ft.MainAxisAlignment.CENTER
            ),
            
            ft.Divider(color="transparent", height=20),
            
            # 플래시 버튼 (노란색)
            ft.ElevatedButton(
                text="플래시 모드 (흰색)", 
                on_click=toggle_flash,
                bgcolor="amber",
                color="black",
                height=60,
                width=200
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # =================================================================
    # 최종 레이아웃 (Column 사용 - 가장 안전함)
    # =================================================================
    page.add(
        ft.Column(
            controls=[
                # 상단 여백
                ft.Container(height=20),
                
                # 원이 들어갈 공간 (높이 고정하여 UI 밀림 방지)
                ft.Container(
                    content=the_circle,
                    alignment=ft.alignment.center,
                    height=500, # 넉넉하게 공간 확보
                ),
                
                # 하단 컨트롤 패널
                controls
            ],
            scroll=ft.ScrollMode.AUTO, # 화면 넘치면 스크롤 가능
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
