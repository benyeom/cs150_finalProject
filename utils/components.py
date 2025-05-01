def year_slider():
    from dash import dcc
    return dcc.Slider(
        id="year-slider",
        min=2010,
        max=2022,
        step=1,
        value=2010,
        marks={year: {"label": str(year), "style": {"fontSize": "20px"}} for year in range(2010, 2023)},
        tooltip={"placement": "bottom", "always_visible": True}
    )

def toggle_buttons():
    from dash import dcc
    return dcc.RadioItems(
        id="view-toggle",
        options=[
            {"label": "Number", "value": "number"},
            {"label": "Percentage", "value": "percentage"}
        ],
        value="number",
        labelStyle={"display": "inline-block", "marginRight": "15px"},
        style={"marginBottom": "20px", "fontWeight": "bold"}
    )

def heatmap_section():
    from dash import html, dcc
    from utils.figures import create_heatmap
    return html.Div([
        html.H2("State-Year Heatmap: Depression vs. Income", style={"textAlign": "center"}),
        dcc.Graph(figure=create_heatmap())
    ])

def spending_bar_section():
    from dash import html, dcc
    from utils.figures import create_cost_bar_chart

    return html.Div([
        html.H2("Annual Mental Health Treatment Spending", style={"textAlign": "center", "marginTop": "40px"}),
        dcc.Graph(figure=create_cost_bar_chart())
    ])

def choropleth_section():
    from dash import html, dcc
    from utils.figures import create_choropleth_map

    return html.Div([
        html.H2("Depression and Physical Inactivity by State", style={"textAlign": "center", "marginTop": "50px"}),
        dcc.Graph(figure=create_choropleth_map())
    ])

def healthcare_cost_section():
    from dash import html, dcc
    from utils.figures import create_healthcare_cost_chart

    return html.Div([
        html.H2("Cost Comparison: Pharmacy, Professional Services, and Exercise", style={"textAlign": "center", "marginTop": "50px"}),
        dcc.Graph(figure=create_healthcare_cost_chart())
    ])

def separate_scatter_row():
    from dash import html, dcc
    from utils.figures import create_separate_regression_scatterplots

    fig1, fig2, fig3 = create_separate_regression_scatterplots()

    return html.Div([
        html.H2("Correlation Scatterplots (2015–2022)", style={"textAlign": "center", "marginTop": "50px"}),
        html.Div([
            html.Div(dcc.Graph(figure=fig1), style={"width": "33%", "display": "inline-block", "padding": "0 10px"}),
            html.Div(dcc.Graph(figure=fig2), style={"width": "33%", "display": "inline-block", "padding": "0 10px"}),
            html.Div(dcc.Graph(figure=fig3), style={"width": "33%", "display": "inline-block", "padding": "0 10px"})
        ], style={"display": "flex", "justifyContent": "space-around"})
    ])



