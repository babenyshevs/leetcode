import pathlib

import matplotlib.pyplot as plt
import matplotlib as mpl

from matplotlib import font_manager

DIRNAME = pathlib.Path(__file__).parent


def load_mpl_style_file() -> None:
    """Load and apply the custom 'nova.mplstyle' file to configure Matplotlib plots globally."""
    mplstyle_location = DIRNAME / "nova.mplstyle"
    assert mplstyle_location.exists(), f"Could not locate nova.mplstyle in {DIRNAME}"
    plt.style.use(mplstyle_location)


def add_organica_font() -> None:
    """Add Organica-Regular font to Matplotlib configuration."""
    font_path = DIRNAME / "Organica-Regular.ttf"
    assert font_path.exists(), f"Could not locate Organica-Regular.ttf in {DIRNAME}"
    font_manager.fontManager.addfont(str(font_path))
    plt.rcParams["font.family"] = "Organica"


def set_mpl_style(figsize: tuple[float, float] = (10, 6), grid_axis='y', axes_grid=True, savefig_dpi: int = 100) -> None:
    """Set custom Matplotlib style by loading the NOVA style file and Organica font.

    This function configures the global Matplotlib plotting style by:
    1. Loading the custom NOVA style file
    2. Adding the Organica font
    3. Setting figure size and grid parameters

    Args:
        figsize (tuple[float, float], optional): Width and height of the figure in inches.
            Defaults to (10, 6).
        grid_axis (str, optional): Which axis the grid should be drawn on.
            Valid values are {'both', 'x', 'y'}. Defaults to 'y'.
        axes_grid (bool, optional): Whether to show grid lines on the plot.
            Defaults to True.

    Returns:
        None

    DANIELS PREFFERED STYLE:
        set_mpl_style(figsize=(10, 8), grid_axis='y', axes_grid=True)
    """
    load_mpl_style_file()
    add_organica_font()
    mpl.rcParams["figure.figsize"] = figsize
    mpl.rcParams["axes.grid.axis"] = grid_axis
    mpl.rcParams["axes.grid"] = axes_grid
    mpl.rcParams["savefig.dpi"] = savefig_dpi
