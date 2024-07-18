from typing import Any

import rio


def colors_equal(color1: rio.Color, color2: rio.Color) -> bool:
    """
    Returns `True` if the two colors are equal and `False` otherwise. Since
    color values are stored as floats, this function applies a small fudge
    factor to account for floating point differences.
    """
    epsilon = 1e-6

    return (
        abs(color1.red - color2.red) < epsilon
        and abs(color1.green - color2.green) < epsilon
        and abs(color1.blue - color2.blue) < epsilon
        and abs(color1.opacity - color2.opacity) < epsilon
    )


def get_minimum_theme_kwargs(theme: rio.Theme) -> dict[str, Any]:
    """
    Given a theme, returns a dictionary with the minimum set of keyword
    arguments required to recreate it.
    """
    # This is more complex than it might seem at first, because many colors are
    # derived from other colors. For example, the neutral color is derived from
    # the primary one.
    result: dict[str, Any] = {}

    # Light / dark mode can impact some colors. Make sure to get that value
    # first.
    if not theme.is_light_theme:
        result["light"] = False

    # Some colors don't depend on anything else
    reference_theme = rio.Theme.from_colors(**result)

    if not colors_equal(theme.primary_color, reference_theme.primary_color):
        result["primary_color"] = theme.primary_color

    if not colors_equal(theme.secondary_color, reference_theme.secondary_color):
        result["secondary_color"] = theme.secondary_color

    if not colors_equal(theme.disabled_color, reference_theme.disabled_color):
        result["disabled_color"] = theme.disabled_color

    if not colors_equal(theme.success_color, reference_theme.success_color):
        result["success_color"] = theme.success_color

    if not colors_equal(theme.warning_color, reference_theme.warning_color):
        result["warning_color"] = theme.warning_color

    if not colors_equal(theme.danger_color, reference_theme.danger_color):
        result["danger_color"] = theme.danger_color

    if not colors_equal(theme.hud_color, reference_theme.hud_color):
        result["hud_color"] = theme.hud_color

    # These depend on the previously defined ones
    reference_theme = rio.Theme.from_colors(**result)

    if not colors_equal(
        theme.background_color, reference_theme.background_color
    ):
        result["background_color"] = theme.background_color

    if not colors_equal(theme.neutral_color, reference_theme.neutral_color):
        result["neutral_color"] = theme.neutral_color

    # Header fill
    #
    # This is nontrivial, because there are many kinds of fill, and some of them
    # can be hard to serialize. Only support solid colors for now.
    heading_color = theme.heading1_style.fill
    reference_heading_color = reference_theme.heading1_style.fill

    assert isinstance(heading_color, rio.Color), heading_color
    assert isinstance(
        reference_heading_color, rio.Color
    ), reference_heading_color

    if isinstance(heading_color, rio.Color) and not colors_equal(
        heading_color, reference_heading_color
    ):
        result["heading_fill"] = heading_color

    # Corner radii
    if theme.corner_radius_large != reference_theme.corner_radius_large:
        result["corner_radius_large"] = theme.corner_radius_large

    if theme.corner_radius_medium != reference_theme.corner_radius_medium:
        result["corner_radius_medium"] = theme.corner_radius_medium

    if theme.corner_radius_small != reference_theme.corner_radius_small:
        result["corner_radius_small"] = theme.corner_radius_small

    return result


async def update_and_apply_theme(
    session: rio.Session,
    theme_replacements: dict[str, Any],
) -> None:
    """
    Overrides the session's theme with the given one, and makes sure to update
    all components so they use the new theme.
    """

    # Determine the kwargs to use for the theme
    theme_kwargs = get_minimum_theme_kwargs(session.theme)
    theme_kwargs.update(theme_replacements)

    # Build the new theme
    new_theme = rio.Theme.from_colors(**theme_kwargs)

    # Apply it
    await session._apply_theme(new_theme)

    # The application itself isn't enough, because some components will have
    # read theme values and used them to set e.g. their corner radii. Dirty
    # every component to force a full rebuild.
    for component in session._weak_components_by_id.values():
        session._register_dirty_component(
            component,
            include_children_recursively=False,
        )

    # Refresh
    await session._refresh()


