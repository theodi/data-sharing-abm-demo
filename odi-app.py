import os

import dash

from dash.dependencies import Input, Output, State
from dash_html_components import Div, Span, Img, P, Button, Details, Summary, A
from dash_core_components import (
    RadioItems,
    Checklist,
    Graph,
    Store,
    Tabs,
    Tab,
    Markdown,
)
import dash_bootstrap_components as dbc

from config import (
    TAB_DICT,
    DATA,
    TOOLTIP_STYLE,
    HOVERTEXTS,
    ITEM_BOTTOM,
    INTRO_MARKDOWN,
    DISCLAIMER,
    ABLED_STYLE_RADIO,
    DISABLED_STYLE_RADIO,
    PARAM_DF
)


external_stylesheets = [
    "https://fonts.googleapis.com/css?family=Dosis",
    "https://fonts.googleapis.com/css?family=Open+Sans",
    "https://fonts.googleapis.com/css?family=Ubuntu",
    "https://fonts.googleapis.com/css?family=Helvetica",
    dbc.themes.BOOTSTRAP,
]

# server = flask.Flask(__name__)
# app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets)

# from flask_cors import CORS
# CORS(app)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

def scenario_input_card(scen_name):
    """
    Function to create the scenario input boxes
    """
    return Div(
        children=[
            Div(
                P(
                    [
                        "Number of big companies:  ",
                        Span(
                            "\u003f\u20dd",
                            id=scen_name + "-tooltip-num-big-firms",
                            className="question-mark",
                        ),
                    ]
                ),
                style={"margin-left": 2},
            ),
            dbc.Tooltip(
                HOVERTEXTS["Number of big companies"],
                target=scen_name + "-tooltip-num-big-firms",
                style=TOOLTIP_STYLE,
                placement="right",
                arrowClassName="arrow",
            ),
            RadioItems(
                id=scen_name + "-num-big-firms",
                options=[{"label": x, "value": x} for x in [1, 2, 3, 4, "None"]],
                labelStyle={"display": "inline-block", "margin-right": "15px"},
                inputStyle={"margin-right": "6px", "verticalAlign": "middle"},
                value=1,
                style={"margin-bottom": "4%"},
            ),
            Div(
                P(
                    [
                        "Privacy concerns from customers: ",
                        Span(
                            "\u003f\u20dd",
                            id=scen_name + "-tooltip-privacy-concern",
                            className="question-mark",
                        ),
                    ]
                ),
                style={"margin-left": 2},
            ),
            dbc.Tooltip(
                HOVERTEXTS["Privacy concern"],
                target=scen_name + "-tooltip-privacy-concern",
                style=TOOLTIP_STYLE,
                placement="right",
            ),
            RadioItems(
                id=scen_name + "-privacy-concern",
                options=[
                    {"label": x, "value": x.lower()} for x in ["Low", "Medium", "High"]
                ],
                labelStyle={"display": "inline-block", "margin-right": "15px"},
                inputStyle={"margin-right": "10px", "verticalAlign": "middle"},
                value="medium",
                style={"margin-bottom": "4%"},
            ),
            Div(
                P(
                    [
                        "Consumer preference for multiple products from the same company: ",
                        Span(
                            "\u003f\u20dd",
                            id=scen_name + "-tooltip-loyalty",
                            className="question-mark",
                        ),
                    ]
                ),
                style={"margin-left": 2},
            ),
            dbc.Tooltip(
                HOVERTEXTS[
                    "Consumer preference for multiple products from the same company"
                ],
                target=scen_name + "-tooltip-loyalty",
                style=TOOLTIP_STYLE,
                placement="right",
            ),
            RadioItems(
                id=scen_name + "-loyalty",
                options=[
                    {"label": x, "value": x.lower()} for x in ["Low", "Medium", "High"]
                ],
                labelStyle={"display": "inline-block", "margin-right": "15px"},
                inputStyle={"margin-right": "10px", "verticalAlign": "middle"},
                value="medium",
                style={"margin-bottom": "4%"},
            ),
            Div(
                P(
                    [
                        "Openness: ",
                        Span(
                            "\u003f\u20dd",
                            id=scen_name + "-tooltip-openness",
                            className="question-mark",
                        ),
                    ]
                ),
                style={"margin-left": 2},
            ),
            dbc.Tooltip(
                HOVERTEXTS["Openness"],
                target=scen_name + "-tooltip-openness",
                style=TOOLTIP_STYLE,
                placement="right",
            ),
            RadioItems(
                id=scen_name + "-openness",
                options=[
                    {"label": x, "value": x.lower()} for x in ["Low", "Medium", "High"]
                ],
                labelStyle={"display": "inline-block", "margin-right": "15px"},
                inputStyle={"margin-right": "10px", "verticalAlign": "middle"},
                value="medium",
                style={"margin-bottom": "4%"},
            ),
            P(
                [
                    "Privacy shock ",
                    Span(
                        "\u003f\u20dd",
                        id=scen_name + "-tooltip-privacy",
                        className="question-mark",
                    ),
                ],
                style={"margin-bottom": "0%", "margin-left": 2},
            ),
            P(
                "(can be applied to several firms)",
                style={"font-size": "12px", "margin-bottom": "0%"},
            ),
            dbc.Tooltip(
                HOVERTEXTS["Privacy shock"],
                target=scen_name + "-tooltip-privacy",
                style=TOOLTIP_STYLE,
                placement="right",
            ),
            Checklist(
                id=scen_name + "-privacy-onoff",
                options=[{"label": "Include a privacy shock", "value": True}],
                values=[],
                inputStyle={"margin-right": "5px"},
                style={"margin-bottom": "2%", "margin-top": "0%"},
            ),
            RadioItems(
                id=scen_name + "-shock-num",
                options=[{"label": x, "value": x} for x in [1, 2, 3, 4]],
                labelStyle={
                    "display": "inline-block",
                    "margin-right": "15px",
                    "padding-bottom": ITEM_BOTTOM,
                },
                inputStyle={"margin-right": "10px"},
                value=1,
                style={"margin-bottom": "4%"},
            ),
        ],
        className="scenario-input",
        style={"background-color": "rgb(234, 234, 234)", "font-size": "16px"},
    )


# Layout
app.layout = Div(
    [
        Div([Store(x + "-store-" + str(i)) for x in TAB_DICT.keys() for i in [1, 2]]),
        # header
        Div(
            Div(
                children=[
                    Span(
                        "Using an ‘agent based model’ for data policy decision-making"
                    ),
                    Div(
                        A(
                            Img(
                                src="/assets/basic-W-48px.png",
                                height="80%",
                                style={"align": "center"},
                            ),
                            href="https://theodi.org",
                            target="_blank",
                        ),
                        className="brandimage",
                    ),
                ],
                className="insideheader",
            ),
            className="header",
        ),
        Div(
            Details(
                [
                    Summary(
                        "What is this about?",
                        style={
                            "color": "white",
                            "backgroundColor": "#1DD3A7",
                            "paddingLeft": "2%",
                            "fontSize": "12px",
                        },
                    ),
                    Div(Markdown(INTRO_MARKDOWN), style={"margin": "2%"})
                ]
            ),
        ),
        Div(  # body
            Div(
                children=[
                    Div(  # left hand side (input)
                        children=[
                            Div(
                                "Compare two scenarios by changing the parameters below",
                                style={"padding-left": 20},
                                className="big-text",
                            ),
                            Div("Scenario 1", className="scenario-name"),
                            scenario_input_card("scen1"),
                            Div("Scenario 2", className="scenario-name"),
                            scenario_input_card("scen2"),
                            Div(
                                Button(
                                    "Apply parameters >",
                                    n_clicks=0,
                                    id="apply-button",
                                    style={
                                        "float": "right",
                                        "margin": "5px",
                                        "border-radius": "25.5px",
                                        "background-color": "#000000",
                                        "color": "white",
                                        "border": "0px",
                                    },
                                )
                            ),
                        ],
                        className="three columns",
                        style={
                            "padding-left": 20,
                            "padding-right": 20,
                            "background-color": "rgb(248, 248, 248)",
                            "padding-top": 20,
                        },
                    ),  # closes left hand side (input) Div
                    Div(  # right hand side (graphs)
                        children=[
                            Div(
                                Div(
                                    "Visualize how the parameters influence your model",
                                    style={
                                        "padding-left": 20,
                                        "padding-bottom": "30px",
                                    },
                                    className="big-text",
                                ),
                                className="row",
                            ),
                            Tabs(
                                id="tab",
                                children=[
                                    Tab(
                                        label=y["label"],
                                        value=x,
                                        className="custom-tab",
                                        selected_className="custom-tab--selected",
                                    )
                                    for x, y in TAB_DICT.items()
                                ],
                                value=list(TAB_DICT.keys())[0],
                                colors={
                                    "background": "white",
                                    "border": "#d6d6d6",
                                    "primary": "#1975FA",
                                },
                            ),
                            Div(
                                children=[
                                    P(
                                        id="tab-text",
                                        style={"margin": "20px", "font-size": "13px"},
                                    )
                                ]
                                + [
                                    Div(
                                        Graph(
                                            id=x + "-graph"
                                        ),
                                        id=x + "-graph-div",
                                        style={"display": "none"}
                                    )
                                    for x in TAB_DICT.keys()
                                ],
                                style={"border": "1px solid #d6d6d6"},
                            ),
                        ],
                        className="nine columns",
                        style={
                            "padding-left": 20,
                            "padding-right": 2,
                            "background-color": "white",
                            "padding-top": 20,
                            "height": "100%",
                        },
                    ),  # closes right hand side (graphs) Div
                ],
                className="row",
            )
        ),  # closes the body div
        Div(Markdown(DISCLAIMER), className="footer", style={"margin": "2%"}),
    ]
)


# callbacks for styling
@app.callback(
    Output("scen1-shock-num", "labelStyle"), [Input("scen1-privacy-onoff", "values")]
)
def decolour_input_1(vals):
    return ABLED_STYLE_RADIO if (True in vals) else DISABLED_STYLE_RADIO


@app.callback(
    Output("scen2-shock-num", "labelStyle"), [Input("scen2-privacy-onoff", "values")]
)
def decolour_input_2(vals):
    return ABLED_STYLE_RADIO if (True in vals) else DISABLED_STYLE_RADIO


@app.callback(
    Output("scen1-shock-num", "options"),
    [Input("scen1-privacy-onoff", "values")],
    [State("scen1-shock-num", "options")],
)
def disable_input_1(vals, opts):
    return [
        {"label": opt["label"], "value": opt["value"], "disabled": (vals == [])}
        for opt in opts
    ]


@app.callback(
    Output("scen2-shock-num", "options"),
    [Input("scen2-privacy-onoff", "values")],
    [State("scen2-shock-num", "options")],
)
def disable_input_2(vals, opts):
    return [
        {"label": opt["label"], "value": opt["value"], "disabled": (vals == [])}
        for opt in opts
    ]


# changing the info text displayed above each figure
@app.callback(Output("tab-text", "children"), [Input("tab", "value")])
def tab_text(val):
    return TAB_DICT[val]["text"]


# whenever user clicks the 'apply scenarios button' we update two stores which
# have the index of the output to use as a string
def update_store_fn(i, x):
    # store just holds a string with the right output number
    def callback(n_click, nbf, pc, l, openness, shock_num, p_onoff):
        if True in p_onoff:
            idx = PARAM_DF.loc[
                (PARAM_DF.n_init_big_firms == str(nbf))
                & (PARAM_DF.mean_cons_concern == pc)
                & (PARAM_DF.w_loyal_firm == l)
                & (PARAM_DF.scen_number_of_firms == str(shock_num))
                & (PARAM_DF.openness_lower == openness)
            ].index[0]
        else:
            idx = PARAM_DF.loc[
                (PARAM_DF.n_init_big_firms == str(nbf))
                & (PARAM_DF.mean_cons_concern == pc)
                & (PARAM_DF.w_loyal_firm == l)
                & (PARAM_DF.scen_number_of_firms == str(0))
                & (PARAM_DF.openness_lower == openness)
            ].index[0]
        return str(idx)

    return callback


for i in [1, 2]:
    for x in TAB_DICT.keys():
        app.callback(
            Output(x + "-store-" + str(i), "data"),
            [Input("apply-button", "n_clicks")],
            [
                State("scen" + str(i) + y, "value")
                for y in [
                    "-num-big-firms",
                    "-privacy-concern",
                    "-loyalty",
                    "-openness",
                    "-shock-num",
                ]
            ]
            + [State("scen" + str(i) + "-privacy-onoff", "values")],
        )(update_store_fn(i, x))


# after clicking apply button, all figures are updated with the correct data
def update_figure(x):
    def callback(st1, st2):
        print(st1, st2)
        return TAB_DICT[x]["figure"](
            DATA["output_" + st1][TAB_DICT[x]["store"]],
            DATA["output_" + st2][TAB_DICT[x]["store"]],
        )

    return callback


# when user clicks a tab, only make visible the relevant figure
def hidden_status_graph(x):
    def callback(tabname):
        return {"display": "block"} if tabname == x else {"display": "none"}

    return callback


for x in TAB_DICT.keys():
    app.callback(
        Output(x + "-graph", "figure"),
        [Input(x + "-store-1", "data"), Input(x + "-store-2", "data")],
    )(update_figure(x))
    app.callback(Output(x + "-graph-div", "style"), [Input("tab", "value")])(
        hidden_status_graph(x)
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run_server(host='0.0.0.0', port=port, debug=True)

    # app.run_server(host='0.0.0.0', debug=True)
