import flet as ft

# =============================================================================
# Google Pixel Style Slider Class (Modern Glassmorphism Version)
# =============================================================================
class PixelSlider(ft.Container):
    def __init__(
        self, 
        value: float, 
        min_v: float, 
        max_v: float, 
        on_change, 
        vertical: bool = False, 
        icon: str = ft.icons.LENS,
        label_format: str = "{:.0f}"
    ):
        super().__init__()
        self.value = value
        self.min_v = min_v
        self.max_v = max_v
        self.cb_on_change = on_change
        self.vertical = vertical
        self.label_format = label_format
        
        self.track_length = 100.0 
        
        # [디자인 수정 1] Glassmorphism (오버랩 대응)
        # 빛이 슬라이더 뒤로 올 때 흐리게 보이도록 블러 처리 + 그림자 추가
        self.blur = ft.Blur(15, 15, ft.BlurTileMode.CLAMP)
        self.shadow = ft.BoxShadow(
            spread_radius=0,
            blur_radius=15,
            color=ft.colors.with_opacity(0.2, ft.colors.BLACK),
            offset=ft.Offset(0, 4)
        )
        
        # [디자인 수정 2] 배경 스타일 (더 얇아진 두께에 맞춰 R값 조정)
        self.bgcolor = ft.colors.with_opacity(0.1, ft.colors.GREY_900)
        self.border_radius = 16 # 두께가 얇아졌으므로 둥글기(R)도 약간 줄임
        self.clip_behavior = ft.ClipBehavior.HARD_EDGE
        self.padding = 0
        
        # 채움 바 (투명도 유지)
        self.fill_bar = ft.Container(
            bgcolor=ft.colors.with_opacity(0.25, ft.colors.WHITE),
            border_radius=16,
            animate=ft.animation.Animation(100, ft.AnimationCurve.EASE_OUT),
        )
        
        # 텍스트/아이콘 (가독성 확보를 위해 약간 더 진하게)
        text_color = ft.colors.with_opacity(0.5, ft.colors.WHITE)
        
        self.icon_view = ft.Icon(icon, color=text_color, size=18) # 아이콘 크기 약간 축소
        self.label_view = ft.Text(
            value=self.label_format.format(value), 
            color=text_color, 
            weight=ft.FontWeight.W_600,
            size=13 # 폰트 크기 약간 축소
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
        if length > 0:
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
    # [변경] 앱 제목 변경
    page.title = "FlatPanel"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.margin = 0
    page.bgcolor = "#000000"
    
    state = {
        "is_light_mode": False,
        "diameter": 300.0,
        "brightness": 1.0,
    }

    # 1. 플래시 오버레이
    flash_overlay = ft.Container(
        expand=True,
        bgcolor=ft.colors.WHITE,
        opacity=0,
        animate_opacity=ft.animation.Animation(500, ft.AnimationCurve.EASE_IN_OUT),
        visible=True,
    )

    # 2. 메인 원
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

    # 3. 슬라이더 패널
    slider_panel = ft.Container(
        animate_opacity=ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT)
    )

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
            e.control.icon = ft.icons.FLASHLIGHT_OFF
            e.control.icon_color = ft.colors.BLACK54
            e.control.bgcolor = ft.colors.with_opacity(0.1, ft.colors.BLACK)
        else:
            flash_overlay.opacity = 0
            slider_panel.opacity = 1
            e.control.icon = ft.icons.FLASHLIGHT_ON
            e.control.icon_color = ft.colors.with_opacity(0.5, ft.colors.WHITE)
            e.control.bgcolor = ft.colors.with_opacity(0.1, ft.colors.WHITE)
        
        flash_overlay.update()
        slider_panel.update()
        e.control.update()

    mode_btn = ft.IconButton(
        icon=ft.icons.FLASHLIGHT_ON,
        icon_color=ft.colors.with_opacity(0.5, ft.colors.WHITE),
        bgcolor=ft.colors.with_opacity(0.1, ft.colors.WHITE),
        icon_size=24,
        on_click=toggle_mode,
        style=ft.ButtonStyle(shape=ft.CircleBorder(), padding=15)
    )

    def on_resize(e):
        w = page.window_width if page.window_width else 400
        h = page.window_height if page.window_height else 800
        
        is_portrait = w < h
        limit_size = max(w, h) * 1.5

        if is_portrait:
            # [세로 모드]
            # [변경] 슬라이더 두께를 얇게 조정 (70 -> 48)
            bar_height = 48
            track_len = w - 40
            
            s_bright = PixelSlider(
                state["brightness"], 0.1, 1.0, on_brightness_change,
                vertical=False, icon=ft.icons.BRIGHTNESS_6, label_format="{:.0%}"
            )
            s_bright.height = bar_height
            s_bright.expand = True 
            s_bright.set_track_length(track_len) 
            
            s_size = PixelSlider(
                state["diameter"], 50, limit_size, on_size_change,
                vertical=False, icon=ft.icons.ASPECT_RATIO, label_format="{:.0f} px"
            )
            s_size.height = bar_height
            s_size.expand = True 
            s_size.set_track_length(track_len)

            slider_panel.width = w
            # 패널 전체 높이도 슬라이더가 얇아진 만큼 조정
            slider_panel.height = 150 
            slider_panel.left = 0
            slider_panel.right = 0
            slider_panel.bottom = 0
            slider_panel.top = None
            
            slider_panel.content = ft.Column(
                controls=[s_bright, s_size],
                spacing=12, # 간격 약간 조정
                alignment=ft.MainAxisAlignment.CENTER
            )
            slider_panel.padding = ft.padding.only(left=20, right=20, bottom=30, top=10)
            
            mode_btn.top = None
            mode_btn.bottom = 160 # 버튼 위치 조정
            mode_btn.right = 20
            mode_btn.left = None

        else:
            # [가로 모드]
            # [변경] 슬라이더 두께를 얇게 조정 (90 -> 60)
            bar_width = 60
            track_len = h - 40
            
            s_bright = PixelSlider(
                state["brightness"], 0.1, 1.0, on_brightness_change,
                vertical=True, icon=ft.icons.BRIGHTNESS_6, label_format="{:.0%}"
            )
            s_bright.width = bar_width
            s_bright.expand = True
            s_bright.set_track_length(track_len)
            
            s_size = PixelSlider(
                state["diameter"], 50, limit_size, on_size_change,
                vertical=True, icon=ft.icons.ASPECT_RATIO, label_format="{:.0f} px"
            )
            s_size.width = bar_width
            s_size.expand = True
            s_size.set_track_length(track_len)

            # 패널 너비 조정
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

        slider_panel.update()
        page.update()

    page.on_resized = on_resize

    layout = ft.Stack(
        controls=[
            ft.Container(content=the_circle, alignment=ft.alignment.center),
            flash_overlay, 
            slider_panel,
            mode_btn
        ],
        expand=True
    )

    page.add(layout)
    on_resize(None)

if __name__ == "__main__":

    ft.app(target=main)
