import flet as ft

# =============================================================================
# Simple Slider (블러/그림자/애니메이션 제거 버전)
# =============================================================================
class SimpleSlider(ft.Container):
    def __init__(
        self, 
        value: float, 
        min_v: float, 
        max_v: float, 
        on_change, 
        vertical: bool = False, 
        icon: str = "circle", 
        label_format: str = "{:.0f}"
    ):
        super().__init__()
        self.value = value
        self.min_v = min_v
        self.max_v = max_v
        self.cb_on_change = on_change
        self.vertical = vertical
        self.label_format = label_format
        
        # [수정] 블러(Blur) 제거 -> 투명도만 사용
        self.bgcolor = ft.colors.with_opacity(0.2, ft.colors.GREY_500)
        self.border_radius = 16
        self.padding = 0
        
        # 채움 바 (애니메이션 제거)
        self.fill_bar = ft.Container(
            bgcolor=ft.colors.with_opacity(0.8, ft.colors.WHITE),
            border_radius=16,
        )
        
        self.icon_view = ft.Icon(icon, color=ft.colors.WHITE, size=18)
        self.label_view = ft.Text(
            value=self.label_format.format(value), 
            color=ft.colors.WHITE, 
            weight=ft.FontWeight.BOLD,
            size=13
        )

        self.content_stack = ft.Stack()
        self.content = ft.GestureDetector(
            content=self.content_stack,
            on_pan_update=self._on_pan,
            on_tap_down=self._on_pan, 
        )
        self._build_layout()
        self._apply_visuals_internal()

    def set_track_length(self, length: float):
        self.track_length = length if length > 50 else 200
        self.update_visuals()

    def _build_layout(self):
        self.content_stack.controls.clear()
        if self.vertical:
            self.fill_bar.bottom = 0; self.fill_bar.left = 0; self.fill_bar.right = 0; self.fill_bar.height = 0
            info = ft.Container(content=ft.Column([self.label_view, self.icon_view], alignment="end", spacing=2), bottom=15, left=0, right=0, alignment=ft.alignment.bottom_center)
            self.content_stack.controls = [self.fill_bar, info]
        else:
            self.fill_bar.left = 0; self.fill_bar.top = 0; self.fill_bar.bottom = 0; self.fill_bar.width = 0
            info = ft.Container(content=ft.Row([self.icon_view, self.label_view], alignment="start", spacing=8), left=15, top=0, bottom=0, alignment=ft.alignment.center_left)
            self.content_stack.controls = [self.fill_bar, info]

    def _on_pan(self, e: ft.DragUpdateEvent):
        limit = self.track_length
        if limit <= 0: limit = 1
        if self.vertical:
            ratio = 1 - (max(0, min(limit, e.local_y)) / limit)
        else:
            ratio = max(0, min(limit, e.local_x)) / limit
        self.value = max(self.min_v, min(self.max_v, self.min_v + (self.max_v - self.min_v) * ratio))
        self.update_visuals()
        if self.cb_on_change: self.cb_on_change(self.value)

    def _apply_visuals_internal(self):
        self.label_view.value = self.label_format.format(self.value)
        ratio = (self.value - self.min_v) / (self.max_v - self.min_v) if self.max_v != self.min_v else 0
        if self.vertical: self.fill_bar.height = self.track_length * ratio
        else: self.fill_bar.width = self.track_length * ratio

    def update_visuals(self):
        self._apply_visuals_internal()
        self.fill_bar.update()
        self.label_view.update()

# =============================================================================
# Main App (GPU Safe Mode)
# =============================================================================
def main(page: ft.Page):
    # 페이지 설정
    page.bgcolor = ft.colors.BLACK
    page.padding = 0
    page.spacing = 0
    
    # [중요] SafeArea 사용 (노치/상태표시줄 침범 방지)
    page.safe_area_top = True
    page.safe_area_bottom = True

    state = {"diameter": 300.0, "brightness": 1.0, "mode": False}

    # [수정] 그림자(Shadow)와 애니메이션 제거한 원
    the_circle = ft.Container(
        width=300,
        height=300,
        bgcolor=ft.colors.WHITE,
        border_radius=150,
        alignment=ft.alignment.center
    )

    # 플래시 화면
    flash_overlay = ft.Container(bgcolor=ft.colors.WHITE, opacity=0, visible=False, expand=True)

    def update_props():
        the_circle.width = state["diameter"]
        the_circle.height = state["diameter"]
        the_circle.border_radius = state["diameter"] / 2
        the_circle.opacity = state["brightness"]
        the_circle.update()

    # 슬라이더 콜백
    def on_size(v): state["diameter"] = v; update_props()
    def on_bright(v): state["brightness"] = v; update_props()

    # 모드 전환
    def toggle_mode(e):
        state["mode"] = not state["mode"]
        if state["mode"]:
            flash_overlay.opacity = 1; flash_overlay.visible = True
            panel_container.opacity = 0
        else:
            flash_overlay.opacity = 0; flash_overlay.visible = False
            panel_container.opacity = 1
        flash_overlay.update(); panel_container.update()

    # 컨트롤 패널 구성
    s_bright = SimpleSlider(1.0, 0.1, 1.0, on_bright, vertical=True, icon="brightness_6", label_format="{:.0%}")
    s_bright.set_track_length(400); s_bright.width = 60; s_bright.expand = True
    
    s_size = SimpleSlider(300, 50, 800, on_size, vertical=True, icon="aspect_ratio", label_format="{:.0f}")
    s_size.set_track_length(400); s_size.width = 60; s_size.expand = True

    panel_content = ft.Row([s_bright, s_size], spacing=20, alignment="center")
    
    # [수정] 정렬을 위해 Container로 감쌈 (위치 고정)
    panel_container = ft.Container(
        content=panel_content,
        width=200,
        padding=20,
        alignment=ft.alignment.center_right
    )

    btn_mode = ft.IconButton(icon="flashlight_on", on_click=toggle_mode, icon_color="white")

    # [핵심] Stack 레이아웃 (Expand 필수)
    layout = ft.Stack(
        controls=[
            ft.Container(content=the_circle, alignment=ft.alignment.center), # 중앙 원
            flash_overlay, # 플래시
            ft.Container(content=panel_container, alignment=ft.alignment.center_right), # 우측 패널
            ft.Container(content=btn_mode, alignment=ft.alignment.top_left, padding=20) # 좌측 상단 버튼
        ],
        expand=True
    )

    page.add(layout)

if __name__ == "__main__":
    ft.app(target=main)
