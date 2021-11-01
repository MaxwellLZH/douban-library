import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, dcc, html
import json
import pandas as pd
from pathlib import Path


# global vars
cur_path = Path(__file__).parent
tag_file_path = cur_path.parent / 'data' / 'tags.csv'
book_file_path = cur_path.parent / 'data' / 'books.json'
book_detail_file_path = cur_path.parent / 'data' / 'book_detail.json'


# utility functions
def load_tags():
    return pd.read_csv(tag_file_path)


def load_books():
    with open(book_file_path, 'r') as f:
        return pd.DataFrame(json.load(f)).head(10)


def load_book_detail():
    pass


# variables used in the app
df_tags = load_tags()
df_books = load_books()

TAGS = df_tags.name


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

controls = dbc.Card(
    [
        html.Div(
            [
                dbc.Label("书籍类别:"),
                dcc.Dropdown(
                    id="tag",
                    options=[
                        {"label": i, "value": i} for i in TAGS
                    ],
                    value="所有",
                ),
            ]
        ),
        html.Div(
            [
                dbc.Label("排序方法:"),
                dcc.Dropdown(
                    id="sort-method",
                    options=[
                        {"label": i, "value": i} for i in ['发行时间', '评分（从高到底）']
                    ],
                    value="评分（从高到底）",
                ),
            ]
        ),
        # html.Div(
        #     [
        #         dbc.Label("Cluster count"),
        #         dbc.Input(id="cluster-count", type="number", value=3),
        #     ]
        # ),
    ],
    body=True,
)

table = dbc.Table.from_dataframe(df_books[['name', 'rating', 'from_url']],
                                id='table')
print(table.__dict__)

app.layout = dbc.Container(
    [
        html.H1("豆瓣图书馆"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, md=4),
                dbc.Col(table, md=8),
                # dbc.Col(dcc.Div(id="cluster-graph"), md=8),
            ],
            align="center",
        ),
    ],
    fluid=True,
)


@app.callback(
    Output("table", "data"),
    [Input("tag", "value")],
)
def filter_tag(tag):
    # minimal input validation, make sure there's at least one cluster
    df = iris.loc[:, [x, y]]
    km.fit(df.values)
    df["cluster"] = km.labels_


if __name__ == "__main__":
    app.run_server(debug=True, port=8888)