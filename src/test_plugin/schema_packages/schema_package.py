
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
        fig=px.line(x=self.m_parent.m_parent.elapsed_time, y=self.data, title="")
        html =fig.to_html(include_plotlyjs="cdn")
        self.figures.append(PlotlyFigure(label="",figure=html))
        #figure1= px.line(x=self.m_parent.m_parent.elapsed_time, y=self.data, title="",render_mode="svg")
        #self.figures.append(PlotlyFigure(label='figure', figure=figure1.to_plotly_json()))
      else:
        fig = go.Figure()

        x = np.array(self.time - self.m_parent.start_time).flatten()
        y = np.array(self.data).flatten()

        fig.add_trace(go.Scattergl(   # 👈 WebGL version (important!)
            x=x,
            y=y,
            mode="lines",             # 👈 remove markers (huge speedup)

            line=dict(width=2),

            # 👇 lightweight hover (NO big text list)
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
            rangeslider=dict(visible=False)   # 👈 REMOVE slider
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
  TV_01_A_PWM_pwmDutyCycle= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  TV_01_B_PWM_pwmDutyCycle= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  TV_02_A_PWM_doDiagnostics= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  TV_02_A_PWM_pwmDutyCycle= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  TV_02_B_PWM_pwmDutyCycle= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  TV_03_A_PWM_pwmDutyCycle= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  TV_03_B_PWM_pwmDutyCycle= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  TV_01_A_pos_viDiagnostics= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  TV_01_B_pos_viDiagnostics= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  TV_02_A_pos_viDiagnostics= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  TV_02_B_pos_viDiagnostics= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  TV_03_A_pos_viDiagnostics= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  TV_03_B_pos_viDiagnostics= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  AR_01_PWM_pwmDutyCycle= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Supply_Position_Sensors_TV_voDiagnostics= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  T_ambient= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  p_ambient= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  RoundTrip_in_diDiagnostics= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  T_ambient_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  p_ambient_barA= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Anode_A_PV_01_prct= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Anode_A_PC_01_pDiff= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Anode_A_PC_01_pDiff_ref= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Anode_B_PV_01_prct= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Anode_B_PC_01_pDiff= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Anode_B_PC_01_pDiff_ref= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Thermal_FLKS_01_freq_ref_Hz= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Thermal_FLKS_01_fan_prct= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Thermal_PV_01_prct= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Thermal_PV_02_prct= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Thermal_MV_01_ref_prct= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Thermal_MV_01_act_prct= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Thermal_CP_01_freq_ref_Hz= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Thermal_CP_01_freq_act_Hz= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Thermal_A_AV_01_ref_prct= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Thermal_A_AV_01_act_prct= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Thermal_B_AV_01_ref_prct= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Thermal_B_AV_01_act_prct= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Cathode_AR_01_prct= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Cathode_EH_01_Power_prct= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Cathode_EH_02_Power_prct= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Cathode_A_TV_01_pos_V= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Cathode_A_TV_01_pwmDutyCycle= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Cathode_A_TV_02_pos_V= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Cathode_A_TV_02_pwmDutyCycle= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Cathode_A_TV_03_pos_V= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Cathode_A_TV_03_pwmDutyCycle= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Cathode_B_TV_01_pos_V= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Cathode_B_TV_01_pwmDutyCycle= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Cathode_B_TV_02_pos_V= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Cathode_B_TV_02_pwmDutyCycle= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Cathode_B_TV_03_pos_V= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Cathode_B_TV_03_pwmDutyCycle= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Cathode_MFC_01_00_p_PSIA= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Cathode_MFC_01_00_T_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Cathode_MFC_01_00_Vflow_LPM= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Cathode_MFC_01_00_mflow_SLPM= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Cathode_MFC_01_00_ref_SLPM= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Actuators_Cathode_MFC_01_00_set_SLPM= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  ECAT_10301_moduleQuality= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  ECAT_10302_moduleQuality= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  ECAT_10303_moduleQuality= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  ECAT_1001_RX_Device_Readings_Gas_Index= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  ECAT_1001_RX_Command_Result_Last_Command_ID= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  ECAT_1001_RX_Command_Result_Last_Command_Status= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  ECAT_1001_TX_Setpoint_Setpoint= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  ECAT_1001_TX_Command_Request_Command_ID= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  ECAT_1001_TX_Command_Request_Command_Argument= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  ECAT_1002_RX_Device_Readings_Gas_Index= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  ECAT_1002_RX_Command_Result_Last_Command_ID= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  ECAT_1002_RX_Command_Result_Last_Command_Status= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  ECAT_1002_TX_Setpoint_Setpoint= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  ECAT_1002_TX_Command_Request_Command_ID= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  ECAT_1002_TX_Command_Request_Command_Argument= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  ECAT_1004_RX_Device_Readings_Gas_Index= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  ECAT_1004_RX_Command_Result_Last_Command_ID= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  ECAT_1004_RX_Command_Result_Last_Command_Status= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  ECAT_1004_TX_Setpoint_Setpoint= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  ECAT_1004_TX_Command_Request_Command_ID= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  ECAT_1004_TX_Command_Request_Command_Argument= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Cathode_PT_01_barG= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Cathode_PT_02_barG= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Cathode_PT_03_barG= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Cathode_TT_01_0_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Cathode_TT_05_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Cathode_TT_02_0_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Cathode_TT_06_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Cathode_TT_03_0_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Cathode_TT_07_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Cathode_TT_01_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Cathode_TT_02_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Cathode_TT_04_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Cathode_A_PT_04_barG= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Cathode_A_PT_05_barG= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Cathode_A_PT_06_barG= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Cathode_A_MFT_02_slpm= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Cathode_A_RHT_01_prctRH= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Cathode_A_TT_09_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Cathode_A_TT_08_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Cathode_A_TT_10_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Cathode_A_TT_11_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Cathode_A_TT_12_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Cathode_B_PT_04_barG= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Cathode_B_PT_05_barG= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Cathode_B_PT_06_barG= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Cathode_B_MFT_02_slpm= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Cathode_B_TT_08_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Cathode_B_TT_10_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Cathode_B_TT_11_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Cathode_B_TT_12_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Anode_PT_01_barG= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Anode_TT_01_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Anode_A_PT_03_barG= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Anode_A_PT_04_barG= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Anode_A_TT_02_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Anode_A_TT_03_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Anode_B_PT_03_barG= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Anode_B_PT_04_barG= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Anode_B_TT_02_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Anode_B_TT_03_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Anode_MFT_01_A_p_PSIA= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Anode_MFT_01_A_T_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Anode_MFT_01_A_Vflow_LPM= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Anode_MFT_01_A_mflow_SLPM= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Anode_MFT_01_A_mTotal_SL= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Anode_MFT_01_B_p_PSIA= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Anode_MFT_01_B_T_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Anode_MFT_01_B_Vflow_LPM= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Anode_MFT_01_B_mflow_SLPM= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Anode_MFT_01_B_mTotal_SL= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Thermal_PT_01_barG= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Thermal_PT_02_barG= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Thermal_PT_03_A_barG= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Thermal_PT_03_B_barG= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Thermal_PT_04_A_barG= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Thermal_PT_04_B_barG= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Thermal_PT_05_barG= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Thermal_PT_06_barG= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Thermal_MFT_01_02_lpm= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Thermal_MFT_02_lpm= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Thermal_TT_01_01_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Thermal_TT_03_02_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Thermal_TT_01_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Thermal_TT_05_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Thermal_TT_02_01_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Thermal_TT_04_02_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Thermal_TT_06_01_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Thermal_TT_08_02_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Thermal_TT_07_01_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Thermal_TT_09_02_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Thermal_TT_11_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Thermal_TT_01_02_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Thermal_A_MFT_01_lpm= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Thermal_A_TT_03_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Thermal_A_TT_04_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Thermal_B_MFT_01_lpm= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Thermal_B_TT_03_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Fluids_Thermal_B_TT_04_Celsius= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  undefined_data=SubSection(section=SectionProxy("Ploted_values"), repeats = True)


class ACTIFData(ArchiveSection):
  #m_def=Section()
  Anode_GasSupply_state= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Anode_PC_01_A_cmd= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Anode_PC_01_A_state= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Anode_PC_01_B_cmd= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Anode_PC_01_B_state= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Anode_PV_01_A_cmd= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Anode_PV_01_A_state= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Anode_PV_01_B_cmd= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Anode_PV_01_B_state= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Cathode_AC_01_cmd= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Cathode_AC_01_state= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Cathode_EH_01_cmd= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Cathode_EH_01_state= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Cathode_EH_02_cmd= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Cathode_EH_02_state= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Cathode_MFC_01_00_cmd= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Cathode_MFC_01_00_state= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Cathode_TV_01_A_cmd= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Cathode_TV_01_A_state= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Cathode_TV_01_A_theta_prct= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Cathode_TV_01_B_cmd= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Cathode_TV_01_B_state= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Cathode_TV_01_B_theta_prct= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Cathode_TV_02_A_cmd= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Cathode_TV_02_A_state= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Cathode_TV_02_A_theta_prct= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Cathode_TV_02_B_cmd= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Cathode_TV_02_B_state= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Cathode_TV_02_B_theta_prct= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Cathode_TV_03_A_cmd= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Cathode_TV_03_A_state= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Cathode_TV_03_A_theta_prct= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Cathode_TV_03_B_cmd= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Cathode_TV_03_B_state= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Cathode_TV_03_B_theta_prct= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Thermal_AV_01_A_cmd= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Thermal_AV_01_A_state= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Thermal_AV_01_B_cmd= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Thermal_AV_01_B_state= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Thermal_CP_01_cmd_prct= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Thermal_CP_01_state= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Thermal_FLKS_01_CP_01_cmd_prct= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Thermal_FLKS_01_CP_01_state= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Thermal_FLKS_01_Fan_01_cmd= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Thermal_FLKS_01_Fan_01_state= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Thermal_MV_01_cmd= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Thermal_MV_01_state= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Thermal_PV_01_cmd= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Thermal_PV_01_state= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Thermal_PV_02_cmd= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Thermal_PV_02_state= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  undefined_data=SubSection(section=SectionProxy("Ploted_values"), repeats = True)


class ACTIF2Data(ArchiveSection):
  #m_def=Section()
  RH_01_A_state= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  RH_01_A_cmd= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  RH_01_B_state= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  RH_01_B_cmd= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  undefined_data=SubSection(section=SectionProxy("Ploted_values"), repeats = True)


class HP_CANData(ArchiveSection):
  #m_def=Section()
  Net_A_fbCAN_FSM_iStep= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Net_A_RH01_actValues_current_act_A= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Net_A_RH01_actValues_power_act_W= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Net_A_RH01_actValues_speed_act_rpm= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Net_A_RH01_actValues_T_circuit_C= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Net_A_RH01_actValues_voltage_act_V= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Net_A_RH01_cmd_mDot_cmd_kgph= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Net_A_RH01_cmd_speed_cmd_rpm= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Net_B_fbCAN_FSM_iStep= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Net_B_RH01_actValues_current_act_A= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Net_B_RH01_actValues_power_act_W= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Net_B_RH01_actValues_speed_act_rpm= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Net_B_RH01_actValues_T_circuit_C= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Net_B_RH01_actValues_voltage_act_V= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Net_B_RH01_cmd_mDot_cmd_kgph= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  Net_B_RH01_cmd_speed_cmd_rpm= SubSection(section=SectionProxy("Ploted_values"), repeats = False)
  undefined_data=SubSection(section=SectionProxy("Ploted_values"), repeats = True)

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



    def create_pdf(self):


        minimum = np.min(self.mio_data.Fluids_Thermal_B_TT_03_Celsius.data)
        maximum = np.max(self.mio_data.Fluids_Thermal_B_TT_03_Celsius.data)
        average =np.average(self.mio_data.Fluids_Thermal_B_TT_03_Celsius.data)
        mean = np.mean(self.mio_data.Fluids_Thermal_B_TT_03_Celsius.data)
        #avg_plot_style,avg_plot_script = import_avg_plot_basics()#graphs.
        #plot_style,plot_canvas,plot_script = import_graph_lib(list(self.elapsed_time),list(self.mio_data.Fluids_Thermal_B_TT_03_Celsius.data))#graphs.
        # data is a list of touple [(data,name,label),(data,name)]
        boxplot_temp_A=import_box_plot([(self.mio_data.Fluids_Anode_A_TT_02_Celsius.data,"Anode","in"),(self.mio_data.Fluids_Anode_A_TT_03_Celsius.data,"Anode","out"),(self.mio_data.Fluids_Cathode_A_TT_10_Celsius.data,"Cathode","in"),(self.mio_data.Fluids_Cathode_A_TT_11_Celsius.data,"Cathode","out"),(self.mio_data.Fluids_Thermal_A_TT_03_Celsius.data,"Thermal","in"),(self.mio_data.Fluids_Thermal_A_TT_04_Celsius.data,"Thermal","out")]," ","Temp[C°]",False)
        boxplot_preassure_A=import_box_plot([(self.mio_data.Fluids_Anode_A_PT_03_barG.data,"Anode","in"),(self.mio_data.Fluids_Cathode_A_PT_05_barG.data,"Cathode","in"),(self.mio_data.Fluids_Thermal_PT_03_A_barG.data,"Thermal","in"),(self.mio_data.Fluids_Anode_A_PT_04_barG.data,"Anode","out"),(self.mio_data.Fluids_Cathode_A_PT_06_barG.data,"Cathode","out"),(self.mio_data.Fluids_Thermal_PT_04_A_barG.data,"Thermal","out")]," ","Pressure[barg]",False)
        boxplot_temp_B=import_box_plot([(self.mio_data.Fluids_Anode_B_TT_02_Celsius.data,"Anode","in"),(self.mio_data.Fluids_Anode_B_TT_03_Celsius.data,"Anode","out"),(self.mio_data.Fluids_Cathode_B_TT_10_Celsius.data,"Cathode","in"),(self.mio_data.Fluids_Cathode_B_TT_11_Celsius.data,"Cathode","out"),(self.mio_data.Fluids_Thermal_B_TT_03_Celsius.data,"Thermal","in"),(self.mio_data.Fluids_Thermal_B_TT_04_Celsius.data,"Thermal","out")]," ","Temp[C°]",False)
        boxplot_preassure_B=import_box_plot([(self.mio_data.Fluids_Anode_B_PT_03_barG.data,"Anode","in"),(self.mio_data.Fluids_Cathode_B_PT_05_barG.data,"Cathode","in"),(self.mio_data.Fluids_Thermal_PT_03_B_barG.data,"Thermal","in"),(self.mio_data.Fluids_Anode_B_PT_04_barG.data,"Anode","out"),(self.mio_data.Fluids_Cathode_B_PT_06_barG.data,"Cathode","out"),(self.mio_data.Fluids_Thermal_PT_04_B_barG.data,"Thermal","out")]," ","Pressure[barg]",False)
        plot=import_plot(self.elapsed_time, self.mio_data.Fluids_Thermal_B_TT_03_Celsius.data, "elapsed time","Temp[°C]")
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
          margin-left:5% ;
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
        if self.mio_data.Fluids_Thermal_B_TT_03_Celsius is not None:
            final_html = self.create_pdf()
            with archive.m_context.raw_file(output,'w') as file:
                file.write(final_html)
            self.results_html=str(final_html)