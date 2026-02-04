import flet as ft
import traceback # 에러 위치 추적용

# =============================================================================
# Google Pixel Style Slider (안전장치 추가됨)
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
        
        # 기본값 안전장치
        self.track_length = 200.0 
        
        # 디자인 요소
        self.bgcolor = ft.colors.with_opacity(0.1, ft.colors.GREY_900)
        self.border_radius = 16
        self.clip_behavior = ft.ClipBehavior.HARD_EDGE
        self.padding = 0
        
        # 채움 바
        self.fill_bar = ft.Container(
            bgcolor=ft.colors.with_opacity(0.25, ft.colors.WHITE),
            border_radius=16,
            # 애니메이션이 초기 로딩 부하를 줄 수 있어 잠시 제거하거나 짧게 설정
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
        if length < 50: length = 100 # 최소 길이 보장
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
        try:
            self.label_view.value = self.label_format.format(self.value)
            if self.max_v == self.min_v: ratio = 0
            else: ratio = (self.value - self.min_v) / (self.max_v - self.min_v)
            ratio = max(0.0, min(1.0, ratio))
            
            if self.vertical: self.fill_bar.height = self.track_length * ratio
            else: self.fill_bar.width = self.track_length * ratio
        except:
            pass # 렌더링 중 에러 무시

    def update_visuals(self, val=None):
        if val is not None: self.value = val
        self._apply_visuals_internal()
        if self.fill_bar.page:
            self.fill_bar.update()
            self.label_view.update()


# =============================================================================
# Main App (Safe Mode)
# =============================================================================
def main(page: ft.Page):
    # [1] 에러 캐치를 위한 Try-Except 전체 래핑
    try:
        # 페이지 기본 설정
        page.title = "FlatPanel Safe"
        page.theme_mode = ft.ThemeMode.DARK
        page.bgcolor = "#000000"
        page.padding = 0
        page.spacing = 0
        # 스크롤 끄지 않음 (오버플로우 시 잘리는 대신 스크롤 되도록 하여 크래시 방지)
        # page.scroll = ft.ScrollMode.OFF 

        state = {
            "is_light_mode": False,
            "diameter": 300.0,
            "brightness": 1.0,
        }

        # ---------------------------------------------------------
        # UI Components
        # ---------------------------------------------------------
        
        flash_overlay = ft.Container(
            expand=True,
            bgcolor=ft.colors.WHITE,
            opacity=0,
            animate_opacity=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            visible=True,
            on_click=lambda _: None 
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

        # ---------------------------------------------------------
        # 로직 함수
        # ---------------------------------------------------------
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
            # UI 업데이트 로직 안전하게 처리
            if state["is_light_mode"]:
                flash_overlay.opacity = 1
                ctrl_container.opacity = 0 # 슬라이더 패널 숨김
                mode_btn.icon = "flashlight_off"
                mode_btn.icon_color = ft.colors.BLACK54
                mode_btn.bgcolor = ft.colors.with_opacity(0.1, ft.colors.BLACK)
            else:
                flash_overlay.opacity = 0
                ctrl_container.opacity = 1 # 슬라이더 패널 보임
                mode_btn.icon = "flashlight_on"
                mode_btn.icon_color = ft.colors.with_opacity(0.5, ft.colors.WHITE)
                mode_btn.bgcolor = ft.colors.with_opacity(0.1, ft.colors.WHITE)
            
            page.update()

        # ---------------------------------------------------------
        # Layout Strategy (on_resize 제거 -> SafeArea & Responsive 사용)
        # ---------------------------------------------------------
        
        # 버튼 생성
        mode_btn = ft.IconButton(
            icon="flashlight_on",
            icon_color=ft.colors.with_opacity(0.5, ft.colors.WHITE),
            bgcolor=ft.colors.with_opacity(0.1, ft.colors.WHITE),
            icon_size=24,
            on_click=toggle_mode,
            style=ft.ButtonStyle(shape=ft.CircleBorder(), padding=15)
        )

        # 슬라이더 생성 (고정 길이 사용 - 안전성 확보)
        # 탭 S10 Ultra는 화면이 매우 크므로 길이를 넉넉히 줌
        slider_len = 400.0 
        
        s_bright = PixelSlider(
            state["brightness"], 0.1, 1.0, on_brightness_change,
            vertical=True, icon="brightness_6", label_format="{:.0%}"
        )
        s_bright.set_track_length(slider_len)
        s_bright.width = 60
        s_bright.expand = True

        s_size = PixelSlider(
            state["diameter"], 50, 1000, on_size_change,
            vertical=True, icon="aspect_ratio", label_format="{:.0f} px"
        )
        s_size.set_track_length(slider_len)
        s_size.width = 60
        s_size.expand = True

        # 컨트롤 패널 (우측 고정)
        ctrl_panel = ft.Container(
            content=ft.Row(
                controls=[s_bright, s_size],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            width=180,
            padding=ft.padding.symmetric(vertical=20, horizontal=10),
            animate_opacity=300,
        )
        
        # 이것이 slider_panel 역할을 합니다.
        ctrl_container = ft.Container(
            content=ctrl_panel,
            alignment=ft.alignment.center_right, # 우측 정렬
            opacity=1,
            animate_opacity=300
        )

        # 버튼 컨테이너 (좌측 상단)
        btn_container = ft.Container(
            content=mode_btn,
            alignment=ft.alignment.top_left,
            padding=20
        )

        # 메인 스택 (SafeArea로 감싸서 시스템 UI 침범 방지)
        main_stack = ft.Stack(
            controls=[
                # 1. 중앙 원 (화면 중앙 정렬)
                ft.Container(content=the_circle, alignment=ft.alignment.center),
                
                # 2. 화이트 플래시 (전체 화면)
                flash_overlay,
                
                # 3. 컨트롤 패널 (우측)
                ctrl_container,

                # 4. 버튼 (좌측 상단)
                btn_container
            ],
            expand=True
        )

        # SafeArea를 쓰면 노치나 네비게이션 바 때문에 검은 화면이 되는 문제를 막아줍니다.
        page.add(ft.SafeArea(main_stack, expand=True))

    except Exception as e:
        # [2] 에러 발생 시 화면에 출력 (매우 중요)
        error_msg = traceback.format_exc()
        page.clean()
        page.bgcolor = ft.colors.RED_900
        page.scroll = ft.ScrollMode.ALWAYS
        page.add(
            ft.Text("CRITICAL ERROR OCCURRED:", size=30, color=ft.colors.WHITE, weight="bold"),
            ft.Text(str(e), size=20, color=ft.colors.YELLOW),
            ft.Divider(color=ft.colors.WHITE),
            ft.Text(error_msg, size=15, color=ft.colors.WHITE, font_family="monospace")
        )
        page.update()

if __name__ == "__main__":
    ft.app(target=main)
