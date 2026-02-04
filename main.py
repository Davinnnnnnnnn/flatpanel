import flet as ft

# =============================================================================
# Google Pixel Style Slider (그대로 유지)
# =============================================================================
class PixelSlider(ft.Container):
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
        
        self.track_length = 200.0 
        
        self.blur = ft.Blur(10, 10, ft.BlurTileMode.CLAMP)
        self.bgcolor = ft.colors.with_opacity(0.1, ft.colors.GREY_900)
        self.border_radius = 16
        self.clip_behavior = ft.ClipBehavior.HARD_EDGE
        self.padding = 0
        
        self.fill_bar = ft.Container(
            bgcolor=ft.colors.with_opacity(0.25, ft.colors.WHITE),
            border_radius=16,
            animate=ft.animation.Animation(100, ft.AnimationCurve.EASE_OUT),
        )
        
        text_color = ft.colors.with_opacity(0.5, ft.colors.WHITE)
        
        self.icon_view = ft.Icon(icon, color=text_color, size=18)
        self.label_view = ft.Text(
            value=self.label_format.format(value), 
            color=text_color, 
            weight=ft.FontWeight.W_600,
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
        if length < 10: length = 100
        self.track_length = length
        self.update_visuals()

    def _build_layout(self):
        self.content_stack.controls.clear()
        
        if self.vertical:
            self.fill_bar.bottom = 0
            self.fill_bar.left = 0
            self.fill_bar.right = 0
            self.fill_bar.height = 0 
            
            info = ft.Container(
                content=ft.Column(
                    [self.label_view, self.icon_view],
                    alignment=ft.MainAxisAlignment.END,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=2
                ),
                alignment=ft.alignment.bottom_center,
                bottom=15, left=0, right=0
            )
            self.content_stack.controls = [self.fill_bar, info]
            
        else:
            self.fill_bar.left = 0
            self.fill_bar.top = 0
            self.fill_bar.bottom = 0
            self.fill_bar.width = 0 
            
            info = ft.Container(
                content=ft.Row(
                    [self.icon_view, self.label_view],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8
                ),
                alignment=ft.alignment.center_left,
                left=15, top=0, bottom=0
            )
            self.content_stack.controls = [self.fill_bar, info]

    def _on_pan(self, e: ft.DragUpdateEvent):
        limit = self.track_length
        if limit <= 0: limit = 1 
        
        if self.vertical:
            y = max(0, min(limit, e.local_y))
            ratio = 1 - (y / limit)
        else:
            x = max(0, min(limit, e.local_x))
            ratio = x / limit
            
        new_val = self.min_v + (self.max_v - self.min_v) * ratio
        new_val = max(self.min_v, min(self.max_v, new_val))
        
        self.value = new_val
        self.update_visuals()
        
        if self.cb_on_change:
            self.cb_on_change(new_val)

    def _apply_visuals_internal(self):
        self.label_view.value = self.label_format.format(self.value)
        if self.max_v == self.min_v: ratio = 0
        else: ratio = (self.value - self.min_v) / (self.max_v - self.min_v)
        ratio = max(0.0, min(1.0, ratio))
        
        if self.vertical: self.fill_bar.height = self.track_length * ratio
        else: self.fill_bar.width = self.track_length * ratio

    def update_visuals(self, val=None):
        if val is not None: self.value = val
        self._apply_visuals_internal()
        if self.fill_bar.page:
            self.fill_bar.update()
            self.label_view.update()


# =============================================================================
# Main App (수정된 버전)
# =============================================================================
def main(page: ft.Page):
    # 기본 설정
    page.title = "FlatPanel"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#000000"
    page.padding = 0
    page.spacing = 0
    # 모바일에서는 스크롤을 끄는 것이 레이아웃 안정성에 좋습니다.
    page.scroll = ft.ScrollMode.OFF 

    # 상태 값
    state = {
        "is_light_mode": False,
        "diameter": 300.0,
        "brightness": 1.0,
    }

    # ---------------------------------------------------------
    # UI Components
    # ---------------------------------------------------------
    
    # 1. 플래시 모드 (전체 화면 덮기)
    flash_overlay = ft.Container(
        expand=True, # 부모 크기에 맞춰 꽉 참
        bgcolor=ft.colors.WHITE,
        opacity=0,
        animate_opacity=ft.animation.Animation(500, ft.AnimationCurve.EASE_IN_OUT),
        visible=True,
        # 터치 이벤트가 아래로 전달되지 않게 막음
        on_click=lambda _: None 
    )

    # 2. 중앙 원 (Flat Frame용)
    the_circle = ft.Container(
        width=state["diameter"],
        height=state["diameter"],
        bgcolor=ft.colors.WHITE,
        border_radius=state["diameter"] / 2,
        opacity=state["brightness"],
        shadow=ft.BoxShadow(
            spread_radius=1, 
            blur_radius=100, 
            color=ft.colors.with_opacity(0.5, ft.colors.WHITE)
        ),
        animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT_CUBIC),
        animate_opacity=300,
        alignment=ft.alignment.center
    )

    # 3. 슬라이더 패널 (위치만 잡아두고 내용은 on_resize에서 채움)
    slider_panel = ft.Container(
        animate_opacity=ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT)
    )

    # 4. 모드 전환 버튼
    def toggle_mode(e):
        state["is_light_mode"] = not state["is_light_mode"]
        if state["is_light_mode"]:
            flash_overlay.opacity = 1
            slider_panel.opacity = 0
            e.control.icon = "flashlight_off"
            e.control.icon_color = ft.colors.BLACK54
            e.control.bgcolor = ft.colors.with_opacity(0.1, ft.colors.BLACK)
        else:
            flash_overlay.opacity = 0
            slider_panel.opacity = 1
            e.control.icon = "flashlight_on"
            e.control.icon_color = ft.colors.with_opacity(0.5, ft.colors.WHITE)
            e.control.bgcolor = ft.colors.with_opacity(0.1, ft.colors.WHITE)
        
        flash_overlay.update()
        slider_panel.update()
        e.control.update()

    mode_btn = ft.IconButton(
        icon="flashlight_on",
        icon_color=ft.colors.with_opacity(0.5, ft.colors.WHITE),
        bgcolor=ft.colors.with_opacity(0.1, ft.colors.WHITE),
        icon_size=24,
        on_click=toggle_mode,
        style=ft.ButtonStyle(shape=ft.CircleBorder(), padding=15)
    )

    # ---------------------------------------------------------
    # Layout Strategy (여기가 핵심 수정)
    # ---------------------------------------------------------
    
    # Stack에 expand=True를 주어 화면 전체를 쓰게 만듭니다.
    # 수동으로 width/height를 주지 않습니다.
    main_layout = ft.Stack(
        expand=True, 
        controls=[
            ft.Container(content=the_circle, alignment=ft.alignment.center, expand=True),
            flash_overlay, 
            slider_panel,
            ft.Container(content=mode_btn, padding=20) # 버튼 위치 제어를 위한 컨테이너
        ],
    )

    # 로직 함수들
    def update_circle_props():
        the_circle.width = state["diameter"]
        the_circle.height = state["diameter"]
        the_circle.border_radius = state["diameter"] / 2
        the_circle.opacity = state["brightness"]
        the_circle.shadow.blur_radius = 60 + (state["diameter"] / 8)
        if the_circle.page: the_circle.update()

    def on_size_change(val):
        state["diameter"] = val
        update_circle_props()

    def on_brightness_change(val):
        state["brightness"] = val
        update_circle_props()

    # ---------------------------------------------------------
    # Resize Logic (UI 배치만 담당, 전체 크기 조절 X)
    # ---------------------------------------------------------
    def on_resize(e):
        # 방어 코드: 모바일에서 초기에 page.width가 0이나 None일 수 있음
        if not page.width or not page.height:
            return

        w = page.width
        h = page.height
        
        # 가로/세로 모드 판단
        is_portrait = w < h
        
        # 슬라이더 최대 크기 제한
        limit_size = max(w, h) * 1.2 

        # 기존 슬라이더 제거 후 재생성 (Clean한 상태 유지)
        # 주의: 실제 앱에서는 컨트롤을 재사용하는 게 좋지만, 여기선 방향 전환이 확실하므로 재생성
        
        if is_portrait:
            # [세로 모드] UI 배치
            bar_height = 48
            track_len = w - 60 # 여백 고려
            
            s_bright = PixelSlider(
                state["brightness"], 0.1, 1.0, on_brightness_change,
                vertical=False, icon="brightness_6", label_format="{:.0%}"
            )
            s_bright.set_track_length(track_len)
            s_bright.height = bar_height
            
            s_size = PixelSlider(
                state["diameter"], 50, limit_size, on_size_change,
                vertical=False, icon="aspect_ratio", label_format="{:.0f} px"
            )
            s_size.set_track_length(track_len)
            s_size.height = bar_height

            # 슬라이더 패널 위치 (하단)
            slider_panel.width = w
            slider_panel.height = 160
            slider_panel.left = 0
            slider_panel.right = 0
            slider_panel.bottom = 0
            slider_panel.top = None
            
            slider_panel.content = ft.Column(
                controls=[s_bright, s_size],
                spacing=15,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
            slider_panel.padding = ft.padding.only(bottom=30, top=10)

            # 모드 버튼 위치 (우측 하단, 패널 위)
            # Stack 내의 Container를 통해 위치 제어
            main_layout.controls[-1].alignment = ft.alignment.bottom_right
            main_layout.controls[-1].padding = ft.padding.only(right=20, bottom=170)

        else:
            # [가로 모드] UI 배치 (갤럭시탭 S10 Ultra는 주로 여기 해당)
            bar_width = 60
            track_len = h - 60
            
            s_bright = PixelSlider(
                state["brightness"], 0.1, 1.0, on_brightness_change,
                vertical=True, icon="brightness_6", label_format="{:.0%}"
            )
            s_bright.set_track_length(track_len)
            s_bright.width = bar_width
            
            s_size = PixelSlider(
                state["diameter"], 50, limit_size, on_size_change,
                vertical=True, icon="aspect_ratio", label_format="{:.0f} px"
            )
            s_size.set_track_length(track_len)
            s_size.width = bar_width

            # 슬라이더 패널 위치 (우측)
            slider_panel.width = 180
            slider_panel.height = h
            slider_panel.right = 0
            slider_panel.top = 0
            slider_panel.bottom = 0
            slider_panel.left = None
            
            slider_panel.content = ft.Row(
                controls=[s_bright, s_size],
                spacing=15,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
            slider_panel.padding = ft.padding.only(right=30, left=10)

            # 모드 버튼 위치 (좌측 상단)
            main_layout.controls[-1].alignment = ft.alignment.top_left
            main_layout.controls[-1].padding = ft.padding.all(20)

        page.update()

    page.on_resized = on_resize

    # [중요] 최상위 컨테이너 추가
    # expand=True를 사용하여 화면 전체를 채웁니다.
    page.add(main_layout)
    
    # 초기 렌더링 강제 실행 (약간의 딜레이를 주면 안전할 수 있으나, 지금은 직접 호출)
    # page.width가 0일 경우 on_resize 내부 가드에 의해 무시됨 -> 화면이 보이기 시작하면 이벤트가 다시 발생하여 그려짐
    if page.width and page.width > 0:
        on_resize(None)

if __name__ == "__main__":
    ft.app(target=main)
