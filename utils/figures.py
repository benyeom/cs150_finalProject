def create_bar_chart(df, year):
    from plotly.graph_objs import Bar, Layout

    filtered = df[df["Year"] == year]

    trace1 = Bar(
        x=["Medication"],
        y=filtered["Medication"],
        name="Antidepressant Prescriptions",
        marker_color='red',
        text=filtered["Medication"].astype(str) + "M",
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(size=16)
    )

    trace2 = Bar(
        x=["Therapy"],
        y=filtered["Therapy"],
        name="Counseling Sessions",
        marker_color='blue',
        text=filtered["Therapy"].astype(str) + "M",
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(size=16)
    )

    return {
        "data": [trace1, trace2],
        "layout": Layout(
            title=f"Treatment Comparison for {year}",
            xaxis={"title": "Treatment Type"},
            yaxis={"title": "# of Individual Cases (in millions)"},
            barmode="group",
            legend={"x": 1.0, "y": 1.1, "xanchor": "right", "yanchor": "top"},
            margin={"t": 50, "r": 50}
        )
    }

def create_percentage_line_chart(df):
    import plotly.graph_objs as go
    years = df["Year"]
    trace1 = go.Scatter(
        x=years,
        y=df["Medication_Percentage"],
        mode='lines+markers+text',
        name="Medication Usage (%)",
        line=dict(color='red'),
        text=["" for _ in range(len(df) - 1)] + ["Medication"],
        textposition="middle right",
        textfont=dict(size=16),
        showlegend=False
    )
    trace2 = go.Scatter(
        x=years,
        y=df["Therapy_Percentage"],
        mode='lines+markers+text',
        name="Therapy Usage (%)",
        line=dict(color='blue'),
        text=["" for _ in range(len(df) - 1)] + ["Therapy"],
        textposition="middle right",
        textfont=dict(size=16),
        showlegend=False
    )
    layout = go.Layout(
        xaxis={"title": {"text": "Year", "font": {"size": 20, "family": "Arial"}}, "range": [2010, 2023.5]},
        yaxis={"title": {"text": "Percentage of Population (%)", "font": {"size": 20, "family": "Arial"}}},
        margin={"t": 50, "r": 140},
        title=None
    )
    return {"data": [trace1, trace2], "layout": layout}


def create_heatmap():
    import pandas as pd
    import numpy as np
    import plotly.express as px

    df_dep = pd.read_csv("assets/dttw-5yxu.csv")
    df_dep = df_dep[['locationabbr', 'year', 'data_value']]
    df_dep.rename(columns={
        'locationabbr': 'State',
        'year': 'Year',
        'data_value': 'Depression_Prevalence'
    }, inplace=True)

    df_inc = pd.read_csv("assets/MEHOINUSA646N.csv")
    df_inc['Year'] = pd.to_datetime(df_inc['observation_date']).dt.year
    df_inc = df_inc[['Year', 'MEHOINUSA646N']].rename(columns={'MEHOINUSA646N': 'Median_Income'})

    df = pd.merge(df_dep, df_inc, on='Year', how='left')
    df.dropna(subset=['Depression_Prevalence', 'Median_Income'], inplace=True)

    unique_inc = df['Median_Income'].unique()
    if len(unique_inc) > 1:
        income_bins = np.linspace(df['Median_Income'].min(), df['Median_Income'].max(), 6)
    else:
        mid = unique_inc[0]
        income_bins = [mid - 1000, mid + 1000]

    unique_dep = df['Depression_Prevalence'].unique()
    if len(unique_dep) > 1:
        dep_bins = np.linspace(df['Depression_Prevalence'].min(), df['Depression_Prevalence'].max(), 6)
    else:
        mid_dep = unique_dep[0]
        dep_bins = [mid_dep - 1, mid_dep + 1]

    df['Income_bin'] = pd.cut(df['Median_Income'], bins=income_bins)
    df['Dep_bin'] = pd.cut(df['Depression_Prevalence'], bins=dep_bins)

    heatmap_df = (
        df.groupby(['Dep_bin', 'Income_bin'], observed=False)
        .size()
        .reset_index(name='Count')
        .pivot(index='Dep_bin', columns='Income_bin', values='Count')
        .fillna(0)
    )

    fig = px.imshow(
        heatmap_df.values,
        x=[f"{int(b.left)}–{int(b.right)}" for b in heatmap_df.columns],
        y=[f"{b.left:.1f}–{b.right:.1f}" for b in heatmap_df.index],
        labels={
            'x': 'Median Income Bin',
            'y': 'Depression Prevalence Bin (%)',
            'color': 'Number of States'
        },
        aspect='auto',
        color_continuous_scale='RdBu_r'  # blue to red
    )

    return fig

def create_cost_bar_chart():
    import pandas as pd
    import plotly.graph_objs as go

    df = pd.read_csv("assets/Mental health treatment costs 2009-2020.csv")
    df.columns = ["Year", "Spending"]
    df["Year"] = df["Year"].astype(int)

    line = go.Scatter(
        x=df["Year"],
        y=df["Spending"],
        mode="lines+markers+text",
        name="Spending",
        line=dict(color="blue", width=3),
        text=df["Spending"].astype(str) + "B",
        textposition="top center",
        textfont=dict(size=18, family="Arial", color="black")
    )

    layout = go.Layout(
        xaxis={"title": {"text": "Year", "font": {"size": 20, "family": "Arial"}}},
        yaxis={"title": {"text": "Spending (Billion USD)", "font": {"size": 20, "family": "Arial"}}},
        margin={"t": 60},
        title=None
    )

    return {"data": [line], "layout": layout}


def create_choropleth_map():
    import pandas as pd
    import plotly.express as px

    dep_df = pd.read_csv("assets/Prevalence of Depression in US by state.csv")
    inact_df = pd.read_csv("assets/Prevalence of Inactivity in US by state.csv")

    # Clean and keep only relevant columns
    dep_df = dep_df[["State", "Prevalence %"]]
    dep_df["Prevalence %"] = dep_df["Prevalence %"].str.replace('%', '').astype(float)

    inact_df = inact_df.rename(columns={"Feature": "State", "Percentage of adults": "Inactivity %"})
    inact_df["Inactivity %"] = inact_df["Inactivity %"].str.replace('%', '').str.strip().astype(float)

    # Use state abbreviations for mapping
    state_abbr = {
        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
        'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
        'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
        'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
        'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
        'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH',
        'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC',
        'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA',
        'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN',
        'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
        'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
    }

    dep_df["Abbreviation"] = dep_df["State"].map(state_abbr)
    inact_df["Abbreviation"] = inact_df["State"].map(state_abbr)

    merged = pd.merge(dep_df, inact_df, on="Abbreviation", suffixes=("_Dep", "_Inact"))
    merged = merged.dropna(subset=["Prevalence %", "Inactivity %"])

    fig = px.choropleth(
        merged,
        locations="Abbreviation",
        locationmode="USA-states",
        scope="usa",
        color="Prevalence %",
        hover_name="State_Dep",
        hover_data={"Prevalence %": True, "Inactivity %": True, "Abbreviation": False},
        color_continuous_scale="Reds",
        labels={"Prevalence %": "Depression %"},
        title="Depression Prevalence by State (Hover shows Inactivity %)"
    )

    fig.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})

    return fig

def create_healthcare_cost_chart():
    import pandas as pd
    import plotly.graph_objs as go

    df = pd.read_csv("assets/Annual healthcare costs US 2023.csv")
    df.columns = ["Category", "Cost"]
    df["Cost"] = df["Cost"].str.replace(",", "").astype(float)

    df_filtered = df[df["Category"].isin(["Pharmacy", "Professional Services"])].copy()
    exercise_row = pd.DataFrame([{"Category": "Exercise", "Cost": 0.0}])
    df_filtered = pd.concat([df_filtered, exercise_row], ignore_index=True)

    bar_labels = ["$" + str(int(val)) for val in df_filtered["Cost"]]

    bar = go.Bar(
        x=df_filtered["Category"],
        y=df_filtered["Cost"],
        marker_color=["blue", "blue", "green"],
        text=bar_labels,
        textposition="inside",
        insidetextanchor="middle",
        textfont=dict(size=22, family="Arial", color="white"),
    )

    layout = go.Layout(
        xaxis={"title": {"text": "Category", "font": {"size": 20, "family": "Arial"}}},
        yaxis={"title": {"text": "Cost (USD)", "font": {"size": 20, "family": "Arial"}}, "range": [0, df_filtered["Cost"].max() * 1.15]},
        margin={"t": 80},
        title=None
    )

    return {"data": [bar], "layout": layout}

def create_separate_regression_scatterplots():
    import pandas as pd
    import numpy as np
    import plotly.graph_objs as go

    # Load and clean data
    dep_df = pd.read_csv("assets/Average depression rate US 2015-2022.csv")
    ex_df = pd.read_csv("assets/Average exercise rate US 2015-2022.csv")
    med_df = pd.read_csv("assets/(1) Medication usage_(sertraline) prescriptions 2010-2022.csv")
    ther_df = pd.read_csv("assets/(1) Therapy_counseling usage 2010-2022.csv")

    dep_df.columns = ["Year", "Depression"]
    dep_df["Year"] = dep_df["Year"].astype(int)
    dep_df["Depression"] = dep_df["Depression"].str.replace('%', '').astype(float)

    ex_df.columns = ["Year", "Exercise"]
    ex_df["Year"] = ex_df["Year"].astype(int)
    ex_df["Exercise"] = ex_df["Exercise"].str.replace('%', '').astype(float)

    med_df.columns = ["Year", "Medication"]
    med_df["Year"] = med_df["Year"].astype(int)

    ther_df.columns = ["Year", "Therapy"]
    ther_df["Year"] = ther_df["Year"].astype(int)

    df = dep_df.merge(ex_df, on="Year")
    df = df.merge(med_df, on="Year")
    df = df.merge(ther_df, on="Year")
    df = df[df["Year"].between(2015, 2022)]

    def make_scatter_with_regression(x, y, x_label, title, color):
        scatter = go.Scatter(
            x=x,
            y=y,
            mode='markers',
            marker=dict(color=color, size=10),
            name="Data"
        )

        # Fit regression line
        slope, intercept = np.polyfit(x, y, 1)
        x_range = np.linspace(min(x), max(x), 100)
        y_pred = slope * x_range + intercept

        line = go.Scatter(
            x=x_range,
            y=y_pred,
            mode='lines',
            line=dict(color=color, width=2, dash='dash'),
            name="Trendline"
        )

        layout = go.Layout(
            title={"text": title, "font": {"size": 24}, "x": 0.5},
            xaxis={"title": {"text": x_label, "font": {"size": 20, "family": "Arial"}}},
            yaxis={"title": {"text": "Depression Rate (%)", "font": {"size": 20, "family": "Arial"}}},
            margin={"t": 60}
        )

        return go.Figure(data=[scatter, line], layout=layout)

    fig1 = make_scatter_with_regression(df["Exercise"], df["Depression"], "Exercise Rate (%)", "Exercise vs Depression", "green")
    fig2 = make_scatter_with_regression(df["Therapy"], df["Depression"], "Therapy Usage (Millions)", "Therapy vs Depression", "blue")
    fig3 = make_scatter_with_regression(df["Medication"], df["Depression"], "Medication Usage (Millions)", "Medication vs Depression", "red")

    return fig1, fig2, fig3
