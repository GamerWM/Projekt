from dash import Dash, html, dcc, Input, Output, State, dash_table, ctx, ClientsideFunction
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
    html.Div(id='menu-bar', children=[      
        html.Button(id='show-road', className='display-button', n_clicks=0),
        html.Button(id='show-results', className='display-button', n_clicks=0)
    ]),
    html.Div(id='all-side', style = {'width' : '91%', 'display': 'block'}, children=[
        dcc.Graph(id='road-graph', style={'width':'100%', 'margin':'0'}, figure=blank_figure()),
    ]),

        html.Div(id='car-stats-table', style={'display' : 'block'}, children=[
            dash_table.DataTable(columns=[
                {'name': i, 'id': i, 'selectable': True} for i in ['Name', 'Max speed', 'Max acceleration', 'Min acceleration', 'Mass']
            ],  data=[], 
                row_selectable='multi',
                selected_rows= [],
                id='car-table',
                style_header={'background-color': 'rgb(47, 47, 47)', 'color': 'white'}
            ),
        html.Div(id='car-stats-input-fields', children=[
            dcc.Input(id='name-input', className='input-field'),
            dcc.Input(id='speed-input', className='input-field'),
            dcc.Input(id='max-acc-input', className='input-field'),
            dcc.Input(id='min-acc-input', className='input-field'),
            dcc.Input(id='mass-input', className='input-field'),
            html.Button(id='add-car-button', children='Add', n_clicks=0),
            html.Button(id='del-car-button', children='Delete', n_clicks=0),
            dcc.Store(id='cars')
        ]),
        ]),
    html.Div(id='input-point', style = {'display' : 'block'}, children=[
        dcc.Input(id='x-input', className='input-field'),
        dcc.Input(id='y-input', className='input-field'),
        html.Button(id='add-point-button', children='Add Point', n_clicks=0),
        html.Button(id='delete-point-button', children='Delete Point', n_clicks=0),
    ]),
    
    html.Div(id='all-side-2', style={'width': '91%', 'display':'block'}, children=[
        dcc.Graph(id='graph-velocity', style = {'width' : '50%'}, figure=blank_figure()),
        dcc.Graph(id='graph-acceleration', style = {'width' : '50%'}, figure=blank_figure())
    ]),
    dcc.Store(id='road'),
    html.Button(children='Calculate', style = {'display':'block'}, id='demo-button'),
    
    #Dodanie Javascriptu
    html.Script(
        src ='assets/script.js defer',
        type ='text/javascript'
    ),
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
        Output(component_id='graph-velocity', component_property='style'),
        Output(component_id='graph-acceleration', component_property='style'),
        Output(component_id='all-side', component_property='style'),
        Output(component_id='input-point', component_property='style'),
        Output(component_id='car-stats-table', component_property='style'),
        Output(component_id='demo-button', component_property='style'),
        Input(component_id='show-road', component_property='n_clicks'),
        Input(component_id='show-results', component_property='n_clicks'),
        State(component_id='all-side-2', component_property='style'),
        State(component_id='graph-velocity', component_property='style'),
        State(component_id='graph-acceleration', component_property='style'),
        State(component_id='all-side', component_property='style'),
        State(component_id='input-point', component_property='style'),
        State(component_id='car-stats-table', component_property='style'),
        State(component_id='demo-button', component_property='style'),
        prevent_initial_call=True

)

def change_width(n_clicks, n_clicks_2, style_all_side_2, velocity, acceleration, style_all_side, input_point, car_stats_table, demo_button):
    if n_clicks and style_all_side is not None:
        style_all_side_2['width'] = '45.5%'
        style_all_side_2['position'] = 'absolute'    
        style_all_side_2['top'] = '0px'    
        style_all_side_2['right'] = '0px'   
        velocity['width'] = '100%'
        acceleration['width'] = '100%' 
        style_all_side['width'] = '45.5%'
        style_all_side['float'] = 'left'
        style_all_side['margin-left'] = '9%'
        style_all_side['display'] = 'block'
        input_point['width'] = '45.5%'
        input_point['margin-left'] = '9%'
        input_point['float'] = 'none'
        input_point['padding-top'] = '2%'
        input_point['display'] = 'block'
        car_stats_table['float'] = 'none'
        car_stats_table['width'] = '45.5%'
        car_stats_table['margin-left'] = '11%'
        car_stats_table['display'] = 'block'
        demo_button['margin-top'] = '15%'
        demo_button['display'] = 'block'

        return style_all_side_2, velocity, acceleration, style_all_side, input_point, car_stats_table, demo_button


    if n_clicks_2 and style_all_side_2 is not None:
        style_all_side_2['width'] = '91%'
        style_all_side_2['display'] = 'block'
        style_all_side['display'] = 'None'
        input_point['display'] = 'None'
        car_stats_table['display'] = 'None'
        demo_button['display'] = 'None'
        return style_all_side_2, velocity, acceleration, style_all_side, input_point, car_stats_table, demo_button


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

 