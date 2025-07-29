Container
Container allows to decorate a control with background color and border and position it with padding, margin and alignment.

Examples
Live example

Clickable container

python/controls/layout/container/clickable-container.py
import flet as ft


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = "Containers - clickable and not"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.add(
        ft.Row(
            [
                ft.Container(
                    content=ft.Text("Non clickable"),
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.Colors.AMBER,
                    width=150,
                    height=150,
                    border_radius=10,
                ),
                ft.Container(
                    content=ft.Text("Clickable without Ink"),
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.Colors.GREEN_200,
                    width=150,
                    height=150,
                    border_radius=10,
                    on_click=lambda e: print("Clickable without Ink clicked!"),
                ),
                ft.Container(
                    content=ft.Text("Clickable with Ink"),
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.Colors.CYAN_200,
                    width=150,
                    height=150,
                    border_radius=10,
                    ink=True,
                    on_click=lambda e: print("Clickable with Ink clicked!"),
                ),
                ft.Container(
                    content=ft.Text("Clickable transparent with Ink"),
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    width=150,
                    height=150,
                    border_radius=10,
                    ink=True,
                    on_click=lambda e: print("Clickable transparent with Ink clicked!"),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )


ft.app(main)

View on GitHub
Properties

alignment
Align the child control within the container.

Value is of type Alignment.

animate
Enables container "implicit" animation that gradually changes its values over a period of time.

Value is of type AnimationValue.

bgcolor
Defines the background color of the container.

blend_mode
The blend mode applied to the color or gradient background of the container.

Value is of type BlendMode and defaults to BlendMode.MODULATE.

blur
Applies Gaussian blur effect under the container.

The value of this property could be one of the following:

a number - specifies the same value for horizontal and vertical sigmas, e.g. 10.
a tuple - specifies separate values for horizontal and vertical sigmas, e.g. (10, 1).
an instance of Blur
For example:

python/controls/layout/container/container-blur.py
import flet as ft


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    i = 1

    img_container = ft.Container(
        image=ft.DecorationImage(src="https://picsum.photos/250/250"),
        width=250,
        height=250,
    )

    def change_img(e):
        nonlocal i
        print(f"button clicked {i}")
        img_container.image = ft.DecorationImage(
            src=f"https://picsum.photos/250/250?random={i}"
        )
        i += 1
        page.update()

    page.add(
        ft.Stack(
            [
                img_container,
                ft.Container(
                    width=100,
                    height=100,
                    blur=10,
                    bgcolor="#22CCCC00",
                ),
                ft.Container(
                    width=100,
                    height=100,
                    left=20,
                    top=120,
                    blur=(0, 10),
                ),
                ft.Container(
                    top=50,
                    right=10,
                    blur=ft.Blur(10, 0, ft.BlurTileMode.MIRROR),
                    width=100,
                    height=100,
                    bgcolor="#44CCCCCC",
                    border_radius=10,
                    border=ft.border.all(2, ft.Colors.BLACK),
                ),
                ft.ElevatedButton(
                    text="Change Background",
                    bottom=5,
                    right=5,
                    style=ft.ButtonStyle(text_style=ft.TextStyle(size=8)),
                    on_click=change_img,
                ),
            ]
        )
    )


ft.app(main)

View on GitHub

border
A border to draw above the background color.

Value is of type Border.

border_radius
If specified, the corners of the container are rounded by this radius.

Value is of type BorderRadius.

clip_behavior
The content will be clipped (or not) according to this option.

Value is of type ClipBehavior and defaults to ClipBehavior.ANTI_ALIAS if border_radius is not None; otherwise ClipBehavior.NONE.

color_filter
Applies a color filter to the container.

Value is of type ColorFilter.

content
A child Control contained by the container.

dark_theme
Allows setting a nested theme to be used when in dark theme mode for all controls inside the container and down the tree.

Value is of type Theme.

foreground_decoration
The foreground decoration.

Value is of type BoxDecoration.

gradient
Defines the gradient background of the container.

Value is of type Gradient.

ignore_interactions
Whether to ignore all interactions with this container and its descendants.

Defaults to False.

image
An image to paint above the bgcolor or gradient. If shape=BoxShape.CIRCLE then this image is clipped to the circle's boundary; if border_radius is not Nonethen the image is clipped to the given radii.

Value is of type DecorationImage.

ink
True to produce ink ripples effect when user clicks the container.

Defaults to False.

ink_color
The splash color of the ink response.

margin
Empty space to surround the decoration and child control.

Value is of type Margin class or a number.

padding
Empty space to inscribe inside a container decoration (background, border). The child control is placed inside this padding.

Value is of type Padding or a number.

rtl
True to set text direction to right-to-left.

Defaults to False.

shadow
Shadows cast by the container.

Value is of type BoxShadow or a List[BoxShadow].

shape
Sets the shape of the container.

Value is of type BoxShape and defaults to BoxShape.RECTANGLE.

theme_mode
Setting theme_mode "resets" parent theme and creates a new, unique scheme for all controls inside the container. Otherwise the styles defined in container's theme property override corresponding styles from the parent, inherited theme.

Value is of type ThemeMode and defaults to ThemeMode.SYSTEM.

theme
Allows setting a nested theme for all controls inside the container and down the tree.

Value is of type Theme.

Usage example

python/controls/layout/container/nested-themes-switch.py
import flet as ft


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK

    def change_theme_mode(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            sw.thumb_icon = ft.Icons.LIGHT_MODE
        else:
            sw.thumb_icon = ft.Icons.DARK_MODE
            page.theme_mode = ft.ThemeMode.DARK
        page.update()

    # Yellow page theme with SYSTEM (default) mode
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.YELLOW,
    )
    sw = ft.Switch(thumb_icon=ft.Icons.DARK_MODE, on_change=change_theme_mode)
    page.add(
        # Page theme
        ft.Row(
            [
                ft.Container(
                    content=ft.ElevatedButton("Page theme button"),
                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                    padding=20,
                    width=300,
                ),
                ft.Container(
                    content=sw,
                    padding=ft.padding.only(bottom=50),
                    alignment=ft.alignment.top_right,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        # Inherited theme with primary color overridden
        ft.Container(
            theme=ft.Theme(color_scheme=ft.ColorScheme(primary=ft.Colors.PINK)),
            content=ft.ElevatedButton("Inherited theme button"),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            padding=20,
            width=300,
        ),
        # Unique always DARK theme
        ft.Container(
            theme=ft.Theme(color_scheme_seed=ft.Colors.INDIGO),
            theme_mode=ft.ThemeMode.DARK,
            content=ft.ElevatedButton("Unique theme button"),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            padding=20,
            width=300,
        ),
    )


ft.app(main)

View on GitHub

url
The URL to open when the container is clicked. If provided, on_click event is fired after that.

url_target
Where to open URL in the web mode.

Value is of type UrlTarget and defaults to UrlTarget.BLANK.

Events
on_click
Fires when a user clicks the container. Will not be fired on long press.

on_hover
Fires when a mouse pointer enters or exists the container area. data property of event object contains true (string) when cursor enters and false when it exits.

A simple example of a container changing its background color on mouse hover:

python/controls/layout/container/simple-hover.py
import flet as ft


def main(page: ft.Page):
    def on_hover(e):
        e.control.bgcolor = "blue" if e.data == "true" else "red"
        e.control.update()

    page.add(
        ft.Container(width=100, height=100, bgcolor="red", ink=False, on_hover=on_hover)
    )


ft.app(main)

View on GitHub

on_long_press
Fires when the container is long-pressed.

on_tap_down
Fires when a user clicks the container with or without a long press.

Event handler argument is of type ContainerTapEvent.

info
If ink is True, e will be plain ControlEvent with empty data instead of ContainerTapEvent.

A simple usage example:

python/controls/layout/container/container-click-events.py
import flet as ft


def main(page: ft.Page):

    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    lp_counter = 0
    cl_counter = 0
    td_counter = 0

    def on_click(e):
        nonlocal cl_counter
        cl_counter += 1
        t1.spans[-1] = ft.TextSpan(
            f"  {cl_counter}  ",
            style=ft.TextStyle(size=16, bgcolor=ft.Colors.TEAL_300),
        )

        page.update()

    def on_long_press(e):
        nonlocal lp_counter
        lp_counter += 1
        t3.spans[-1] = ft.TextSpan(
            f"  {lp_counter}  ",
            style=ft.TextStyle(size=16, bgcolor=ft.Colors.TEAL_300),
        )
        page.update()

    def on_tap_down(e: ft.ContainerTapEvent):
        nonlocal td_counter
        td_counter += 1
        t2.spans[-1] = ft.TextSpan(
            f"  {td_counter}  ",
            style=ft.TextStyle(size=16, bgcolor=ft.Colors.TEAL_300),
        )
        page.update()

    c = ft.Container(
        bgcolor=ft.Colors.PINK_900,
        content=ft.Text(
            "Press Me!",
            text_align=ft.TextAlign.CENTER,
            style=ft.TextStyle(
                size=30,
                # weight=ft.FontWeight.BOLD,
                foreground=ft.Paint(
                    color=ft.Colors.BLUE_700,
                    stroke_cap=ft.StrokeCap.BUTT,
                    stroke_width=2,
                    stroke_join=ft.StrokeJoin.BEVEL,
                    style=ft.PaintingStyle.STROKE,
                ),
            ),
            theme_style=ft.TextThemeStyle.DISPLAY_MEDIUM,
        ),
        alignment=ft.alignment.center,
        padding=ft.padding.all(10),
        height=150,
        width=150,
        on_click=on_click,
        on_long_press=on_long_press,
        on_tap_down=on_tap_down,
    )
    t1 = ft.Text(
        spans=[
            ft.TextSpan(
                "On Click", style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
            ),
            ft.TextSpan(" counter:  ", style=ft.TextStyle(size=16, italic=True)),
            ft.TextSpan(
                f"  {cl_counter}  ",
                style=ft.TextStyle(size=16, bgcolor=ft.Colors.TEAL_300),
            ),
        ]
    )
    t2 = ft.Text(
        spans=[
            ft.TextSpan(
                "Tap Down", style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
            ),
            ft.TextSpan(" counter:  ", style=ft.TextStyle(size=16, italic=True)),
            ft.TextSpan(
                f"  {td_counter}  ",
                style=ft.TextStyle(size=16, bgcolor=ft.Colors.TEAL_300),
            ),
        ]
    )
    t3 = ft.Text(
        spans=[
            ft.TextSpan(
                "Long Press", style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
            ),
            ft.TextSpan(" counter:  ", style=ft.TextStyle(size=16, italic=True)),
            ft.TextSpan(
                f"  {lp_counter}  ",
                style=ft.TextStyle(size=16, bgcolor=ft.Colors.TEAL_300),
            ),
        ]
    )

    page.add(c, t1, t3, t2)


ft.app(main)

View on GitHub
