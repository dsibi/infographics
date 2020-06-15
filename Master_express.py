import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import os

if not os.path.exists("images"):
    os.mkdir("images")

df = pd.read_csv('C:/Users/dsibi/Google Диск/Edu/Python/Meteors/data/MeteorStrikesDataSet1.csv')
df.dropna(inplace=True)
# print(df.columns)
df = df.astype({"year": int})
df['mass_t']=df['mass_g']/1000000
df['bins'] = pd.cut(df['year'], [-1000, 1810, 1880, 1950, 3000],
                    labels=['till 1810', '1811-1880', '1881-1950', 'more than 1950'])
order = ['till 1810', '1811-1880', '1881-1950', 'more than 1950']
df = df.set_index('bins')
df_ordered = df.T[order].T.reset_index()
df_ordered = df_ordered.astype({"mass_g": int})
# print(df_ordered)
df_ordered_labels = df_ordered.sort_values(by=['mass_g'], ascending=False).reset_index()
df_ordered_labels = df_ordered_labels[['place', 'mass_g', 'longitude', 'latitude']]
df_ordered_labels = df_ordered_labels[:10]
# print(df_ordered_labels)

fig=px.scatter_geo(df_ordered,lon='longitude', lat='latitude',color='bins',
                   color_discrete_sequence=px.colors.qualitative.Set1,
                   hover_name="place",
                   size='mass_g',opacity=0.7,text='mass_g',
                   projection="equirectangular",size_max=35,
                   # animation_frame='year',
                   hover_data={"longitude": False,
                                 "latitude": False,
                                 "mass_g": False,
                               "year": True,
                               "bins": False,
                               "mass_t": ":.1f"}
                   )

for data in fig.data:
    template = data.hovertemplate
    template = template.replace("<b>", "<b>")\
                       .replace("year=", "Year: ")\
                       .replace("mass_t=", "Mass (tonns): ")
    data.hovertemplate = template

fig.update_layout(title_text='Meteors strike',
                  showlegend=True, legend_title_text='Range Years',
                  geo=dict(scope='world',
                           landcolor='rgb(0, 0, 0)',
                           bgcolor='rgb(0, 0, 0)',
                           lakecolor='rgb(0, 0, 0)',
                           showocean=False,
                           showcountries=True,
                           countrywidth=0.3)
                  )

fig.update_traces(marker=dict(symbol='circle',
                              line=dict(
                                  color='white',
                                  width=0
                              )))

fig.add_trace(go.Scattergeo(lon=df_ordered_labels["longitude"],
              lat=df_ordered_labels["latitude"],
              text=df_ordered_labels["place"],
              textposition="middle right",
              mode='text',
                            textfont=dict(
                                # family="recto",
                                          size=12,
                                          color="white"),
              showlegend=False,
              texttemplate="       %{text}",
                            hoverinfo='skip',
                           ))

fig.show()
# fig.write_image("images/fig.svg")