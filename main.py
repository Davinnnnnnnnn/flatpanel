import flet as ft

# =============================================================================
# 1. 안전한 슬라이더 (Blur 제거, 기능 유지)
# =============================================================================
class SafePixelSlider(ft.Container):
    def __init__(self, value, min_v, max_v, on_change, icon_name):
        super().__init__()
        self.value = value
        self.min_v = min_v
        self.max_v = max_v
        self.cb_on_change = on_change
        
        # 디자인: 블러 대신 반투명 배경 사용 (안전함)
        self.bgcolor = ft.colors.with_opacity(0.15, ft.colors.GREY_200)
        self.border_radius = 12
        self.padding = 0
        self.clip_behavior = ft.ClipBehavior.HARD_EDGE
        self.width = 70  # 너비 고정
        self.height = 300 # 높이 기본값
        
        # 내부 채움 바
        self.fill_bar = ft.Container(
            bgcolor=ft.colors.with_opacity(0.8, ft.colors.WHITE),
            border_radius=12,
            width=70,
            height=0, # 초기값
            alignment=ft.alignment.bottom_center,
            animate=ft.animation.Animation(100, ft.AnimationCurve.LINEAR) # 가벼운 애니메이션
        )
        
        # 아이콘 및 텍스트
        self.icon_view = ft.Icon(icon_name, color=ft.colors.WHITE, size=20)
        self.label_view = ft.Text(
            "{:.0f}".format(value), 
            color=ft.colors.WHITE, 
            size=12, 
            weight="bold"
        )
        
        # 정보 표시창 (아이콘+텍스트)
        self.info_col = ft.Column(
            [self.label_view, self.icon_view],
            alignment=ft.MainAxisAlignment.END,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5
        )
        
        self.content = ft.Stack(
            controls=[
                # 1. 바닥 (터치 영역)
                ft.GestureDetector(
                    on_pan_update=self._on_pan,
                    on_tap_down=self._on_pan,
                    content=ft.Container(bgcolor=ft.colors.TRANSPARENT, expand=True)
                ),
                # 2. 채움 바 (아래 정렬)
                ft.Container(
                    content=self.fill_bar,
                    alignment=ft.alignment.bottom_center,
                    bottom=0, left=0, right=0
                ),
                # 3. 정보 (맨 위)
                ft.Container(
                    content=self.info_col,
                    alignment=ft.alignment.bottom_center,
                    bottom=15, left=0, right=0,
                    touchable=False # 터치 통과
                )
            ]
        )
        
        self._update_layout()

    def _on_pan(self, e: ft.DragUpdateEvent):
        # 높이 기준으로 값 계산
        h = self.height if self.height > 0 else 300
        y = max(0, min(h, e.local_y))
        ratio = 1 - (y / h) # 아래가 0, 위가 1
        
        self.value = self.min_v + (self.max_v - self.min_v) * ratio
        self._update_layout()
        if self.cb_on_change:
            self.cb_on_change(self.value)

    def _update_layout(self):
        # 텍스트 업데이트
        if self.max_v > 10: # 크기(px) 모드
             self.label_view.value = f"{int(self.value)}"
        else: # 밝기(%) 모드
             self.label_view.value = f"{int(self.value * 100)}%"
        
        # 바 높이 업데이트
        ratio = (self.value - self.min_v) / (self.max_v - self.min_v)
        self.fill_bar.height = self.height * ratio
        self.fill_bar.update()
        self.label_view.update()

# =============================================================================
# 2. 메인 앱
# =============================================================================
def main(page: ft.Page):
    page.bgcolor = "black"
    page.padding = 0
    page.spacing = 0
    
    # [중요] 상태바 영역 침범 방지
    page.safe_area_top = True
    page.safe_area_bottom = True

    # 상태 변수
    state = {
        "diameter": 300.0,
        "brightness": 1.0,
        "mode": "control" # 'control' or 'flash'
    }

    # ---------------------------------------------------------
    # UI 컴포넌트
    # ---------------------------------------------------------
    
    # 1. 중앙 원 (단색, 그림자 제거 -> 안전함)
    the_circle = ft.Container(
        width=300,
        height=300,
        bgcolor=ft.colors.WHITE,
        border_radius=150,
        alignment=ft.alignment.center,
        animate_opacity=200 # 투명도 애니메이션은 안전함
    )

    # 2. 플래시 오버레이 (화면 덮개)
    flash_overlay = ft.Container(
        bgcolor=ft.colors.WHITE,
        opacity=0,
        visible=False,
        expand=True,
        animate_opacity=300
    )

    # 3. 로직 함수
    def update_circle():
        the_circle.width = state["diameter"]
        the_circle.height = state["diameter"]
        the_circle.border_radius = state["diameter"] / 2
        the_circle.opacity = state["brightness"]
        the_circle.update()

    def on_size_change(v):
        state["diameter"] = v
        update_circle()

    def on_bright_change(v):
        state["brightness"] = v
        update_circle()

    def toggle_mode(e):
        if state["mode"] == "control":
            # 플래시 모드로 전환
            state["mode"] = "flash"
            flash_overlay.opacity = 1
            flash_overlay.visible = True
            panel_container.opacity = 0 # 패널 숨김
            btn_mode.icon = "flashlight_off"
            btn_mode.icon_color = "black"
        else:
            # 컨트롤 모드로 전환
            state["mode"] = "control"
            flash_overlay.opacity = 0
            flash_overlay.visible = False
            panel_container.opacity = 1 # 패널 보임
            btn_mode.icon = "flashlight_on"
            btn_mode.icon_color = "white"
            
        flash_overlay.update()
        panel_container.update()
        btn_mode.update()

    # 4. 컨트롤 패널 조립
    slider_bright = SafePixelSlider(1.0, 0.1, 1.0, on_bright_change, "brightness_6")
    slider_size = SafePixelSlider(300, 50, 900, on_size_change, "aspect_ratio") # 최대크기 900
    
    # 슬라이더 높이 설정 (화면 꽉 차게)
    # 탭 S10 Ultra 높이가 큼 -> 넉넉하게 500으로 설정
    slider_bright.height = 500
    slider_size.height = 500

    panel_row = ft.Row(
        [slider_bright, slider_size],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER
    )

    panel_container = ft.Container(
        content=panel_row,
        padding=20,
        alignment=ft.alignment.center_right,
        animate_opacity=300
    )

    btn_mode = ft.IconButton(
        icon="flashlight_on",
        icon_color="white",
        icon_size=30,
        on_click=toggle_mode,
        style=ft.ButtonStyle(bgcolor=ft.colors.with_opacity(0.2, "white"), shape=ft.CircleBorder(), padding=15)
    )

    # ---------------------------------------------------------
    # 레이아웃 배치
    # ---------------------------------------------------------
    layout = ft.Stack(
        controls=[
            # 1. 원 (정중앙)
            ft.Container(content=the_circle, alignment=ft.alignment.center),
            
            # 2. 플래시 (전체 화면)
            flash_overlay,
            
            # 3. 컨트롤 패널 (오른쪽 정렬)
            ft.Container(
                content=panel_container, 
                alignment=ft.alignment.center_right,
                padding=ft.padding.only(right=30)
            ),
            
            # 4. 모드 버튼 (왼쪽 상단)
            ft.Container(
                content=btn_mode, 
                alignment=ft.alignment.top_left,
                padding=30
            )
        ],
        expand=True
    )

    page.add(layout)
    
    # 초기화
    update_circle()

if __name__ == "__main__":
    ft.app(target=main)
