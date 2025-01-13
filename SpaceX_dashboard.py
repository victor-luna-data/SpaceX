from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv')

app = Dash()
app.layout = [
    html.Div([
        html.H1('SpaceX Launch Records Dashboard', style={'textAlign':'center','color':'#000003','fontsize':24}),
        dcc.Dropdown(id='site-dropdown',
                     options=[{'label':i,'value':i} for i in df['Launch Site'].unique()] +[{'label':'All sites','value':'ALL'}],
                     value='ALL',
                     placeholder='Select a Launch site here',
                     searchable=True),
        dcc.Graph(id='success-pie-chart'),
        html.H4('Payload Mass (kg)'),
        dcc.RangeSlider(id='payload-slicer',
                        min=0,
                        max=10000,
                        step=1000,
                        value=[0,10000]),
        dcc.Graph(id='success-payload-scatter-chart')
    ])
]

@app.callback(Output(component_id='success-pie-chart',component_property='figure'),
              Input(component_id='site-dropdown',component_property='value'))
def pie_chart(site):
    if site == 'ALL':
        group = df.groupby(by=['Launch Site'],as_index=False).agg({'class':'sum'})
        fig = px.pie(group,values='class',names='Launch Site',title='Total success launches')
        return fig
    else:
        group = df[df['Launch Site']==site].groupby(by=['class'], as_index=False).agg({'class':'count'})
        fig = px.pie(group,values='class',names=[1,0],title=f'Total success launches by {site}')
        return fig
    
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown',component_property='value'),
              Input(component_id='payload-slicer',component_property='value'))
def scatter(site,range):
    if site == 'ALL':
        df_filtered = df[(df['Payload Mass (kg)']>=range[0]) & (df['Payload Mass (kg)']<=range[1])]
        fig = px.scatter(df_filtered,x='Payload Mass (kg)', y='class',color='Booster Version Category')
    else:
        df_filtered = df[(df['Launch Site']==site) & (df['Payload Mass (kg)']>=range[0]) & (df['Payload Mass (kg)']<=range[1])]
        fig = px.scatter(df_filtered,x='Payload Mass (kg)', y='class',color='Booster Version Category')
    return fig


if __name__ == '__main__':
    app.run_server()