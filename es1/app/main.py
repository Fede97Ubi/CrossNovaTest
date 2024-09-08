import plotly.express as px
import dash
from dash import Dash, dcc, html, Input, Output
import psycopg2
import flask

app= flask.Flask(__name__)
dash_app = dash.Dash(__name__, server=app)
dash_app.config.suppress_callback_exceptions = True

host = '168.119.35.175'
port_id = 5433
database = 'auto'
user = 'candidato'
pwd = 'crossnection21'

conn = None
cur = None
data = [[],[],[],[],[],[],[]]
try:
    print("test docker 3")
    conn = psycopg2.connect(
        host = host,
        dbname = database,
        user = user,
        password = pwd,
        port = port_id
    )
    cur = conn.cursor()


    query = """
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'auto';
        """
    cur.execute(query)
    columns = cur.fetchall()
    culumnsName = [col[0] for col in columns]
    # print("Nomi delle colonne:", culumnsName)


    col1 = culumnsName[0]
    col2 = culumnsName[2]

    query = "SELECT * FROM auto;"
    # le parti testuali non hanno avuto bisogno di essere eliminate
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        data[0].append(row[0])
        data[1].append(row[1])
        data[2].append(row[2])
        data[3].append(row[3])
        data[4].append(row[4])
        data[5].append(row[5])
        data[6].append(row[6])
except Exception as error:
    print("test docker exeption")
    print(error)
finally:
    print("test docker finaly")
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()

dash_app.layout = html.Div([

    html.H1("Web Application with Dash Graph for Auto", style={'text-align': 'center'}),

    
    dcc.Dropdown(id="colonna1",
                 options=[
                     {"label": culumnsName[0], "value": culumnsName[0]},
                     {"label": culumnsName[1], "value": culumnsName[1]},
                     {"label": culumnsName[2], "value": culumnsName[2]},
                     {"label": culumnsName[3], "value": culumnsName[3]},
                     {"label": culumnsName[4], "value": culumnsName[4]},
                     {"label": culumnsName[5], "value": culumnsName[5]},
                     {"label": culumnsName[6], "value": culumnsName[6]}],
                 multi=False,
                 value=culumnsName[0],
                 style={'width': "40%"}
                 ),
    dcc.Dropdown(id="colonna2",
                 options=[
                     {"label": culumnsName[0], "value": culumnsName[0]},
                     {"label": culumnsName[1], "value": culumnsName[1]},
                     {"label": culumnsName[2], "value": culumnsName[2]},
                     {"label": culumnsName[3], "value": culumnsName[3]},
                     {"label": culumnsName[4], "value": culumnsName[4]},
                     {"label": culumnsName[5], "value": culumnsName[5]},
                     {"label": culumnsName[6], "value": culumnsName[6]}],
                 multi=False,
                 value=culumnsName[1],
                 style={'width': "40%"}
                 ),
    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='graph', figure={})

])

@dash_app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='graph', component_property='figure')],
    [Input(component_id='colonna1', component_property='value')],
    [Input(component_id='colonna2', component_property='value')]
)
def update_graph(col1sel, col2sel):
    container = None
    print("test docker 4")
    if col1sel == None:
        container = "selezionare il primo parametro"
    elif col1sel == col2sel:
        container = "è stato selezionato due volte lo stesso parametro : {}".format(col1sel)

    if col1sel == "acceleration":
        k = data[0]
    elif col1sel == "cilinders":
        k = data[1]
    elif col1sel == "displacement":
        k = data[2]
    elif col1sel == "horsepower":
        k = data[3]
    elif col1sel == "model_year":
        k = data[4]
    elif col1sel == "weight":
        k = data[5]
    elif col1sel == "mpg":
        k = data[6]
    else:
        k = []

    if col2sel == "acceleration":
        j = data[0]
    elif col2sel == "cilinders":
        j = data[1]
    elif col2sel == "displacement":
        j = data[2]
    elif col2sel == "horsepower":
        j = data[3]
    elif col2sel == "model_year":
        j = data[4]
    elif col2sel == "weight":
        j = data[5]
    elif col2sel == "mpg":
        j = data[6]
    else:
        j = k
    
    # k e j differiscono per come vengono gestiti nel caso null ma non è importante in un caso isolato come questo
    
    fig = px.scatter(x = k, y = j)
    fig.update_layout(xaxis_title=col1sel, yaxis_title=col2sel)

    print("test docker 5")
    return container, fig



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)