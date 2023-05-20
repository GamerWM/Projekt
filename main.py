from dash import Dash, html, dcc, Input, Output, State, dash_table, ctx
from simulator import Simulator
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate


app = Dash(__name__)
app.title = 'Symulator'

def blank_figure():
    #stylizuje pusty wykres na czarny motyw
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template='plotly_dark')
    return fig

#stylizowanie strony
app.layout = html.Div(children=[
    html.Div(id='all-side', children=[
        dcc.Graph(id='road-graph', style={'width':'100vw', 'margin-left':'0'}, figure=blank_figure()),
        dcc.Input(id='x-input', className='input-field', style={'margin-left':'5vw'}),
        dcc.Input(id='y-input', className='input-field'),
        html.Button(id='add-point-button', children='Add Point', n_clicks=0, style={'width' : '7vw'}),
        html.Div(id='new-point', style={'margin':'20px 20vw'}, children=[
            
            
            dash_table.DataTable(columns=[
                {'name': i, 'id': i, 'selectable': True} for i in ['Name', 'Max speed', 'Max acceleration', 'Min acceleration', 'Mass']
            ],  data=[], 
                row_selectable='multi',
                selected_rows= [],
                id='car-table',
                style_header={'background-color': 'rgb(47, 47, 47)', 'color': 'white'}
            ),

            dcc.Input(id='name-input', className='input-field'),
            dcc.Input(id='speed-input', className='input-field'),
            dcc.Input(id='max-acc-input', className='input-field'),
            dcc.Input(id='min-acc-input', className='input-field'),
            dcc.Input(id='mass-input', className='input-field'),
            html.Button(id='add-car-button', children='Add', n_clicks=0),
            html.Button(id='del-car-button', children='Delete', n_clicks=0),
            dcc.Store(id='cars')
        ])
    ]),
    
    html.Div(id='all-side-2', style={'display':'None'}, children=[
        dcc.Graph(id='graph-velocity', style={'width':'50%', 'float':'left'}, figure=blank_figure()),
        dcc.Graph(id='graph-acceleration', style={'width':'50%', 'float':'left'}, figure=blank_figure())
    ]),
    dcc.Store(id='road'),
    html.Button(children='Click Me', id='demo-button', style={'margin':'30px 35%', 'padding': '1%', 'font-size' : '150%', 'width' : '30%'}),
])

#obslugiwanie akcji związanych z tabelą aut
@app.callback(
        Output(component_id='cars', component_property='data'),
        Output(component_id='car-table', component_property='data'),
        Input(component_id='add-car-button', component_property='n_clicks'),
        Input(component_id='del-car-button', component_property='n_clicks'),
        State(component_id='name-input', component_property='value'),
        State(component_id='speed-input', component_property='value'),
        State(component_id='max-acc-input', component_property='value'),
        State(component_id='min-acc-input', component_property='value'),
        State(component_id='mass-input', component_property='value'),
        State(component_id='cars', component_property='data'),
        prevent_initial_call=True
)
def handle_car_table(click_add, click_del, name, speed, max_acc, min_acc, mass, data):
    triggered_id = ctx.triggered_id
    if triggered_id == 'add-car-button':
        return add_new_car(name, speed, max_acc, min_acc, mass, data)
    elif triggered_id == 'del-car-button':
        return delete_car(data)

def add_new_car(name, speed, max_acc, min_acc, mass, data):
    if name == '' or speed == '' or max_acc == '' or min_acc == '' or mass == '':
        raise PreventUpdate

    data = data or []
    data.append({'Name': name, 'Max speed': speed, 'Max acceleration': max_acc, 'Min acceleration': min_acc, 'Mass': mass})
    cars = data
    return data, cars

def delete_car(data):
    print(data)

#dodawanie punktów na trasie
@app.callback(
        Output(component_id='road', component_property='data'),
        Output(component_id='road-graph', component_property='figure'),
        Input(component_id='add-point-button', component_property='n_clicks'),
        State(component_id='x-input', component_property='value'),
        State(component_id='y-input', component_property='value'),
        State(component_id='road', component_property='data'),
        prevent_initial_call=True
)
def add_point(click, x_value, y_value, road):
    if x_value == '' or y_value == '':
        raise PreventUpdate

    data = road or {'x': [], 'y': []}
    
    data['x'].append(int(x_value))
    data['y'].append(int(y_value))

    fig = go.Figure(go.Scatter(x=data['x'], y=data['y']))
    fig.update_layout(template='plotly_dark')

    return data, fig

#crap do testów pozniej sie to usunie
@app.callback(
        # Output(component_id='graph-velocity', component_property='figure'),
        # Output(component_id='graph-acceleration', component_property='figure'),
        Output(component_id='all-side-2', component_property='style'),
        Input(component_id='demo-button', component_property='n_clicks'),
        State(component_id='all-side-2', component_property='style'),
        prevent_initial_call=True

)
def display_section(click, style):
    if click == None:
        raise PreventUpdate
    
    style = dict(style)
    if style['display'] == 'None':
        style['display'] = 'Block'
    elif style['display'] == 'Block':
        style['display'] = 'None'
    
    print(style)
    return style

# def buttonPressed(value):
#     if value == None:
#         raise PreventUpdate
#     else:
#         sim = Simulator(10, 10, -10, 50)
#         road = [[0, 750], [300, 650], [600, 650], [900, 750]]
#         sim.simulate(road)

#         fig = go.Figure(go.Scatter(x=sim.time, y=sim.velocity, name='Velocity'))
#         fig.update_xaxes(title='Time [s]')
#         fig.update_yaxes(title='Velocity [m/s]')
#         fig.update_layout(template='plotly_dark')

#         fig2 = go.Figure(go.Scatter(x=sim.time, y=sim.acceleration))
#         fig2.update_xaxes(title='Time [s]')
#         fig2.update_yaxes(title='Acceleration [m/s^2]')
#         fig2.update_layout(template='plotly_dark')

#         return fig, fig2

if __name__ == "__main__":
    app.run_server(debug=True)

 