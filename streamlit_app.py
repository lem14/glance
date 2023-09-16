from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import simulate_patient
import interact


st.set_page_config(page_title='Glance Dashboard',  layout='wide', page_icon="🚨")

"""
# Welcome to Glance!
alerts are binary, humans are not

ICU Floor Plan
"""

# add toggle options
col1, col2, col3, col4 = st.columns(4)

with col1:
    warn_stats_on = st.toggle("View Warnings")

with col2:
    all_stats_on = st.toggle("View All Stats")

# build top row
col1, col2, col3, col4 = st.columns(4)

with col1:
    if all_stats_on:
        st.success('BP: 120/80, SpO2: 99', icon="✅")
    else:
        st.success('',icon="✅")

with col2:
    if all_stats_on:
        st.error('BP: 120/80, SpO2: 75', icon="🚨")
    else:
        st.error(" ", icon="🚨")

with col3:
   st.success('',icon="✅")

with col4:
   st.warning("", icon="⚠️")

# build side rows
col1, col2, col3, col4 = st.columns(4)

with col1:
   st.error(" ", icon="🚨")
   st.success('',icon="✅")
   st.warning("", icon="⚠️")

with col2:
   st.empty()

with col3:
   st.empty()

with col4:
   st.error(" ", icon="🚨")
   st.success('',icon="✅")
   st.success('',icon="✅")


patient = st.selectbox('Select Bed #:', range(1,11), 1)
#patient_data = data[data[bed_num] == patient]


import matplotlib
import io
from typing import List, Optional

import markdown
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly import express as px
from plotly.subplots import make_subplots
import pyperclip
# matplotlib.use("TkAgg")
matplotlib.use("Agg")
COLOR = "black"
BACKGROUND_COLOR = "#fff"


def main():

    a=st.text_area('Type in the text_area and click copy')

    if st.button('Copy'):
        pyperclip.copy(a)
        st.success('Text copied successfully!')

    #st.title("Copy Paste in streamlit")
    #pathinput = st.text_input("Enter your Path:")
    #you can place your path instead
    Path = f'''{"Vitals"}'''
    st.code(Path, language="python")
    #st.markdown("Now you get option to copy")

    """Main function. Run this to run the app"""
    st.sidebar.title("Select Hospital Floor")
    #st.sidebar.header("Settings")
    st.markdown(
        """
# Welcome to Glance!
alerts are binary, humans are not

ICU Floor Plan
"""
    )

    select_block_container_style()
    add_resources_section()

    # My preliminary idea of an API for generating a grid
    with Grid("1 1 1", color=COLOR, background_color=BACKGROUND_COLOR) as grid:
        grid.cell(
            class_="a",
            grid_column_start=2,
            grid_column_end=3,
            grid_row_start=1,
            grid_row_end=2,
        ).markdown("# This is A Markdown Cell")
        grid.cell("b", 2, 3, 2, 3).text(interact.interactive_bubble('Bed 1'))
        grid.cell("c", 3, 4, 2, 3).plotly_chart(get_plotly_fig())
        grid.cell("d", 1, 2, 1, 3).dataframe(get_dataframe())
        grid.cell("e", 3, 4, 1, 2).markdown(
            "Try changing the **block container style** in the sidebar!"
        )
        grid.cell("f", 1, 3, 3, 4).text(
            "The cell to the right is a matplotlib svg image"
        )
        grid.cell("g", 3, 4, 3, 4).pyplot(get_matplotlib_plt())
        grid.cell("h", 2, 3, 2, 3).text(interact.interactive_bubble('Bed 2'))

    st.plotly_chart(get_plotly_subplots())


def add_resources_section():
    """Adds a resources section to the sidebar"""
    st.sidebar.header("Add_resources_section")
    st.sidebar.markdown(
        """
- [gridbyexample.com] (https://gridbyexample.com/examples/)
"""
    )


class Cell:
    """A Cell can hold text, markdown, plots etc."""

    def __init__(
        self,
        class_: str = None,
        grid_column_start: Optional[int] = None,
        grid_column_end: Optional[int] = None,
        grid_row_start: Optional[int] = None,
        grid_row_end: Optional[int] = None,
    ):
        self.class_ = class_
        self.grid_column_start = grid_column_start
        self.grid_column_end = grid_column_end
        self.grid_row_start = grid_row_start
        self.grid_row_end = grid_row_end
        self.inner_html = ""

    def _to_style(self) -> str:
        return f"""
.{self.class_} {{
    grid-column-start: {self.grid_column_start};
    grid-column-end: {self.grid_column_end};
    grid-row-start: {self.grid_row_start};
    grid-row-end: {self.grid_row_end};
}}
"""

    def text(self, text: str = ""):
        self.inner_html = text

    def markdown(self, text):
        self.inner_html = markdown.markdown(text)

    def dataframe(self, dataframe: pd.DataFrame):
        self.inner_html = dataframe.to_html()

    def plotly_chart(self, fig):
        self.inner_html = f"""
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<body>
    <p>This should have been a plotly plot.
    But since *script* tags are removed when inserting MarkDown/ HTML i cannot get it to workto work.
    But I could potentially save to svg and insert that.</p>
    <div id='divPlotly'></div>
    <script>
        var plotly_data = {fig.to_json()}
        Plotly.react('divPlotly', plotly_data.data, plotly_data.layout);
    </script>
</body>
"""

    def pyplot(self, fig=None, **kwargs):
        string_io = io.StringIO()
        #plt.savefig(string_io, format="svg", fig=(2, 2))
        svg = string_io.getvalue()[215:]
        plt.close(fig)
        self.inner_html = '<div height="200px">' + svg + "</div>"

    def _to_html(self):
        return f"""<div class="box {self.class_}">{self.inner_html}</div>"""


class Grid:
    """A (CSS) Grid"""

    def __init__(
        self,
        template_columns="1 1 1",
        gap="10px",
        background_color=COLOR,
        color=BACKGROUND_COLOR,
    ):
        self.template_columns = template_columns
        self.gap = gap
        self.background_color = background_color
        self.color = color
        self.cells: List[Cell] = []

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        st.markdown(self._get_grid_style(), unsafe_allow_html=True)
        st.markdown(self._get_cells_style(), unsafe_allow_html=True)
        st.markdown(self._get_cells_html(), unsafe_allow_html=True)

    def _get_grid_style(self):
        return f"""
<style>
    .wrapper {{
    display: grid;
    grid-template-columns: {self.template_columns};
    grid-gap: {self.gap};
    background-color: {self.background_color};
    color: {self.color};
    }}
    .box {{
    background-color: {self.color};
    color: {self.background_color};
    border-radius: 5px;
    padding: 20px;
    font-size: 150%;
    }}
    table {{
        color: {self.color}
    }}
</style>
"""

    def _get_cells_style(self):
        return (
            "<style>"
            + "\n".join([cell._to_style() for cell in self.cells])
            + "</style>"
        )

    def _get_cells_html(self):
        return (
            '<div class="wrapper">'
            + "\n".join([cell._to_html() for cell in self.cells])
            + "</div>"
        )

    def cell(
        self,
        class_: str = None,
        grid_column_start: Optional[int] = None,
        grid_column_end: Optional[int] = None,
        grid_row_start: Optional[int] = None,
        grid_row_end: Optional[int] = None,
    ):
        cell = Cell(
            class_=class_,
            grid_column_start=grid_column_start,
            grid_column_end=grid_column_end,
            grid_row_start=grid_row_start,
            grid_row_end=grid_row_end,
        )
        self.cells.append(cell)
        return cell


def select_block_container_style():
    """Add selection section for setting setting the max-width and padding
    of the main block container"""
    st.sidebar.header("Block Container Style")
    max_width_100_percent = st.sidebar.checkbox("Max-width: 100%?", False)
    if not max_width_100_percent:
        max_width = st.sidebar.slider("Select max-width in px", 100, 2000, 1200, 100)
    else:
        max_width = 1200
    dark_theme = st.sidebar.checkbox("Dark Theme?", False)
    padding_top = st.sidebar.number_input("Select padding top in rem", 0, 200, 5, 1)
    padding_right = st.sidebar.number_input("Select padding right in rem", 0, 200, 1, 1)
    padding_left = st.sidebar.number_input("Select padding left in rem", 0, 200, 1, 1)
    padding_bottom = st.sidebar.number_input(
        "Select padding bottom in rem", 0, 200, 10, 1
    )
    if dark_theme:
        global COLOR
        global BACKGROUND_COLOR
        BACKGROUND_COLOR = "rgb(17,17,17)"
        COLOR = "#fff"

    _set_block_container_style(
        max_width,
        max_width_100_percent,
        padding_top,
        padding_right,
        padding_left,
        padding_bottom,
    )


def _set_block_container_style(
    max_width: int = 1200,
    max_width_100_percent: bool = False,
    padding_top: int = 5,
    padding_right: int = 1,
    padding_left: int = 1,
    padding_bottom: int = 10,
):
    if max_width_100_percent:
        max_width_str = f"max-width: 100%;"
    else:
        max_width_str = f"max-width: {max_width}px;"
    st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        {max_width_str}
        padding-top: {padding_top}rem;
        padding-right: {padding_right}rem;
        padding-left: {padding_left}rem;
        padding-bottom: {padding_bottom}rem;
    }}
    .reportview-container .main {{
        color: {COLOR};
        background-color: {BACKGROUND_COLOR};
    }}
</style>
""",
        unsafe_allow_html=True,
    )


@st.cache_data
def get_dataframe() -> pd.DataFrame():
    """Dummy DataFrame"""
    data = [
        {"quantity": 1, "price": 2},
        {"quantity": 3, "price": 5},
        {"quantity": 4, "price": 8},
    ]
    return pd.DataFrame(data)


def get_plotly_fig():
    """Dummy Plotly Plot"""
    return px.line(data_frame=get_dataframe(), x="quantity", y="price")


def get_matplotlib_plt():
    get_dataframe().plot(kind="line", x="quantity", y="price", figsize=(5, 3))


def get_plotly_subplots():
    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=("Plot 1", "Plot 2", "Plot 3", "Table 4"),
        specs=[
            [{"type": "scatter"}, {"type": "scatter"}],
            [{"type": "scatter"}, {"type": "table"}],
        ],
    )

    fig.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 5, 6]), row=1, col=1)

    fig.add_trace(go.Scatter(x=[20, 30, 40], y=[50, 60, 70]), row=1, col=2)

    fig.add_trace(go.Scatter(x=[300, 400, 500], y=[600, 700, 800]), row=2, col=1)

    fig.add_table(
        header=dict(values=["A Scores", "B Scores"]),
        cells=dict(values=[[100, 90, 80, 90], [95, 85, 75, 95]]),
        row=2,
        col=2,
    )

    if COLOR == "black":
        template="plotly"
    else:
        template ="plotly_dark"
    fig.update_layout(
        height=500,
        width=700,
        title_text="Plotly Multiple Subplots with Titles",
        template=template,
    )
    return fig

main()

