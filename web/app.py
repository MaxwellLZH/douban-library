import dash
from dash import dash_table
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
        return pd.DataFrame(json.load(f))


def load_book_detail():
    with open(book_detail_file_path, 'r') as f:
        j = json.load(f)
        print(j[0])
        print(j[1])
        return pd.DataFrame(json.load(f))


# variables used in the app
df_tags = load_tags()
df_books = load_books()
df_book_detail = load_book_detail()

TAGS = df_tags.name


print(df_book_detail.columns)

#
# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
#
# controls = dbc.Card(
#     [
#         html.Div(
#             [
#                 dbc.Label("书籍类别:"),
#                 dcc.Dropdown(
#                     id="tag",
#                     options=[
#                         {"label": i, "value": i} for i in TAGS
#                     ],
#                     value="所有",
#                 ),
#             ]
#         ),
#         html.Div(
#             [
#                 dbc.Label("排序方法:"),
#                 dcc.Dropdown(
#                     id="sort-method",
#                     options=[
#                         {"label": i, "value": i} for i in ['发行时间', '评分（从高到底）']
#                     ],
#                     value="评分（从高到底）",
#                 ),
#             ]
#         ),
#         # html.Div(
#         #     [
#         #         dbc.Label("Cluster count"),
#         #         dbc.Input(id="cluster-count", type="number", value=3),
#         #     ]
#         # ),
#     ],
#     body=True,
# )
#
# # table = dbc.Table.from_dataframe(df_books[['name', 'rating', 'from_url']],
# #                                 id='table')
#
# df = df_books[['name', 'rating', 'from_url']].head(5000)
#
# table = dash_table.DataTable(
#         id='datatable',
#         columns=[
#             {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
#         ],
#         data=df.to_dict('records'),
#         editable=True,
#         filter_action="native",
#         sort_action="native",
#         sort_mode="multi",
#         column_selectable="single",
#         row_selectable="single",
#         row_deletable=True,
#         selected_columns=[],
#         selected_rows=[],
#         page_action="native",
#         page_current=0,
#         page_size=10,
#     ),
#
#
# app.layout = dbc.Container(
#     [
#         html.H1("豆瓣读书"),
#         html.Hr(),
#         dbc.Row(
#             [
#                 dbc.Col(controls, md=4),
#                 dbc.Col(table, md=8),
#                 # dbc.Col(dcc.Div(id="cluster-graph"), md=8),
#             ],
#             align="center",
#         ),
#     ],
#     fluid=True,
# )
#
#
# # @app.callback(
# #     Output("datatable", "data"),
# #     [Input("tag", "value")],
# # )
# # def filter_tag(tag):
# #     d = df_books[df_books['tag']]
# #     pass
#
#
# if __name__ == "__main__":
#     app.run_server(debug=True, port=8888)