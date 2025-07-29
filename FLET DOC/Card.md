Card
A material design card: a panel with slightly rounded corners and an elevation shadow.

Examples
Live example

python/controls/layout/card/card-with-buttons.py
import flet as ft


def main(page: ft.Page):
    page.title = "Card Example"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.add(
        ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.ALBUM),
                            title=ft.Text("The Enchanted Nightingale"),
                            subtitle=ft.Text(
                                "Music by Julie Gable. Lyrics by Sidney Stein."
                            ),
                            bgcolor=ft.Colors.GREY_400,
                        ),
                        ft.Row(
                            [ft.TextButton("Buy tickets"), ft.TextButton("Listen")],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ]
                ),
                width=400,
                padding=10,
            ),
            shadow_color=ft.Colors.ON_SURFACE_VARIANT,
        )
    )


ft.app(main)

View on GitHub

Properties
clip_behavior
The content will be clipped (or not) according to this option.

Value is of type ClipBehavior and defaults to ClipBehavior.NONE.

color
The card's background color.

content
The Control that should be displayed inside the card.

This control can only have one child. To lay out multiple children, let this control's child be a control such as Row, Column, or Stack, which have a children property, and then provide the children to that control.

elevation
Controls the size of the shadow below the card. Default value is 1.0.

is_semantic_container
Set to True (default) if this card represents a single semantic container, or to False if it instead represents a collection of individual semantic nodes (different types of content).

margin
The empty space that surrounds the card.

Value can be one of the following types: int, float, or Margin.

shadow_color
The color to paint the shadow below the card.

shape
The shape of the card.

Value is of type OutlinedBorder and defaults to RoundedRectangleBorder(radius=4.0).

show_border_on_foreground
Whether the shape of the border should be painted in front of the content or behind.

Defaults to True.

surface_tint_color
The color used as an overlay on color to indicate elevation.

If this is None, no overlay will be applied. Otherwise this color will be composited on top of color with an opacity related to elevation and used to paint the background of the card.

Defaults to None.

variant
Defines the card variant to be used.

Value is of type CardVariant and defaults to CardVariant.ELEVATED.