from dash import Dash, html, dcc, Output, Input
import pandas as pd
import utils.components as components
import utils.figures as figures
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.MORPH],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1.0"}]
)
app.title = "Final Project"
server = app.server

# Load datasets
med_df = pd.read_csv("assets/(1) Medication usage_(sertraline) prescriptions 2010-2022.csv")
therapy_df = pd.read_csv("assets/(1) Therapy_counseling usage 2010-2022.csv")
pop_df = pd.read_csv("assets/(1) Global population 2010-2022.csv")

# Clean and merge
med_df.columns = ["Year", "Medication"]
therapy_df.columns = ["Year", "Therapy"]
pop_df.columns = ["Year", "Population"]

med_df["Year"] = med_df["Year"].astype(int)
therapy_df["Year"] = therapy_df["Year"].astype(int)
pop_df["Year"] = pop_df["Year"].astype(int)
pop_df["Population"] = pop_df["Population"].replace({",": ""}, regex=True).astype(float) / 1_000_000

merged_df = pd.merge(med_df, therapy_df, on="Year")
merged_df = pd.merge(merged_df, pop_df, on="Year")

# Compute percentages
merged_df["Medication_Percentage"] = (merged_df["Medication"] / merged_df["Population"]) * 100
merged_df["Therapy_Percentage"] = (merged_df["Therapy"] / merged_df["Population"]) * 100

# Layout
app.layout = html.Div([
    html.Div([
        html.H1("Depression In Context", style={
            "fontSize": "32px",
            "margin": "0",
            "paddingTop": "10px",
            "textAlign": "center",
            "fontWeight": "bold"
        }),
        html.H3("Ben Yeom", style={
            "fontSize": "18px",
            "margin": "0",
            "textAlign": "center",
            "fontWeight": "normal"
        }),
        html.H4("CS-150 Data Visualization", style={
            "fontSize": "16px",
            "marginBottom": "10px",
            "textAlign": "center",
            "fontWeight": "normal"
        })
    ], style={
        "backgroundColor": "#f0f0f0",
        "width": "100%",
        "borderBottom": "1px solid #ccc"
    }),

    html.Div([
        components.toggle_buttons(),
        html.Div([
            dcc.Graph(id="main-graph", figure=figures.create_bar_chart(merged_df, 2010)),
            html.Div(components.year_slider(), id="slider-container")
        ])
    ], style={
        "width": "70%",
        "margin": "auto",
        "marginTop": "30px",  # added top space
        "marginBottom": "50px"
    }),

    html.Hr(),

    components.heatmap_section(),

    components.spending_bar_section(),

    components.choropleth_section(),

    components.healthcare_cost_section(),

    components.separate_scatter_row()


])


# Callback
@app.callback(
    Output("main-graph", "figure"),
    Output("slider-container", "style"),
    Input("view-toggle", "value"),
    Input("year-slider", "value")
)
def update_graph(view_mode, selected_year):
    if view_mode == "number":
        return figures.create_bar_chart(merged_df, selected_year), {"display": "block"}
    else:
        return figures.create_percentage_line_chart(merged_df), {"display": "none"}

if __name__ == "__main__":
    app.run(debug=True)
