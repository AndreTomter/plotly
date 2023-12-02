import requests
import plotly.express as px

url = "https://dbh.hkdir.no/api/Tabeller/streamJsonData"
res = requests.get(url)

årstall=[2019,2020,2021,2022,2023]
query = {"encoding":"UTF-8","tabell_id":112,"api_versjon":1,"statuslinje":"N","begrensning":"10000","kodetekst":"J","desimal_separator":".",
"groupBy":["Institusjonskode", "Avdelingskode", "Årstall", "Semester", "Studieprogramkode","Nivåkode"],
"sortBy":["Institusjonskode", "Avdelingskode"],
"filter":[
   {
      "variabel": "Institusjonskode",
      "selection": {
         "filter": "like",
         "values": [
            "1120"
         ],
         "exclude": [
            ""
         ]
      }
   },
   {
      "variabel": "Avdelingskode",
      "selection": {
         "filter": "like",
         "values": [
            "210%"
         ],
         "exclude": [
            ""
         ]
      }
   },
   {
      "variabel": "Årstall",
      "selection": {
         "filter": "item",
         "values": 
            årstall
         ,
         "exclude": [
            ""
         ]
      }
   },
   {
      "variabel": "Semester",
      "selection": {
         "filter": "item",
         "values": [
            '3'
         ]
            
         ,
         "exclude": [
            ""
         ]
      }
   },
   {
      "variabel": "Nivåkode",
      "selection": {
         "filter": "item",
         "values": [
            'B3'
         ]
            
         ,
         "exclude": [
            ""
         ]
      }
   }
]} 

res = requests.post(url, json = query).json()
#print(res)

Studieprogramkode = []
for a in res:
    if a['Studieprogramkode'] not in Studieprogramkode:
        Studieprogramkode.append(a['Studieprogramkode']) 
    else:
        continue 
år =[]
for i in Studieprogramkode:
   år.append(årstall)

li = []
for i in Studieprogramkode:
    for a in årstall:
      dic = dict()
      dic['Studieprogramkode']=i
      dic['Årstall']=str(a)
      dic['Antall totalt']= ''
      li.append(dic)

liste = []
for sp in Studieprogramkode:
   temp = []
   for l in li:
      if sp == l['Studieprogramkode']:
         for r in res:
            if l['Studieprogramkode'] == r['Studieprogramkode'] and l['Årstall'] == str(r['Årstall']):
               l['Antall totalt']=r['Antall totalt']
         temp.append(l['Antall totalt'])
   liste.append(temp)

colors = [
'#1a2640',
'#1a2640',
'#cdab3f',
'#4ea0b7',
'#789a5b',
'#705686',
'#db3f3d',
'#640000',
'#5c86c5',
'#1a2640',
'#1a2640',
'#cdab3f',
'#4ea0b7',
'#789a5b',
'#705686',
'#db3f3d',
'#640000',
'#5c86c5'
]

fig = px.line(x=årstall, y=liste[0], )
nr=0
for n in liste:
   fig.add_scatter(x=årstall, y=n, name=Studieprogramkode[nr], line={'color': colors[nr], 'width':2}, marker={'color': colors[nr], 'size': 7})
   nr = nr + 1

fig.update_layout(
   showlegend= True,
   legend= {
    'x': 1,
    'y': 0.5
  },
   height= 600,
   width= 650,
   plot_bgcolor="white",
   xaxis = dict(
      tickmode = 'linear',
      title="",
      tick0 = 1,
      dtick = 1,
      fixedrange = True,
      showline= True,
      showgrid= False,
      showticklabels= True,
      linecolor= 'rgb(204,204,204)',
      linewidth= 1,
      ticks= 'outside',
      tickcolor= 'rgb(204,204,204)',
      tickwidth= 1,
      ticklen= 5,
      tickfont= {
         'family': 'Arial',
         'size': 12,
         'color': 'rgb(82, 82, 82)'
         }
    ),
   yaxis= dict(
      title="",
  	   fixedrange= True,
      showgrid= True,
      zeroline= False,
      showline= False,
      showticklabels= True
   ),
   autosize= False,
   margin= {
      'autoexpand': False,
      'l': 30,
      'r': 120,
      't': 5
  },
  annotations= [
    {
      'xref': 'paper',
      'yref': 'paper',
      'x': 0.0,
      'y': 0.05,
      'xanchor': 'left',
      'yanchor': 'bottom',
      'text': '',
      'font':{
        'family': 'Arial',
        'size': 30,
        'color': 'rgb(37,37,37)'
      },
      'showarrow': False
    }
  ]
)

# show the plot
fig.show()
