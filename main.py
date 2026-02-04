import flet as ft

# =============================================================================
# Google Pixel Style Slider Class (Tablet Optimized & Crash Free)
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
        
        # 트랙 길이 안전장치 (0이 들어오면 기본값 200 사용)
        self.track_length = 200.0 
        
        # Glassmorphism
        self.blur = ft.Blur(10, 10, ft.BlurTileMode.CLAMP)
        
        # 디자인
        self.bgcolor = ft.colors.with_opacity(0.1, ft.colors.GREY_900)
        self.border_radius = 16
        self.clip_behavior = ft.ClipBehavior.HARD_EDGE
        self.padding = 0
        
        # 채움 바
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
        # 길이가 너무 작거나 0이면 안전값 사용
        if length < 10: 
            length = 100
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
        
        if self.max_v == self.min_v:
            ratio = 0
        else:
            ratio = (self.value - self.min_v) / (self.max_v - self.min_v)
        
        ratio = max(0.0, min(1.0, ratio))
        
        if self.vertical:
            self.fill_bar.height = self.track_length * ratio
        else:
            self.fill_bar.width = self.track_length * ratio

    def update_visuals(self, val=None):
        if val is not None:
            self.value = val
        self._apply_visuals_internal()
        if self.fill_bar.page:
            self.fill_bar.update()
            self.label_view.update()


# =============================================================================
# Main App
# =============================================================================
def main(page: ft.Page):
    # 1. 페이지 초기 설정
    page.title = "FlatPanel"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#000000"
    
    # [핵심 수정 1] 스크롤 끄기: 모바일에서 expand=True가 작동하려면 스크롤이 꺼져 있어야 함
    page.scroll = ft.ScrollMode.OFF 
    
    # [핵심 수정 2] 패딩/간격 제거 및 정렬: 콘텐츠 붕괴 방지
    page.padding = 0
    page.spacing = 0
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # 상태 변수
    state = {
        "is_light_mode": False,
        "diameter": 300.0,
        "brightness": 1.0,
    }

    # UI 컴포넌트
    flash_overlay = ft.Container(
        expand=True,
        bgcolor=ft.colors.WHITE,
        opacity=0,
        animate_opacity=ft.animation.Animation(500, ft.AnimationCurve.EASE_IN_OUT),
        visible=True,
    )

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

    slider_panel = ft.Container(
        animate_opacity=ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT)
    )

    # 로직 핸들러
    def update_circle_props():
        the_circle.width = state["diameter"]
        the_circle.height = state["diameter"]
        the_circle.border_radius = state["diameter"] / 2
        the_circle.opacity = state["brightness"]
        the_circle.shadow.blur_radius = 60 + (state["diameter"] / 8)
        the_circle.update()

    def on_size_change(val):
        state["diameter"] = val
        update_circle_props()

    def on_brightness_change(val):
        state["brightness"] = val
        update_circle_props()

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

    # [핵심 수정 3] 화면 크기 감지 및 안전장치
    def on_resize(e):
        # 갤럭시 탭 등에서 초기 width가 0일 경우를 대비해 기본값(태블릿 가로 모드 기준) 설정
        safe_w = page.width if page.width and page.width > 0 else 1200
        safe_h = page.height if page.height and page.height > 0 else 800
        
        w = safe_w
        h = safe_h
        
        is_portrait = w < h
        limit_size = max(w, h) * 1.5

        if is_portrait:
            # [세로 모드]
            bar_height = 48
            track_len = w - 40
            if track_len < 50: track_len = 300 # 안전값

            s_bright = PixelSlider(
                state["brightness"], 0.1, 1.0, on_brightness_change,
                vertical=False, icon="brightness_6", label_format="{:.0%}"
            )
            s_bright.height = bar_height
            s_bright.expand = True 
            s_bright.set_track_length(track_len) 
            
            s_size = PixelSlider(
                state["diameter"], 50, limit_size, on_size_change,
                vertical=False, icon="aspect_ratio", label_format="{:.0f} px"
            )
            s_size.height = bar_height
            s_size.expand = True 
            s_size.set_track_length(track_len)

            slider_panel.width = w
            slider_panel.height = 150 
            slider_panel.left = 0
            slider_panel.right = 0
            slider_panel.bottom = 0
            slider_panel.top = None
            
            slider_panel.content = ft.Column(
                controls=[s_bright, s_size],
                spacing=12,
                alignment=ft.MainAxisAlignment.CENTER
            )
            slider_panel.padding = ft.padding.only(left=20, right=20, bottom=30, top=10)
            
            mode_btn.top = None
            mode_btn.bottom = 160 
            mode_btn.right = 20
            mode_btn.left = None

        else:
            # [가로 모드]
            bar_width = 60
            track_len = h - 40
            if track_len < 50: track_len = 300 # 안전값

            s_bright = PixelSlider(
                state["brightness"], 0.1, 1.0, on_brightness_change,
                vertical=True, icon="brightness_6", label_format="{:.0%}"
            )
            s_bright.width = bar_width
            s_bright.expand = True
            s_bright.set_track_length(track_len)
            
            s_size = PixelSlider(
                state["diameter"], 50, limit_size, on_size_change,
                vertical=True, icon="aspect_ratio", label_format="{:.0f} px"
            )
            s_size.width = bar_width
            s_size.expand = True
            s_size.set_track_length(track_len)

            slider_panel.width = 160 
            slider_panel.height = h
            slider_panel.right = 0
            slider_panel.top = 0
            slider_panel.bottom = 0
            slider_panel.left = None
            
            slider_panel.content = ft.Row(
                controls=[s_bright, s_size],
                spacing=12,
                alignment=ft.MainAxisAlignment.CENTER
            )
            slider_panel.padding = ft.padding.only(top=20, bottom=20, right=20, left=10)
            
            mode_btn.top = 20
            mode_btn.left = 20
            mode_btn.bottom = None
            mode_btn.right = None

        # UI 업데이트
        if slider_panel.page: slider_panel.update()
        if mode_btn.page: mode_btn.update()

    page.on_resized = on_resize

    # [중요] 레이아웃 구성: Stack을 사용하여 전체 화면 강제
    layout = ft.Stack(
        controls=[
            ft.Container(content=the_circle, alignment=ft.alignment.center),
            flash_overlay, 
            slider_panel,
            mode_btn
        ],
        expand=True, # Stack이 부모(Page) 크기를 꽉 채우도록 함
        alignment=ft.alignment.center
    )

    page.add(layout)
    
    # [핵심 수정 4] 초기 렌더링 강제 실행
    # 앱이 켜지자마자 기본값으로라도 UI를 그려서 검은 화면 방지
    on_resize(None)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
