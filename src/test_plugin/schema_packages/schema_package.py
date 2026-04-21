
from nomad.config import config
from nomad.datamodel.data import EntryData,ArchiveSection
from nomad.metainfo import Quantity, SchemaPackage , Section , SubSection , MSection,SectionProxy

from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
import numpy as np

from nomad.datamodel.metainfo.plot import PlotSection, PlotlyFigure
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import os
import plotly.express as px
import pandas as pd

import matplotlib.pyplot as plt


#import test_plugin.parsers.graphs as graphs
configuration = config.get_plugin_entry_point(
    'test_plugin.schema_packages:schema_package_entry_point'
)

m_package = SchemaPackage()


def import_plot(x_data,y_data,x_label,y_label):
  df = pd.DataFrame({
        x_label: x_data,
        y_label: y_data
    })
  fig= px.line(df,x=x_label,y=y_label,title="test title")
  return (fig.to_html(full_html=False,include_plotlyjs=False))#wenn diese funktion nicht verwendet wird muss die plotly library andersow included werden

# data is a list of touple [(data,name,label),(data,name)]
def import_box_plot(data,x_label,y_label,include_plotlyjs_bool):
    tabular_data = {}
    shown = {"in": False, "out": False}
    fig = go.Figure()
    for (dataitem,var_name,label) in data:
      if label == "in":
        fig.add_trace(go.Box( y=list(dataitem),x=[var_name for i in range(0,len(dataitem))] ,quartilemethod="linear", name= "in",legendgroup=label,showlegend=not shown[label] , marker_color='darkblue'))
        shown[label] = True
      elif label =="out":
        fig.add_trace(go.Box( y=list(dataitem),x=[var_name for i in range(0,len(dataitem))] ,quartilemethod="linear", name= "out",legendgroup=label,showlegend=not shown[label],marker_color='indianred'))
        shown[label] = True
      tabular_data[var_name,label,"max"]=round(np.max(list(dataitem)),3)
      tabular_data[var_name,label,"min"]=round(np.min(list(dataitem)),3)
      tabular_data[var_name,label,"avg"]=round(np.average(list(dataitem)),3)

    fig.update_layout(
      yaxis=dict(
        title=dict(
          text= y_label
        )
      ),
      xaxis=dict(
        title=dict(
          text=x_label
        )
      ),
      boxmode='group'
    )

    table =f"""
<div style="align-self:center; width: 100%;"><table class="table"><thead>
    <tr >
      <th class="inactive-cell"></th>
      <th class="header-cell" style="border-top-left-radius:10px"  colspan="2">Anode</th>
      <th class="header-cell" colspan="2">Cathode</th>
      <th class="header-cell" style="border-top-right-radius:10px" colspan="2">Thermal</th>
    </tr></thead>
  <tbody>
    <tr class="table-second-header">
      <td class="empty-cell"></td>
      <td class="second-header-cell">in</td>
      <td class="second-header-cell">out</td>
      <td class="second-header-cell">in</td>
      <td class="second-header-cell">out</td>
      <td class="second-header-cell">in</td>
      <td class="second-header-cell">out</td>
    </tr>
    <tr>
      <td class="second-header-cell-left" style="border-top-left-radius:10px ;">min</td>
      <td class="active-cell">{tabular_data["Anode","in","min"]}</td>
      <td class="active-cell">{tabular_data["Anode","out","min"]}</td>
      <td class="active-cell">{tabular_data["Cathode","in","min"]}</td>
      <td class="active-cell">{tabular_data["Cathode","out","min"]}</td>
      <td class="active-cell">{tabular_data["Thermal","in","min"]}</td>
      <td class="active-cell">{tabular_data["Thermal","out","min"]}</td>
    </tr>
    <tr>
      <td class="second-header-cell-left">avg</td>
      <td class="active-cell">{tabular_data["Anode","in","avg"]}</td>
      <td class="active-cell">{tabular_data["Anode","out","avg"]}</td>
      <td class="active-cell">{tabular_data["Cathode","in","avg"]}</td>
      <td class="active-cell">{tabular_data["Cathode","out","avg"]}</td>
      <td class="active-cell">{tabular_data["Thermal","in","avg"]}</td>
      <td class="active-cell">{tabular_data["Thermal","out","avg"]}</td>
    </tr>
    <tr>
      <td class="second-header-cell-left" style="border-bottom-left-radius:10px ">max</td>
      <td class="active-cell">{tabular_data["Anode","in","max"]}</td>
      <td class="active-cell">{tabular_data["Anode","out","max"]}</td>
      <td class="active-cell">{tabular_data["Cathode","in","max"]}</td>
      <td class="active-cell">{tabular_data["Cathode","out","max"]}</td>
      <td class="active-cell">{tabular_data["Thermal","in","max"]}</td>
      <td class="active-cell">{tabular_data["Thermal","out","max"]}</td>
    </tr>
</tbody></table></div>"""
    return("""<div style="align-self:center; width: 70%;">""" + fig.to_html(full_html=False,include_plotlyjs=include_plotlyjs_bool)+"</div>"+"\n"+table)

def import_print_button():
  return ["""
  button.print-button {
  width: 100px;
  height: 100px;
}
span.print-icon, span.print-icon::before, span.print-icon::after, button.print-button:hover .print-icon::after {
  border: solid 4px #333;
}
span.print-icon::after {
  border-width: 2px;
}

button.print-button {
  position: relative;
  padding: 0;
  border: 0;

  border: none;
  background: transparent;
}

span.print-icon, span.print-icon::before, span.print-icon::after, button.print-button:hover .print-icon::after {
  box-sizing: border-box;
  background-color: #fff;
}

span.print-icon {
  position: relative;
  display: inline-block;
  padding: 0;
  margin-top: 20%;

  width: 60%;
  height: 35%;
  background: #fff;
  border-radius: 20% 20% 0 0;
}

span.print-icon::before {
  content: "";
  position: absolute;
  bottom: 100%;
  left: 12%;
  right: 12%;
  height: 110%;

  transition: height .2s .15s;
}

span.print-icon::after {
  content: "";
  position: absolute;
  top: 55%;
  left: 12%;
  right: 12%;
  height: 0%;
  background: #fff;
  background-repeat: no-repeat;
  background-size: 70% 90%;
  background-position: center;

}

button.print-button:hover {
  cursor: pointer;
}

button.print-button:hover .print-icon::before {
  height:0px;
  transition: height .2s;
}
  """ ,"""
  <div class="content">
<button href="#" id="print" class="print-button"><span class="print-icon"></span> <a href="#" id="print"></a></button>
  """
  ,"""
  <script>
  document.addEventListener("DOMContentLoaded", () => {
    let printLink = document.getElementById("print");
    let container = document.getElementById("container");

    printLink.addEventListener("click", event => {
        event.preventDefault();
        printLink.style.display = "none";
        window.print();
        printLink.style.display = "flex";
    }, false);
}, false);
</script>
  """]


class Ploted_values(PlotSection,ArchiveSection):
    data=Quantity(type=np.float64,shape =['*'])
    name=Quantity(type=  str)
    time=Quantity(type=np.float64,shape =['*'])


    def normalize(self, archive, logger):
      super(Ploted_values, self).normalize(archive, logger)
      if not hasattr(self, 'data') or self.data is None or len(self.data) == 0:
        return 0
        #self.append(self.generate_scan_plot())
      if not hasattr(self, 'time') or self.time is None or len(self.time)==0:
        fig = go.Figure()

        x = np.array(self.m_parent.m_parent.elapsed_time).flatten()
        y = np.array(self.data).flatten()

        fig.add_trace(go.Scattergl(
            x=x,
            y=y,
            mode="lines",

            line=dict(width=2),

            hovertemplate="x=%{x:.2f}<br>y=%{y:.2f}<extra></extra>"
        ))

        fig.update_xaxes(fixedrange=False)
        fig.update_yaxes(fixedrange=False)
        fig.update_layout(
            hovermode="closest",
            dragmode="zoom",
            title=""
        )

        fig.update_xaxes(
            rangeslider=dict(visible=False)
        )

        self.figures.append(
            PlotlyFigure(
                label="",
                figure=fig.to_plotly_json()
            )
        )

        #fig=px.line(x=self.m_parent.m_parent.elapsed_time, y=self.data, title="")
        #html =fig.to_html(include_plotlyjs="cdn")
        #self.figures.append(PlotlyFigure(label="",figure=html))
        #figure1= px.line(x=self.m_parent.m_parent.elapsed_time, y=self.data, title="",render_mode="svg")
        #self.figures.append(PlotlyFigure(label='figure', figure=figure1.to_plotly_json()))
      else:
        fig = go.Figure()

        x = np.array(self.time - self.m_parent.start_time).flatten()
        y = np.array(self.data).flatten()

        fig.add_trace(go.Scattergl(
            x=x,
            y=y,
            mode="lines",

            line=dict(width=2),

            hovertemplate="x=%{x:.2f}<br>y=%{y:.2f}<extra></extra>"
        ))

        fig.update_xaxes(fixedrange=False)
        fig.update_yaxes(fixedrange=False)
        fig.update_layout(
            hovermode="closest",
            dragmode="zoom",
            title=""
        )

        fig.update_xaxes(
            rangeslider=dict(visible=False)
        )

        self.figures.append(
            PlotlyFigure(
                label="",
                figure=fig.to_plotly_json()
            )
        )


        #figure1= px.line(x=self.time-self.m_parent.start_time, y=self.data, title="",render_mode="svg")
        #self.figures.append(PlotlyFigure(label='figure', figure=figure1.to_plotly_json()))
      #try:
      #  figure2 = go.Figure()
      #  figure2.add_trace(go.Box( y=self.data, quartilemethod="linear", name=  "" ))
      #  self.figures.append(PlotlyFigure(label="figure2",figure = figure2.to_plotly_json()))
      #except NameError:
      #    print("variable namme wasnt defined")


class MIOData(ArchiveSection):
  data=SubSection(section=SectionProxy("Ploted_values"), repeats = True)


class ACTIFData(ArchiveSection):
  #m_def=Section()
  data=SubSection(section=SectionProxy("Ploted_values"), repeats = True)


class ACTIF2Data(ArchiveSection):
  #m_def=Section()

  data=SubSection(section=SectionProxy("Ploted_values"), repeats = True)


class HP_CANData(ArchiveSection):
  #m_def=Section()
  data=SubSection(section=SectionProxy("Ploted_values"), repeats = True)

class Undefined_data(ArchiveSection):
  data=SubSection(section=SectionProxy("Ploted_values"), repeats = True)
  start_time=Quantity(type=np.float64)
  end_time=Quantity(type=np.float64)

class NomadCamelsDataHandler_data(ArchiveSection):
  data=SubSection(section=SectionProxy("Ploted_values"), repeats = True)
  start_time=Quantity(type=np.float64)
  end_time=Quantity(type=np.float64)

# Define your schema class
class NewSchemaPackage(ArchiveSection):
    #m_def=Section()
    #m_def = Section(label='New Schema Package')
    nomadcamelsdatahandler_data=SubSection(section=SectionProxy("NomadCamelsDataHandler_data"),repeats= False)
    undef_data=SubSection(section=SectionProxy("Undefined_data"), repeats =False)
    mio_data = SubSection(section=SectionProxy("MIOData"), repeats =False)
    actif_data= SubSection(section=SectionProxy("ACTIFData"), repeats = False)
    actif2_data= SubSection(section=SectionProxy("ACTIF2Data"),repeats = False)
    hp_can_data= SubSection(section=SectionProxy("HP_CANData"), repeats = False)
    file_name = Quantity(
      type = str
    )
    first_name = Quantity(
        type=str
    )
    last_name = Quantity(
        type= str
    )
    email =  Quantity(
        type = str
    )
    affiliation = Quantity(
        type = str
    )
  #class MeasurementInfo(MSection):
    measurement_comments = Quantity(
        type= str
    )
    measurement_description = Quantity(
        type = str
    )
    protocol_description = Quantity(
        type = str
    )
  #class TimeSeries(MSection)  :
    time = Quantity(
        type = np.float64,
        shape = ['*']
    )
    elapsed_time = Quantity(
        type=np.float64,
        shape = ['*']
    )
    date= Quantity(
      type=str,
    )
    results_pdf = Quantity(
        type=str,
        a_browser=dict(adaptor='RawFileAdaptor',render_value ='HtmlValue')
    )
    results_html = Quantity(
        type= str,
        a_browser=dict(render_value ='HtmlValue')
    )

    def get_data(self, name):
      # first source
      for x in getattr(self.mio_data, "data", []):
          if x.name == name:
              return x.data

      # fallback source
      for x in getattr(self.nomadcamelsdatahandler_data, "data", []):
          if x.name == name:
              return x.data

      return None

    def create_pdf(self):

        self.get_data("Fluids_Thermal_B_TT_03_Celsius")
        minimum = np.min(self.get_data("Fluids_Thermal_B_TT_03_Celsius"))
        maximum = np.max(self.get_data("Fluids_Thermal_B_TT_03_Celsius"))
        average =np.average(self.get_data("Fluids_Thermal_B_TT_03_Celsius"))
        mean = np.mean(self.get_data("Fluids_Thermal_B_TT_03_Celsius"))
        #avg_plot_style,avg_plot_script = import_avg_plot_basics()#graphs.
        #plot_style,plot_canvas,plot_script = import_graph_lib(list(self.elapsed_time),list(self.mio_data.Fluids_Thermal_B_TT_03_Celsius.data))#graphs.
        # data is a list of touple [(data,name,label),(data,name)]
        boxplot_temp_A = import_box_plot([
            (self.get_data("Fluids_Anode_A_TT_02_Celsius"), "Anode", "in"),
            (self.get_data("Fluids_Anode_A_TT_03_Celsius"), "Anode", "out"),
            (self.get_data("Fluids_Cathode_A_TT_10_Celsius"), "Cathode", "in"),
            (self.get_data("Fluids_Cathode_A_TT_11_Celsius"), "Cathode", "out"),
            (self.get_data("Fluids_Thermal_A_TT_03_Celsius"), "Thermal", "in"),
            (self.get_data("Fluids_Thermal_A_TT_04_Celsius"), "Thermal", "out"),
        ], " ", "Temp[C°]", False)


        boxplot_preassure_A = import_box_plot([
            (self.get_data("Fluids_Anode_A_PT_03_barG"), "Anode", "in"),
            (self.get_data("Fluids_Cathode_A_PT_05_barG"), "Cathode", "in"),
            (self.get_data("Fluids_Thermal_PT_03_A_barG"), "Thermal", "in"),
            (self.get_data("Fluids_Anode_A_PT_04_barG"), "Anode", "out"),
            (self.get_data("Fluids_Cathode_A_PT_06_barG"), "Cathode", "out"),
            (self.get_data("Fluids_Thermal_PT_04_A_barG"), "Thermal", "out"),
        ], " ", "Pressure[barg]", False)


        boxplot_temp_B = import_box_plot([
            (self.get_data("Fluids_Anode_B_TT_02_Celsius"), "Anode", "in"),
            (self.get_data("Fluids_Anode_B_TT_03_Celsius"), "Anode", "out"),
            (self.get_data("Fluids_Cathode_B_TT_10_Celsius"), "Cathode", "in"),
            (self.get_data("Fluids_Cathode_B_TT_11_Celsius"), "Cathode", "out"),
            (self.get_data("Fluids_Thermal_B_TT_03_Celsius"), "Thermal", "in"),
            (self.get_data("Fluids_Thermal_B_TT_04_Celsius"), "Thermal", "out"),
        ], " ", "Temp[C°]", False)


        boxplot_preassure_B = import_box_plot([
            (self.get_data("Fluids_Anode_B_PT_03_barG"), "Anode", "in"),
            (self.get_data("Fluids_Cathode_B_PT_05_barG"), "Cathode", "in"),
            (self.get_data("Fluids_Thermal_PT_03_B_barG"), "Thermal", "in"),
            (self.get_data("Fluids_Anode_B_PT_04_barG"), "Anode", "out"),
            (self.get_data("Fluids_Cathode_B_PT_06_barG"), "Cathode", "out"),
            (self.get_data("Fluids_Thermal_PT_04_B_barG"), "Thermal", "out"),
        ], " ", "Pressure[barg]", False)
        self.get_data("Fluids_Thermal_B_TT_03_Celsius")
        plot=import_plot(self.elapsed_time, self.get_data("Fluids_Thermal_B_TT_03_Celsius"), "elapsed time","Temp[°C]")
        print_style,print_button, print_script = import_print_button()#graphs.
        return f"""
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.plot.ly/plotly-3.1.0.min.js" charset="utf-8"></script>
    <style>
        @media print {{
            @page {{
                size: A4 portrait;
                margin: 0;
            }}

            * {{
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }}

            .page {{
                page-break-after: always;
            }}
        }}
        body {{
            font-family:'Courier New';
            margin: 0;
            padding: 0;
        }}

        .quick_event_bar{{
          display: flex;
            align-items: center;       /* vertically center */
            justify-content: space-between; /* space between title and button */
            padding: 0px 0px;

        }}
        .headline{{

            text-align: center;
        }}
        .print_button{{
            align-items: right;
            text-align: end;
            padding-right: 10px;
        }}

        .border {{
            margin-right: 10%;
            margin-left: 5%;
            padding-left:5%;
            padding-right:5%;
            padding-top:5px;
            padding-bottom: 5px;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
            background: #fff;
        }}
        .quick_info {{
          border-radius: 2px;
          margi  nomadcamelsdatahandler_data=schema.m_create(NomadCamelsDataHandler_data)n-left:5% ;
          margin-right:5% ;
          margin-bottom:10px ;
          display: grid;
          grid-template-columns: auto auto;
          border:2px solid black;
          grid-template-areas: "info1 info2";
        }}
        .info1 {{
          padding:10px;
          border-right:2px solid black;
        }}
        .info2 {{
          padding: 10px;
        }}
        h2 {{
          margin-left:5%;
          margin-top:5%;
        }}
        h1 {{
          page-break-before: always;
          margin-left:5%;
          padding-top:5%;
        }}
        .plotly-graph-div {{
          page-break-inside: avoid;
          break-inside: avoid;

        }}
        table {{
          border-spacing: 0px !important;
          margin: auto;
          text-align: center;
          page-break-inside: avoid;
          break-inside: avoid;

        }}
        th, td {{

          padding: 12px !important;
        }}
        .table{{
          margin-left: 13%;
          padding-top: 30px;
          margin-top: 5%;
          margin-bottom: 5%;
          width: 70%;
          text-align: left;
        }}
        .header-cell{{
          text-align: center;
          border-bottom:2px solid black !important;
          background-color: lightgray;
        }}
        .second-header-cell{{
          background-color: whitesmoke;

        }}
        .second-header-cell-left{{
          background-color: whitesmoke;
        }}
        .inactive-cell{{
          background-color: white;
          border:0px white;
        }}
        .active-cell{{

        }}
    </style>
    <style>
        button.print-button {{
  width: 100px;
  height: 100px;
}}
span.print-icon, span.print-icon::before, span.print-icon::after, button.print-button:hover .print-icon::after {{
  border: solid 4px #333;
}}
span.print-icon::after {{
  border-width: 2px;
}}

button.print-button {{
  position: relative;
  padding: 0;
  border: 0;

  border: none;
  background: transparent;
}}

span.print-icon, span.print-icon::before, span.print-icon::after, button.print-button:hover .print-icon::after {{
  box-sizing: border-box;
  background-color: #fff;
}}

span.print-icon {{
  position: relative;
  display: inline-block;
  padding: 0;
  margin-top: 20%;

  width: 60%;
  height: 35%;
  background: #fff;
  border-radius: 20% 20% 0 0;
}}

span.print-icon::before {{
  content: "";
  position: absolute;
  bottom: 100%;
  left: 12%;
  right: 12%;
  height: 110%;

  transition: height .2s .15s;
}}

span.print-icon::after {{
  content: "";
  position: absolute;
  top: 55%;
  left: 12%;
  right: 12%;
  height: 0%;
  background: #fff;
  background-repeat: no-repeat;
  background-size: 70% 90%;
  background-position: center;
  background-image: linear-gradient(
    to top,
    #fff 0, #fff 14%,
    #333 14%, #333 28%,
    #fff 28%, #fff 42%,
    #333 42%, #333 56%,
    #fff 56%, #fff 70%,
    #333 70%, #333 84%,
    #fff 84%, #fff 100%
  );

  transition: height .2s, border-width 0s .2s, width 0s .2s;
}}

button.print-button:hover {{
  cursor: pointer;
}}

button.print-button:hover .print-icon::before {{
  height:0px;
  transition: height .2s;
}}
button.print-button:hover .print-icon::after {{
  height:120%;
  transition: height .2s .15s, border-width 0s .16s;
}}

    </style>
</head>
<body>
<div class="quick_event_bar">
    <div class="headline"></div>
    <div class="headline">  <h1>Test Report</h1></div>
    <div class ="print_button"><button href="#" id="print" class="print-button"><span class="print-icon"> </span> <a href="#" id="print"></a></button></div>
</div>



<div class="quick_info">
  <div class="info1" >
    Researcher: {self.first_name} {self.last_name}
  </div>
  <div class="info2">
    Date: {self.date}
  </div>
</div>
<div class="quick_info">
  <div class="info1" >
    Email:{self.email}
  </div>
  <div class="info2">
    Institute: {self.affiliation}
  </div>
</div>
<h2>Protocol description:</h2>
<div class="border"><blockquote contenteditable="true"><p>{self.protocol_description}</p></blockquote></div>
<h2>Measurement description:</h2>
<div class="border"><blockquote contenteditable="true"><p>{self.measurement_description}</p></blockquote></div>
<h2>Measurement comments:</h2>
<div class="border"><blockquote contenteditable="true"><p>{self.measurement_comments}</p></blockquote></div>


<h1>Evaluation Stack A:</h1>

<p id="outline">{boxplot_temp_A}<br>{boxplot_preassure_A}</p>

<h1>Evaluation Stack B:</h1>

<p id="outline">{boxplot_temp_B}<br>{boxplot_preassure_B}</p>





<script>
    document.addEventListener("DOMContentLoaded", () => {{
      let printLink = document.getElementById("print");
      let container = document.getElementById("container");

      printLink.addEventListener("click", event => {{
          event.preventDefault();
          printLink.style.visibility = "hidden";
          window.print();
          printLink.style.visibility = "visible";
      }}, false);
  }}, false);
  </script>
</body>
</html>
"""

    def normalize(self, archive:'EntryArchive',logger:'BoundLogger')-> None:
        super(NewSchemaPackage,self).normalize(archive,logger)

        output=f"{self.file_name}.html"
        if any(x.name == "Fluids_Thermal_B_TT_03_Celsius" for x in self.mio_data.data) or any(x.name == "Fluids_Thermal_B_TT_03_Celsius" for x in self.nomadcamelsdatahandler_data.data):
            final_html = self.create_pdf()
            with archive.m_context.raw_file(output,'w') as file:
                file.write(final_html)
            self.results_html=str(final_html)