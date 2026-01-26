from typing import Any
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st


def create_figure(a: float, b: float, c: float, d: float, 
                  vector: np.ndarray, grid_range: int = 5, grid_step: int = 1
                 ) -> go.Figure:
    """
    Создаёт фигуру с двумя подграфиками (1x2):

    1) Исходное пространство с заданным вектором v.
    2) Деформированное пространство с образом вектора v'.

    Параметры:
        a, b, c, d (float): Элементы матрицы A = [[a, b], [c, d]].
        vector (np.ndarray): Исходный вектор (длина 2).
        grid_range (int): Диапазон значений координатной сетки.
        grid_step (int): Шаг между линиями сетки.

    Возвращает:
        go.Figure: Фигура с двумя подграфиками.
    """
    xs: np.ndarray = np.arange(-grid_range, grid_range + grid_step, grid_step)
    ys: np.ndarray = np.arange(-grid_range, grid_range + grid_step, grid_step)
    matrix: np.ndarray = np.array([[a, b], [c, d]])

    fig: go.Figure = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=["Исходное пространство", "Деформированное пространство"],
        horizontal_spacing=0.02
    )

    def add_vector_annotation(x: float, y: float, xref: str, yref: str, 
                              color: str, label: str,
                              row: int = 1, col: int = 1, 
                              text_xshift: int = 10, text_yshift: int = -10) -> None:
        """Добавляет стрелку и подпись в указанном подграфике."""
        fig.add_annotation(
            x=x, y=y,
            ax=0, ay=0,
            xref=xref, yref=yref,
            axref=xref, ayref=yref,
            showarrow=True,
            arrowhead=3,
            arrowcolor=color,
            arrowsize=1,
            arrowwidth=2,
            text="",
            row=row,
            col=col
        )
        fig.add_annotation(
            x=x, y=y,
            xref=xref, yref=yref,
            text=label,
            showarrow=False,
            xshift=text_xshift,
            yshift=text_yshift,
            row=row,
            col=col
        )

    # Исходное пространство
    for x_val in xs:
        fig.add_trace(
            go.Scatter(
                x=[x_val, x_val],
                y=[-grid_range, grid_range],
                mode='lines',
                line=dict(color='lightgray', dash='dash'),
                showlegend=False
            ),
            row=1, col=1
        )
    for y_val in ys:
        fig.add_trace(
            go.Scatter(
                x=[-grid_range, grid_range],
                y=[y_val, y_val],
                mode='lines',
                line=dict(color='lightgray', dash='dash'),
                showlegend=False
            ),
            row=1, col=1
        )
    add_vector_annotation(1, 0, "x", "y", "red", "i", row=1, col=1)
    add_vector_annotation(0, 1, "x", "y", "green", "j", row=1, col=1)
    add_vector_annotation(vector[0], vector[1], "x", "y", "blue", "v", row=1, col=1)

    # Деформированное пространство
    for x_val in xs:
        line_y = np.linspace(-grid_range, grid_range, 100)
        original_points = np.array([[x_val, y_val] for y_val in line_y])
        transformed = original_points @ matrix.T
        fig.add_trace(
            go.Scatter(
                x=transformed[:, 0],
                y=transformed[:, 1],
                mode='lines',
                line=dict(color='lightgray', dash='dash'),
                showlegend=False
            ),
            row=1, col=2
        )
    for y_val in ys:
        line_x = np.linspace(-grid_range, grid_range, 100)
        original_points = np.array([[x_val, y_val] for x_val in line_x])
        transformed = original_points @ matrix.T
        fig.add_trace(
            go.Scatter(
                x=transformed[:, 0],
                y=transformed[:, 1],
                mode='lines',
                line=dict(color='lightgray', dash='dash'),
                showlegend=False
            ),
            row=1, col=2
        )

    v_prime: np.ndarray = matrix @ vector
    add_vector_annotation(v_prime[0], v_prime[1], "x2", "y2", "blue", "v'", row=1, col=2)
    i_prime: np.ndarray = matrix @ np.array([1, 0])
    j_prime: np.ndarray = matrix @ np.array([0, 1])
    add_vector_annotation(i_prime[0], i_prime[1], "x2", "y2", "red", "i'", row=1, col=2)
    add_vector_annotation(j_prime[0], j_prime[1], "x2", "y2", "green", "j'", row=1, col=2)

    fig.update_layout(
        width=1000,
        height=500,
        margin=dict(l=0, r=0, t=50, b=50),
        xaxis=dict(
            domain=[0, 0.45],
            range=[-grid_range, grid_range],
            scaleanchor="y",
            scaleratio=1,
            constrain="domain"
        ),
        yaxis=dict(
            domain=[0, 1],
            range=[-grid_range, grid_range],
            scaleanchor="x",
            scaleratio=1,
            constrain="domain"
        ),
        xaxis2=dict(
            domain=[0.55, 1],
            range=[-grid_range, grid_range],
            scaleanchor="y2",
            scaleratio=1,
            constrain="domain"
        ),
        yaxis2=dict(
            domain=[0, 1],
            range=[-grid_range, grid_range],
            scaleanchor="x2",
            scaleratio=1,
            constrain="domain"
        )
    )

    return fig

def main() -> None:
    """Главная функция приложения Streamlit."""
    st.title("Интерактивная визуализация линейной деформации")

    st.subheader("Коэффициенты матрицы линейного отображения")
    col1, col2 = st.columns(2)
    a: float = col1.number_input("a:", value=1.0, step=0.1)
    b: float = col2.number_input("b:", value=0.0, step=0.1)
    col3, col4 = st.columns(2)
    c: float = col3.number_input("c:", value=0.0, step=0.1)
    d: float = col4.number_input("d:", value=1.0, step=0.1)

    st.subheader("Координаты исходного вектора")
    v1: float = st.number_input("v₁:", value=2.0, step=0.1)
    v2: float = st.number_input("v₂:", value=1.0, step=0.1)
    vector: np.ndarray = np.array([v1, v2])

    fig: go.Figure = create_figure(a, b, c, d, vector)
    st.plotly_chart(fig, use_container_width=True)

if __name__ == '__main__':
    main()
    
