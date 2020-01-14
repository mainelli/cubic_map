import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output, State

df = pd.read_csv('https://raw.githubusercontent.com/mainelli/cubic_map/master/Origins_and_Destinations_sample.csv')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        dcc.Graph(
            id='cube',
            clear_on_unhover=True,
            figure=dict(
                layout=go.Layout(
                )
            )
        )
    ],
        id='divcube',
        style={
            'float': 'center',
            'textAlign': 'center',
            'display': 'block',
            'margin-bottom': '30px',
            'padding': '5px',
        }
    )
]
)


@app.callback(  # updates the map whenever a click occurs
    Output('cube', 'figure'),
    [Input('cube', 'clickData')],
    state=[State('cube', 'figure')])
def update_cube(clickData, _):
    dff = df
    origin_name = ''
    if clickData and len(clickData['points']) > 0:
        origin_name = clickData['points'][0]['hovertext']
        print("origin_name is " + origin_name)
        dff = df[df['OrigName'] == origin_name]

    x_lines = list()
    y_lines = list()
    z_lines = list()

    for i, p in dff.iterrows():
        x_lines.append(p['OrigLat'])
        y_lines.append(p['OrigLon'])
        z_lines.append(0)
        x_lines.append(p['DestLat'])
        y_lines.append(p['DestLon'])
        z_lines.append(1)
        x_lines.append(None)
        y_lines.append(None)
        z_lines.append(None)

    return dict(
        data=[go.Scatter3d(  # data for all the ORIGINS
            x=df['OrigLat'],
            y=df['OrigLon'],
            z=[0] * df.shape[0],  # makes the z value 0, so that all origins are together on one face of the cube
            hoverinfo='text',  # Hides the x,y,z values being shown on hover-over
            hovertext=df['OrigName'],
            mode='markers',
            marker=dict(
                size=5,
                symbol='circle',
                color='#fc197f',
                opacity=1,
                line=dict(
                    width=1,
                    color='#fce702'
                )
            )
        ),
            go.Scatter3d(  # data for all the DESTINATIONS
                x=dff['DestLat'],
                y=dff['DestLon'],
                z=[1] * dff.shape[0],  # makes the z value 1, so that all destinations are together on the opposite face of the cube
                hoverinfo='text',  # Hides the x,y,z values being shown on hover-over
                hovertext=dff['DestName'],
                mode='markers',
                marker=dict(
                    size=5,
                    symbol='circle',
                    color='#1e1ecc',
                    opacity=1,
                    line=dict(
                        width=1,
                        color='#fce702'
                    )
                )
            ),
            go.Scatter3d(
                x=x_lines,
                y=y_lines,
                z=z_lines,
                hoverinfo='text',  # Hides the x,y,z values being shown on hover-over
                hovertext=dff['OrigName'] + ' to ' + dff['DestName'],
                mode='lines',
                name='lines',
                line=dict(
                    dash='solid',
                    color='#3b604e',
                    width=2
                )
            )
        ],
        layout=go.Layout(
            title='Hover over a line to see the flight route',
            hovermode='closest',
            width=800,
            height=800,
            uirevision='same_all_the_time',
            scene=dict(
                xaxis=dict(
                    range=[-90, 90],
                    title='Latitude',
                    titlefont_color='#056b51'
                ),
                yaxis=dict(
                    range=[180, -180],
                    title='Longitude',
                    titlefont_color='#056b51'
                ),
                zaxis=dict(
                    range=[1, 0],
                    title='',
                    showticklabels=False
                ),
                camera=dict(
                    up=dict(x=1, y=0, z=0),
                    center=dict(x=0, y=0, z=0),
                    eye=dict(x=0.1, y=2, z=1.5)
                )
            ),
            font=dict(
                family='Garamond EB',
                size=14,
                color='#60647a'
            )
        )
    )


if __name__ == '__main__':
    app.run_server(debug=True)
