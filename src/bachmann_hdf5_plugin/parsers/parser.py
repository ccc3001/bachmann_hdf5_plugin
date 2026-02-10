import h5py
from datetime import datetime 
from typing import (
    TYPE_CHECKING,
)
import os

from nomad.datamodel.datamodel import EntryArchive
from structlog.stdlib import (
        BoundLogger,
    )

from nomad.config import config
from nomad.datamodel.metainfo.workflow import Workflow
from nomad.parsing.parser import MatchingParser
from test_plugin.schema_packages.schema_package import NewSchemaPackage,MIOData,ACTIF2Data,ACTIFData,HP_CANData,Ploted_values,Undefined_data

configuration = config.get_plugin_entry_point(
    'test_plugin.parsers:parser_entry_point'
)


class NewParser(MatchingParser):
    def set_attribute(self,value,_object,_atribute,keys):
        for key in keys[:-1]:
            value=value[key]

        if keys[-1] in list(value.keys()):
            value=value[keys[-1]][()]
            if isinstance(value, bytes):
                setattr(_object,_atribute,value.decode('utf-8'))
            else:
                setattr(_object,_atribute,value)
        else:
            setattr(_object,_atribute,None)
    def parse(
        self,
        mainfile: str,
        archive: 'EntryArchive',
        logger: 'BoundLogger',
        #child_archives: dict[str, 'EntryArchive'] = None,
    ) -> None:
        schema= NewSchemaPackage()
        logger.info('NewParser.parse', parameter=configuration.parameter)
        




        
        mio_data= schema.m_create(MIOData)#MIOData()
        actif2_data= schema.m_create(ACTIF2Data)#ACTIF2Data()
        actif_data= schema.m_create(ACTIFData)#ACTIFData()
        hp_can_data= schema.m_create(HP_CANData)#HP_CANData()
        schema.file_name = str(os.path.splitext(os.path.basename(str(mainfile)))[0])
        schema.date = str(datetime.today().strftime('%Y-%m-%d'))
        undef_data=schema.m_create(Undefined_data)
        with h5py.File(mainfile, "r") as f:
            
            
            
            if len(f.keys())==1:
                CAMELS_entry=list(f.keys())[0]
            else:
                CAMELS_entry=list(f.keys())[0]
            
            
            
            


            if "measurement_comments" in f[CAMELS_entry]["measurement_details"]:
                if str(f[CAMELS_entry]["measurement_details"]["measurement_comments"][()]) != "b''":
                    self.set_attribute(f,schema, "measurement_comments" , [CAMELS_entry, "measurement_details", "measurement_comments"])
            if "measurement_description" in f[CAMELS_entry]["measurement_details"]:
                if str(f[CAMELS_entry]["measurement_details"]["measurement_description"][()]) != "b''":
                    self.set_attribute(f,schema,"measurement_description",[CAMELS_entry,"measurement_details","measurement_description"])
            if "protocol_description" in f[CAMELS_entry]["measurement_details"]:
                if str(f[CAMELS_entry]["measurement_details"]["protocol_description"][()]) != "b''":
                    self.set_attribute(f,schema,"protocol_description",[CAMELS_entry,"measurement_details","protocol_description"])
            if "first_name" in f[CAMELS_entry]["user"]:
                if str(f[CAMELS_entry]["user"]["first_name"][()]) != "b''":
                    self.set_attribute(f,schema,"first_name",[CAMELS_entry,"user","first_name"])
            if "last_name" in f[CAMELS_entry]["user"]:
                if str(f[CAMELS_entry]["user"]["last_name"][()]) != "b''":
                    self.set_attribute(f,schema,"last_name",[CAMELS_entry,"user","last_name"])
            if "email" in f[CAMELS_entry]["user"]:
                if str(f[CAMELS_entry]["user"]["email"][()]) != "b''":
                    self.set_attribute(f,schema,"email",[CAMELS_entry,"user","email"])
            if "affiliation" in f[CAMELS_entry]["user"]:
                if str(f[CAMELS_entry]["user"]["affiliation"][()]) != "b''":
                    self.set_attribute(f,schema,"affiliation",[CAMELS_entry,"user","affiliation"])
            self.set_attribute(f,schema,"time",[CAMELS_entry,"data","time"])
            self.set_attribute(f,actif_data,"time",[CAMELS_entry,"data","time"])
            self.set_attribute(f,schema,"elapsed_time",[CAMELS_entry,"data","ElapsedTime"])
            
            opc_ua_instrument_name=None
            for key in f[CAMELS_entry]["instruments"]:
                if "opc" and "ua" in key:
                    opc_ua_instrument_name=str(key)
            
            for key in f[CAMELS_entry]["data"]:
                if opc_ua_instrument_name and key.startswith(opc_ua_instrument_name):
                    if key.startswith(opc_ua_instrument_name+"_MIO"):
                        if opc_ua_instrument_name +"_MIO_TV_01_A_PWM_pwmDutyCycle"== key:
                            TV_01_A_PWM_pwmDutyCycle=mio_data.m_create(Ploted_values,MIOData.TV_01_A_PWM_pwmDutyCycle)
                            self.set_attribute(f,TV_01_A_PWM_pwmDutyCycle,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_TV_01_A_PWM_pwmDutyCycle"])
                        elif opc_ua_instrument_name + "_MIO_TV_01_B_PWM_pwmDutyCycle"== key:
                            TV_01_B_PWM_pwmDutyCycle=mio_data.m_create(Ploted_values,MIOData.TV_01_B_PWM_pwmDutyCycle)
                            self.set_attribute(f,TV_01_B_PWM_pwmDutyCycle,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_TV_01_B_PWM_pwmDutyCycle"])
                        elif opc_ua_instrument_name + "_MIO_TV_02_A_PWM_doDiagnostics"== key:
                            TV_02_A_PWM_doDiagnostics=mio_data.m_create(Ploted_values,MIOData.TV_02_A_PWM_doDiagnostics)
                            self.set_attribute(f,TV_02_A_PWM_doDiagnostics,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_TV_02_A_PWM_doDiagnostics"])
                        elif opc_ua_instrument_name + "_MIO_TV_02_A_PWM_pwmDutyCycle"== key:
                            TV_02_A_PWM_pwmDutyCycle=mio_data.m_create(Ploted_values,MIOData.TV_02_A_PWM_pwmDutyCycle)
                            self.set_attribute(f,TV_02_A_PWM_pwmDutyCycle,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_TV_02_A_PWM_pwmDutyCycle"])
                        elif opc_ua_instrument_name + "_MIO_TV_02_B_PWM_pwmDutyCycle"== key:
                            TV_02_B_PWM_pwmDutyCycle=mio_data.m_create(Ploted_values,MIOData.TV_02_B_PWM_pwmDutyCycle)
                            self.set_attribute(f,TV_02_B_PWM_pwmDutyCycle,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_TV_02_B_PWM_pwmDutyCycle"])
                        elif opc_ua_instrument_name + "_MIO_TV_03_A_PWM_pwmDutyCycle"== key:
                            TV_03_A_PWM_pwmDutyCycle=mio_data.m_create(Ploted_values,MIOData.TV_03_A_PWM_pwmDutyCycle)
                            self.set_attribute(f,TV_03_A_PWM_pwmDutyCycle,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_TV_03_A_PWM_pwmDutyCycle"])
                        elif opc_ua_instrument_name + "_MIO_TV_03_B_PWM_pwmDutyCycle"== key:
                            TV_03_B_PWM_pwmDutyCycle=mio_data.m_create(Ploted_values,MIOData.TV_03_B_PWM_pwmDutyCycle)
                            self.set_attribute(f,TV_03_B_PWM_pwmDutyCycle,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_TV_03_B_PWM_pwmDutyCycle"])
                        elif opc_ua_instrument_name + "_MIO_TV_01_A_pos_viDiagnostics"== key:
                            TV_01_A_pos_viDiagnostics=mio_data.m_create(Ploted_values,MIOData.TV_01_A_pos_viDiagnostics)
                            self.set_attribute(f,TV_01_A_pos_viDiagnostics,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_TV_01_A_pos_viDiagnostics"])
                        elif opc_ua_instrument_name + "_MIO_TV_01_B_pos_viDiagnostics"== key:
                            TV_01_B_pos_viDiagnostics=mio_data.m_create(Ploted_values,MIOData.TV_01_B_pos_viDiagnostics)
                            self.set_attribute(f,TV_01_B_pos_viDiagnostics,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_TV_01_B_pos_viDiagnostics"])
                        elif opc_ua_instrument_name + "_MIO_TV_02_A_pos_viDiagnostics"== key:
                            TV_02_A_pos_viDiagnostics=mio_data.m_create(Ploted_values,MIOData.TV_02_A_pos_viDiagnostics)
                            self.set_attribute(f,TV_02_A_pos_viDiagnostics,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_TV_02_A_pos_viDiagnostics"])
                        elif opc_ua_instrument_name + "_MIO_TV_02_B_pos_viDiagnostics"== key:
                            TV_02_B_pos_viDiagnostics=mio_data.m_create(Ploted_values,MIOData.TV_02_B_pos_viDiagnostics)
                            self.set_attribute(f,TV_02_B_pos_viDiagnostics,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_TV_02_B_pos_viDiagnostics"])
                        elif opc_ua_instrument_name + "_MIO_TV_03_A_pos_viDiagnostics"== key:
                            TV_03_A_pos_viDiagnostics=mio_data.m_create(Ploted_values,MIOData.TV_03_A_pos_viDiagnostics)
                            self.set_attribute(f,TV_03_A_pos_viDiagnostics,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_TV_03_A_pos_viDiagnostics"])
                        elif opc_ua_instrument_name + "_MIO_TV_03_B_pos_viDiagnostics"== key:
                            TV_03_B_pos_viDiagnostics=mio_data.m_create(Ploted_values,MIOData.TV_03_B_pos_viDiagnostics)
                            self.set_attribute(f,TV_03_B_pos_viDiagnostics,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_TV_03_B_pos_viDiagnostics"])
                        elif opc_ua_instrument_name + "_MIO_AR_01_PWM_pwmDutyCycle"== key:
                            AR_01_PWM_pwmDutyCycle=mio_data.m_create(Ploted_values,MIOData.AR_01_PWM_pwmDutyCycle)
                            self.set_attribute(f,AR_01_PWM_pwmDutyCycle,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_AR_01_PWM_pwmDutyCycle"])
                        elif opc_ua_instrument_name + "_MIO_Supply_Position_Sensors_TV_voDiagnostics"== key:
                            Supply_Position_Sensors_TV_voDiagnostics=mio_data.m_create(Ploted_values,MIOData.Supply_Position_Sensors_TV_voDiagnostics)
                            self.set_attribute(f,Supply_Position_Sensors_TV_voDiagnostics,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Supply_Position_Sensors_TV_voDiagnostics"])
                        elif opc_ua_instrument_name + "_MIO_T_ambient"== key:
                            T_ambient=mio_data.m_create(Ploted_values,MIOData.T_ambient)
                            self.set_attribute(f,T_ambient,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_T_ambient"])
                        elif opc_ua_instrument_name + "_MIO_p_ambient"== key:
                            p_ambient=mio_data.m_create(Ploted_values,MIOData.p_ambient)
                            self.set_attribute(f,p_ambient,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_p_ambient"])
                        elif opc_ua_instrument_name + "_MIO_RoundTrip_in_diDiagnostics"== key:
                            RoundTrip_in_diDiagnostics=mio_data.m_create(Ploted_values,MIOData.RoundTrip_in_diDiagnostics)
                            self.set_attribute(f,RoundTrip_in_diDiagnostics,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_RoundTrip_in_diDiagnostics"])
                        elif opc_ua_instrument_name + "_MIO_T_ambient_Celsius"== key:
                            T_ambient_Celsius=mio_data.m_create(Ploted_values,MIOData.T_ambient_Celsius)
                            self.set_attribute(f,T_ambient_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_T_ambient_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_p_ambient_barA"== key:
                            p_ambient_barA=mio_data.m_create(Ploted_values,MIOData.p_ambient_barA)
                            self.set_attribute(f,p_ambient_barA,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_p_ambient_barA"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Anode_A_PV_01_prct"== key:
                            Actuators_Anode_A_PV_01_prct=mio_data.m_create(Ploted_values,MIOData.Actuators_Anode_A_PV_01_prct)
                            self.set_attribute(f,Actuators_Anode_A_PV_01_prct,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Anode_A_PV_01_prct"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Anode_A_PC_01_pDiff"== key:
                            Actuators_Anode_A_PC_01_pDiff=mio_data.m_create(Ploted_values,MIOData.Actuators_Anode_A_PC_01_pDiff)
                            self.set_attribute(f,Actuators_Anode_A_PC_01_pDiff,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Anode_A_PC_01_pDiff"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Anode_A_PC_01_pDiff_ref"== key:
                            Actuators_Anode_A_PC_01_pDiff_ref=mio_data.m_create(Ploted_values,MIOData.Actuators_Anode_A_PC_01_pDiff_ref)
                            self.set_attribute(f,Actuators_Anode_A_PC_01_pDiff_ref,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Anode_A_PC_01_pDiff_ref"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Anode_B_PV_01_prct"== key:
                            Actuators_Anode_B_PV_01_prct=mio_data.m_create(Ploted_values,MIOData.Actuators_Anode_B_PV_01_prct)
                            self.set_attribute(f,Actuators_Anode_B_PV_01_prct,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Anode_B_PV_01_prct"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Anode_B_PC_01_pDiff"== key:
                            Actuators_Anode_B_PC_01_pDiff=mio_data.m_create(Ploted_values,MIOData.Actuators_Anode_B_PC_01_pDiff)
                            self.set_attribute(f,Actuators_Anode_B_PC_01_pDiff,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Anode_B_PC_01_pDiff"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Anode_B_PC_01_pDiff_ref"== key:
                            Actuators_Anode_B_PC_01_pDiff_ref=mio_data.m_create(Ploted_values,MIOData.Actuators_Anode_B_PC_01_pDiff_ref)
                            self.set_attribute(f,Actuators_Anode_B_PC_01_pDiff_ref,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Anode_B_PC_01_pDiff_ref"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Thermal_FLKS_01_freq_ref_Hz"== key:
                            Actuators_Thermal_FLKS_01_freq_ref_Hz=mio_data.m_create(Ploted_values,MIOData.Actuators_Thermal_FLKS_01_freq_ref_Hz)
                            self.set_attribute(f,Actuators_Thermal_FLKS_01_freq_ref_Hz,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Thermal_FLKS_01_freq_ref_Hz"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Thermal_FLKS_01_fan_prct"== key:
                            Actuators_Thermal_FLKS_01_fan_prct=mio_data.m_create(Ploted_values,MIOData.Actuators_Thermal_FLKS_01_fan_prct)
                            self.set_attribute(f,Actuators_Thermal_FLKS_01_fan_prct,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Thermal_FLKS_01_fan_prct"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Thermal_PV_01_prct"== key:
                            Actuators_Thermal_PV_01_prct=mio_data.m_create(Ploted_values,MIOData.Actuators_Thermal_PV_01_prct)
                            self.set_attribute(f,Actuators_Thermal_PV_01_prct,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Thermal_PV_01_prct"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Thermal_PV_02_prct"== key:
                            Actuators_Thermal_PV_02_prct=mio_data.m_create(Ploted_values,MIOData.Actuators_Thermal_PV_02_prct)
                            self.set_attribute(f,Actuators_Thermal_PV_02_prct,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Thermal_PV_02_prct"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Thermal_MV_01_ref_prct"== key:
                            Actuators_Thermal_MV_01_ref_prct=mio_data.m_create(Ploted_values,MIOData.Actuators_Thermal_MV_01_ref_prct)
                            self.set_attribute(f,Actuators_Thermal_MV_01_ref_prct,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Thermal_MV_01_ref_prct"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Thermal_MV_01_act_prct"== key:
                            Actuators_Thermal_MV_01_act_prct=mio_data.m_create(Ploted_values,MIOData.Actuators_Thermal_MV_01_act_prct)
                            self.set_attribute(f,Actuators_Thermal_MV_01_act_prct,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Thermal_MV_01_act_prct"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Thermal_CP_01_freq_ref_Hz"== key:
                            Actuators_Thermal_CP_01_freq_ref_Hz=mio_data.m_create(Ploted_values,MIOData.Actuators_Thermal_CP_01_freq_ref_Hz)
                            self.set_attribute(f,Actuators_Thermal_CP_01_freq_ref_Hz,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Thermal_CP_01_freq_ref_Hz"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Thermal_CP_01_freq_act_Hz"== key:
                            Actuators_Thermal_CP_01_freq_act_Hz=mio_data.m_create(Ploted_values,MIOData.Actuators_Thermal_CP_01_freq_act_Hz)
                            self.set_attribute(f,Actuators_Thermal_CP_01_freq_act_Hz,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Thermal_CP_01_freq_act_Hz"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Thermal_A_AV_01_ref_prct"== key:
                            Actuators_Thermal_A_AV_01_ref_prct=mio_data.m_create(Ploted_values,MIOData.Actuators_Thermal_A_AV_01_ref_prct)
                            self.set_attribute(f,Actuators_Thermal_A_AV_01_ref_prct,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Thermal_A_AV_01_ref_prct"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Thermal_A_AV_01_act_prct"== key:
                            Actuators_Thermal_A_AV_01_act_prct=mio_data.m_create(Ploted_values,MIOData.Actuators_Thermal_A_AV_01_act_prct)
                            self.set_attribute(f,Actuators_Thermal_A_AV_01_act_prct,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Thermal_A_AV_01_act_prct"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Thermal_B_AV_01_ref_prct"== key:
                            Actuators_Thermal_B_AV_01_ref_prct=mio_data.m_create(Ploted_values,MIOData.Actuators_Thermal_B_AV_01_ref_prct)
                            self.set_attribute(f,Actuators_Thermal_B_AV_01_ref_prct,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Thermal_B_AV_01_ref_prct"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Thermal_B_AV_01_act_prct"== key:
                            Actuators_Thermal_B_AV_01_act_prct=mio_data.m_create(Ploted_values,MIOData.Actuators_Thermal_B_AV_01_act_prct)
                            self.set_attribute(f,Actuators_Thermal_B_AV_01_act_prct,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Thermal_B_AV_01_act_prct"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Cathode_AR_01_prct"== key:
                            Actuators_Cathode_AR_01_prct=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_AR_01_prct)
                            self.set_attribute(f,Actuators_Cathode_AR_01_prct,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Cathode_AR_01_prct"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Cathode_EH_01_Power_prct"== key:
                            Actuators_Cathode_EH_01_Power_prct=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_EH_01_Power_prct)
                            self.set_attribute(f,Actuators_Cathode_EH_01_Power_prct,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Cathode_EH_01_Power_prct"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Cathode_EH_02_Power_prct"== key:
                            Actuators_Cathode_EH_02_Power_prct=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_EH_02_Power_prct)
                            self.set_attribute(f,Actuators_Cathode_EH_02_Power_prct,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Cathode_EH_02_Power_prct"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Cathode_A_TV_01_pos_V"== key:
                            Actuators_Cathode_A_TV_01_pos_V=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_A_TV_01_pos_V)
                            self.set_attribute(f,Actuators_Cathode_A_TV_01_pos_V,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Cathode_A_TV_01_pos_V"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Cathode_A_TV_01_pwmDutyCycle"== key:
                            Actuators_Cathode_A_TV_01_pwmDutyCycle=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_A_TV_01_pwmDutyCycle)
                            self.set_attribute(f,Actuators_Cathode_A_TV_01_pwmDutyCycle,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Cathode_A_TV_01_pwmDutyCycle"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Cathode_A_TV_02_pos_V"== key:
                            Actuators_Cathode_A_TV_02_pos_V=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_A_TV_02_pos_V)
                            self.set_attribute(f,Actuators_Cathode_A_TV_02_pos_V,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Cathode_A_TV_02_pos_V"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Cathode_A_TV_02_pwmDutyCycle"== key:
                            Actuators_Cathode_A_TV_02_pwmDutyCycle=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_A_TV_02_pwmDutyCycle)
                            self.set_attribute(f,Actuators_Cathode_A_TV_02_pwmDutyCycle,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Cathode_A_TV_02_pwmDutyCycle"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Cathode_A_TV_03_pos_V"== key:
                            Actuators_Cathode_A_TV_03_pos_V=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_A_TV_03_pos_V)
                            self.set_attribute(f,Actuators_Cathode_A_TV_03_pos_V,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Cathode_A_TV_03_pos_V"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Cathode_A_TV_03_pwmDutyCycle"== key:
                            Actuators_Cathode_A_TV_03_pwmDutyCycle=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_A_TV_03_pwmDutyCycle)
                            self.set_attribute(f,Actuators_Cathode_A_TV_03_pwmDutyCycle,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Cathode_A_TV_03_pwmDutyCycle"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Cathode_B_TV_01_pos_V"== key:
                            Actuators_Cathode_B_TV_01_pos_V=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_B_TV_01_pos_V)
                            self.set_attribute(f,Actuators_Cathode_B_TV_01_pos_V,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Cathode_B_TV_01_pos_V"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Cathode_B_TV_01_pwmDutyCycle"== key:
                            Actuators_Cathode_B_TV_01_pwmDutyCycle=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_B_TV_01_pwmDutyCycle)
                            self.set_attribute(f,Actuators_Cathode_B_TV_01_pwmDutyCycle,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Cathode_B_TV_01_pwmDutyCycle"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Cathode_B_TV_02_pos_V"== key:
                            Actuators_Cathode_B_TV_02_pos_V=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_B_TV_02_pos_V)
                            self.set_attribute(f,Actuators_Cathode_B_TV_02_pos_V,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Cathode_B_TV_02_pos_V"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Cathode_B_TV_02_pwmDutyCycle"== key:
                            Actuators_Cathode_B_TV_02_pwmDutyCycle=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_B_TV_02_pwmDutyCycle)
                            self.set_attribute(f,Actuators_Cathode_B_TV_02_pwmDutyCycle,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Cathode_B_TV_02_pwmDutyCycle"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Cathode_B_TV_03_pos_V"== key:
                            Actuators_Cathode_B_TV_03_pos_V=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_B_TV_03_pos_V)
                            self.set_attribute(f,Actuators_Cathode_B_TV_03_pos_V,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Cathode_B_TV_03_pos_V"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Cathode_B_TV_03_pwmDutyCycle"== key:
                            Actuators_Cathode_B_TV_03_pwmDutyCycle=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_B_TV_03_pwmDutyCycle)
                            self.set_attribute(f,Actuators_Cathode_B_TV_03_pwmDutyCycle,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Cathode_B_TV_03_pwmDutyCycle"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Cathode_MFC_01_00_p_PSIA"== key:
                            Actuators_Cathode_MFC_01_00_p_PSIA=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_MFC_01_00_p_PSIA)
                            self.set_attribute(f,Actuators_Cathode_MFC_01_00_p_PSIA,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Cathode_MFC_01_00_p_PSIA"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Cathode_MFC_01_00_T_Celsius"== key:
                            Actuators_Cathode_MFC_01_00_T_Celsius=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_MFC_01_00_T_Celsius)
                            self.set_attribute(f,Actuators_Cathode_MFC_01_00_T_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Cathode_MFC_01_00_T_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Cathode_MFC_01_00_Vflow_LPM"== key:
                            Actuators_Cathode_MFC_01_00_Vflow_LPM=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_MFC_01_00_Vflow_LPM)
                            self.set_attribute(f,Actuators_Cathode_MFC_01_00_Vflow_LPM,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Cathode_MFC_01_00_Vflow_LPM"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Cathode_MFC_01_00_mflow_SLPM"== key:
                            Actuators_Cathode_MFC_01_00_mflow_SLPM=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_MFC_01_00_mflow_SLPM)
                            self.set_attribute(f,Actuators_Cathode_MFC_01_00_mflow_SLPM,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Cathode_MFC_01_00_mflow_SLPM"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Cathode_MFC_01_00_ref_SLPM"== key:
                            Actuators_Cathode_MFC_01_00_ref_SLPM=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_MFC_01_00_ref_SLPM)
                            self.set_attribute(f,Actuators_Cathode_MFC_01_00_ref_SLPM,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Cathode_MFC_01_00_ref_SLPM"])
                        elif opc_ua_instrument_name + "_MIO_Actuators_Cathode_MFC_01_00_set_SLPM"== key:
                            Actuators_Cathode_MFC_01_00_set_SLPM=mio_data.m_create(Ploted_values,MIOData.Actuators_Cathode_MFC_01_00_set_SLPM)
                            self.set_attribute(f,Actuators_Cathode_MFC_01_00_set_SLPM,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Actuators_Cathode_MFC_01_00_set_SLPM"])
                        elif opc_ua_instrument_name + "_MIO_ECAT_10301_moduleQuality"== key:
                            ECAT_10301_moduleQuality=mio_data.m_create(Ploted_values,MIOData.ECAT_10301_moduleQuality)
                            self.set_attribute(f,ECAT_10301_moduleQuality,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_ECAT_10301_moduleQuality"])
                        elif opc_ua_instrument_name + "_MIO_ECAT_10302_moduleQuality"== key:
                            ECAT_10302_moduleQuality=mio_data.m_create(Ploted_values,MIOData.ECAT_10302_moduleQuality)
                            self.set_attribute(f,ECAT_10302_moduleQuality,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_ECAT_10302_moduleQuality"])
                        elif opc_ua_instrument_name + "_MIO_ECAT_10303_moduleQuality"== key:
                            ECAT_10303_moduleQuality=mio_data.m_create(Ploted_values,MIOData.ECAT_10303_moduleQuality)
                            self.set_attribute(f,ECAT_10303_moduleQuality,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_ECAT_10303_moduleQuality"])
                        elif opc_ua_instrument_name + "_MIO_ECAT_1001_RX_Device_Readings_Gas_Index"== key:
                            ECAT_1001_RX_Device_Readings_Gas_Index=mio_data.m_create(Ploted_values,MIOData.ECAT_1001_RX_Device_Readings_Gas_Index)
                            self.set_attribute(f,ECAT_1001_RX_Device_Readings_Gas_Index,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_ECAT_1001_RX_Device_Readings_Gas_Index"])
                        elif opc_ua_instrument_name + "_MIO_ECAT_1001_RX_Command_Result_Last_Command_ID"== key:
                            ECAT_1001_RX_Command_Result_Last_Command_ID=mio_data.m_create(Ploted_values,MIOData.ECAT_1001_RX_Command_Result_Last_Command_ID)
                            self.set_attribute(f,ECAT_1001_RX_Command_Result_Last_Command_ID,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_ECAT_1001_RX_Command_Result_Last_Command_ID"])
                        elif opc_ua_instrument_name + "_MIO_ECAT_1001_RX_Command_Result_Last_Command_Status"== key:
                            ECAT_1001_RX_Command_Result_Last_Command_Status=mio_data.m_create(Ploted_values,MIOData.ECAT_1001_RX_Command_Result_Last_Command_Status)
                            self.set_attribute(f,ECAT_1001_RX_Command_Result_Last_Command_Status,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_ECAT_1001_RX_Command_Result_Last_Command_Status"])
                        elif opc_ua_instrument_name + "_MIO_ECAT_1001_TX_Setpoint_Setpoint"== key:
                            ECAT_1001_TX_Setpoint_Setpoint=mio_data.m_create(Ploted_values,MIOData.ECAT_1001_TX_Setpoint_Setpoint)
                            self.set_attribute(f,ECAT_1001_TX_Setpoint_Setpoint,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_ECAT_1001_TX_Setpoint_Setpoint"])
                        elif opc_ua_instrument_name + "_MIO_ECAT_1001_TX_Command_Request_Command_ID"== key:
                            ECAT_1001_TX_Command_Request_Command_ID=mio_data.m_create(Ploted_values,MIOData.ECAT_1001_TX_Command_Request_Command_ID)
                            self.set_attribute(f,ECAT_1001_TX_Command_Request_Command_ID,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_ECAT_1001_TX_Command_Request_Command_ID"])
                        elif opc_ua_instrument_name + "_MIO_ECAT_1001_TX_Command_Request_Command_Argument"== key:
                            ECAT_1001_TX_Command_Request_Command_Argument=mio_data.m_create(Ploted_values,MIOData.ECAT_1001_TX_Command_Request_Command_Argument)
                            self.set_attribute(f,ECAT_1001_TX_Command_Request_Command_Argument,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_ECAT_1001_TX_Command_Request_Command_Argument"])
                        elif opc_ua_instrument_name + "_MIO_ECAT_1002_RX_Device_Readings_Gas_Index"== key:
                            ECAT_1002_RX_Device_Readings_Gas_Index=mio_data.m_create(Ploted_values,MIOData.ECAT_1002_RX_Device_Readings_Gas_Index)
                            self.set_attribute(f,ECAT_1002_RX_Device_Readings_Gas_Index,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_ECAT_1002_RX_Device_Readings_Gas_Index"])
                        elif opc_ua_instrument_name + "_MIO_ECAT_1002_RX_Command_Result_Last_Command_ID"== key:
                            ECAT_1002_RX_Command_Result_Last_Command_ID=mio_data.m_create(Ploted_values,MIOData.ECAT_1002_RX_Command_Result_Last_Command_ID)
                            self.set_attribute(f,ECAT_1002_RX_Command_Result_Last_Command_ID,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_ECAT_1002_RX_Command_Result_Last_Command_ID"])
                        elif opc_ua_instrument_name + "_MIO_ECAT_1002_RX_Command_Result_Last_Command_Status"== key:
                            ECAT_1002_RX_Command_Result_Last_Command_Status=mio_data.m_create(Ploted_values,MIOData.ECAT_1002_RX_Command_Result_Last_Command_Status)
                            self.set_attribute(f,ECAT_1002_RX_Command_Result_Last_Command_Status,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_ECAT_1002_RX_Command_Result_Last_Command_Status"])
                        elif opc_ua_instrument_name + "_MIO_ECAT_1002_TX_Setpoint_Setpoint"== key:
                            ECAT_1002_TX_Setpoint_Setpoint=mio_data.m_create(Ploted_values,MIOData.ECAT_1002_TX_Setpoint_Setpoint)
                            self.set_attribute(f,ECAT_1002_TX_Setpoint_Setpoint,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_ECAT_1002_TX_Setpoint_Setpoint"])
                        elif opc_ua_instrument_name + "_MIO_ECAT_1002_TX_Command_Request_Command_ID"== key:
                            ECAT_1002_TX_Command_Request_Command_ID=mio_data.m_create(Ploted_values,MIOData.ECAT_1002_TX_Command_Request_Command_ID)
                            self.set_attribute(f,ECAT_1002_TX_Command_Request_Command_ID,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_ECAT_1002_TX_Command_Request_Command_ID"])
                        elif opc_ua_instrument_name + "_MIO_ECAT_1002_TX_Command_Request_Command_Argument"== key:
                            ECAT_1002_TX_Command_Request_Command_Argument=mio_data.m_create(Ploted_values,MIOData.ECAT_1002_TX_Command_Request_Command_Argument)
                            self.set_attribute(f,ECAT_1002_TX_Command_Request_Command_Argument,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_ECAT_1002_TX_Command_Request_Command_Argument"])
                        elif opc_ua_instrument_name + "_MIO_ECAT_1004_RX_Device_Readings_Gas_Index"== key:
                            ECAT_1004_RX_Device_Readings_Gas_Index=mio_data.m_create(Ploted_values,MIOData.ECAT_1004_RX_Device_Readings_Gas_Index)
                            self.set_attribute(f,ECAT_1004_RX_Device_Readings_Gas_Index,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_ECAT_1004_RX_Device_Readings_Gas_Index"])
                        elif opc_ua_instrument_name + "_MIO_ECAT_1004_RX_Command_Result_Last_Command_ID"== key:
                            ECAT_1004_RX_Command_Result_Last_Command_ID=mio_data.m_create(Ploted_values,MIOData.ECAT_1004_RX_Command_Result_Last_Command_ID)
                            self.set_attribute(f,ECAT_1004_RX_Command_Result_Last_Command_ID,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_ECAT_1004_RX_Command_Result_Last_Command_ID"])
                        elif opc_ua_instrument_name + "_MIO_ECAT_1004_RX_Command_Result_Last_Command_Status"== key:
                            ECAT_1004_RX_Command_Result_Last_Command_Status=mio_data.m_create(Ploted_values,MIOData.ECAT_1004_RX_Command_Result_Last_Command_Status)
                            self.set_attribute(f,ECAT_1004_RX_Command_Result_Last_Command_Status,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_ECAT_1004_RX_Command_Result_Last_Command_Status"])
                        elif opc_ua_instrument_name + "_MIO_ECAT_1004_TX_Setpoint_Setpoint"== key:
                            ECAT_1004_TX_Setpoint_Setpoint=mio_data.m_create(Ploted_values,MIOData.ECAT_1004_TX_Setpoint_Setpoint)
                            self.set_attribute(f,ECAT_1004_TX_Setpoint_Setpoint,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_ECAT_1004_TX_Setpoint_Setpoint"])
                        elif opc_ua_instrument_name + "_MIO_ECAT_1004_TX_Command_Request_Command_ID"== key:
                            ECAT_1004_TX_Command_Request_Command_ID=mio_data.m_create(Ploted_values,MIOData.ECAT_1004_TX_Command_Request_Command_ID)
                            self.set_attribute(f,ECAT_1004_TX_Command_Request_Command_ID,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_ECAT_1004_TX_Command_Request_Command_ID"])
                        elif opc_ua_instrument_name + "_MIO_ECAT_1004_TX_Command_Request_Command_Argument"== key:
                            ECAT_1004_TX_Command_Request_Command_Argument=mio_data.m_create(Ploted_values,MIOData.ECAT_1004_TX_Command_Request_Command_Argument)
                            self.set_attribute(f,ECAT_1004_TX_Command_Request_Command_Argument,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_ECAT_1004_TX_Command_Request_Command_Argument"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Cathode_PT_01_barG"== key:
                            Fluids_Cathode_PT_01_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_PT_01_barG)
                            self.set_attribute(f,Fluids_Cathode_PT_01_barG,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Cathode_PT_01_barG"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Cathode_PT_02_barG"== key:
                            Fluids_Cathode_PT_02_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_PT_02_barG)
                            self.set_attribute(f,Fluids_Cathode_PT_02_barG,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Cathode_PT_02_barG"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Cathode_PT_03_barG"== key:
                            Fluids_Cathode_PT_03_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_PT_03_barG)
                            self.set_attribute(f,Fluids_Cathode_PT_03_barG,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Cathode_PT_03_barG"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Cathode_TT_01_0_Celsius"== key:
                            Fluids_Cathode_TT_01_0_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_TT_01_0_Celsius)
                            self.set_attribute(f,Fluids_Cathode_TT_01_0_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Cathode_TT_01_0_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Cathode_TT_05_Celsius"== key:
                            Fluids_Cathode_TT_05_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_TT_05_Celsius)
                            self.set_attribute(f,Fluids_Cathode_TT_05_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Cathode_TT_05_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Cathode_TT_02_0_Celsius"== key:
                            Fluids_Cathode_TT_02_0_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_TT_02_0_Celsius)
                            self.set_attribute(f,Fluids_Cathode_TT_02_0_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Cathode_TT_02_0_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Cathode_TT_06_Celsius"== key:
                            Fluids_Cathode_TT_06_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_TT_06_Celsius)
                            self.set_attribute(f,Fluids_Cathode_TT_06_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Cathode_TT_06_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Cathode_TT_03_0_Celsius"== key:
                            Fluids_Cathode_TT_03_0_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_TT_03_0_Celsius)
                            self.set_attribute(f,Fluids_Cathode_TT_03_0_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Cathode_TT_03_0_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Cathode_TT_07_Celsius"== key:
                            Fluids_Cathode_TT_07_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_TT_07_Celsius)
                            self.set_attribute(f,Fluids_Cathode_TT_07_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Cathode_TT_07_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Cathode_TT_01_Celsius"== key:
                            Fluids_Cathode_TT_01_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_TT_01_Celsius)
                            self.set_attribute(f,Fluids_Cathode_TT_01_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Cathode_TT_01_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Cathode_TT_02_Celsius"== key:
                            Fluids_Cathode_TT_02_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_TT_02_Celsius)
                            self.set_attribute(f,Fluids_Cathode_TT_02_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Cathode_TT_02_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Cathode_TT_04_Celsius"== key:
                            Fluids_Cathode_TT_04_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_TT_04_Celsius)
                            self.set_attribute(f,Fluids_Cathode_TT_04_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Cathode_TT_04_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Cathode_A_PT_04_barG"== key:
                            Fluids_Cathode_A_PT_04_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_A_PT_04_barG)
                            self.set_attribute(f,Fluids_Cathode_A_PT_04_barG,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Cathode_A_PT_04_barG"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Cathode_A_PT_05_barG"== key:
                            Fluids_Cathode_A_PT_05_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_A_PT_05_barG)
                            self.set_attribute(f,Fluids_Cathode_A_PT_05_barG,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Cathode_A_PT_05_barG"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Cathode_A_PT_06_barG"== key:
                            Fluids_Cathode_A_PT_06_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_A_PT_06_barG)
                            self.set_attribute(f,Fluids_Cathode_A_PT_06_barG,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Cathode_A_PT_06_barG"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Cathode_A_MFT_02_slpm"== key:
                            Fluids_Cathode_A_MFT_02_slpm=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_A_MFT_02_slpm)
                            self.set_attribute(f,Fluids_Cathode_A_MFT_02_slpm,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Cathode_A_MFT_02_slpm"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Cathode_A_RHT_01_prctRH"== key:
                            Fluids_Cathode_A_RHT_01_prctRH=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_A_RHT_01_prctRH)
                            self.set_attribute(f,Fluids_Cathode_A_RHT_01_prctRH,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Cathode_A_RHT_01_prctRH"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Cathode_A_TT_09_Celsius"== key:
                            Fluids_Cathode_A_TT_09_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_A_TT_09_Celsius)
                            self.set_attribute(f,Fluids_Cathode_A_TT_09_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Cathode_A_TT_09_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Cathode_A_TT_08_Celsius"== key:
                            Fluids_Cathode_A_TT_08_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_A_TT_08_Celsius)
                            self.set_attribute(f,Fluids_Cathode_A_TT_08_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Cathode_A_TT_08_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Cathode_A_TT_10_Celsius"== key:
                            Fluids_Cathode_A_TT_10_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_A_TT_10_Celsius)
                            self.set_attribute(f,Fluids_Cathode_A_TT_10_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Cathode_A_TT_10_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Cathode_A_TT_11_Celsius"== key:
                            Fluids_Cathode_A_TT_11_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_A_TT_11_Celsius)
                            self.set_attribute(f,Fluids_Cathode_A_TT_11_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Cathode_A_TT_11_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Cathode_A_TT_12_Celsius"== key:
                            Fluids_Cathode_A_TT_12_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_A_TT_12_Celsius)
                            self.set_attribute(f,Fluids_Cathode_A_TT_12_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Cathode_A_TT_12_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Cathode_B_PT_04_barG"== key:
                            Fluids_Cathode_B_PT_04_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_B_PT_04_barG)
                            self.set_attribute(f,Fluids_Cathode_B_PT_04_barG,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Cathode_B_PT_04_barG"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Cathode_B_PT_05_barG"== key:
                            Fluids_Cathode_B_PT_05_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_B_PT_05_barG)
                            self.set_attribute(f,Fluids_Cathode_B_PT_05_barG,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Cathode_B_PT_05_barG"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Cathode_B_PT_06_barG"== key:
                            Fluids_Cathode_B_PT_06_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_B_PT_06_barG)
                            self.set_attribute(f,Fluids_Cathode_B_PT_06_barG,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Cathode_B_PT_06_barG"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Cathode_B_MFT_02_slpm"== key:
                            Fluids_Cathode_B_MFT_02_slpm=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_B_MFT_02_slpm)
                            self.set_attribute(f,Fluids_Cathode_B_MFT_02_slpm,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Cathode_B_MFT_02_slpm"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Cathode_B_TT_08_Celsius"== key:
                            Fluids_Cathode_B_TT_08_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_B_TT_08_Celsius)
                            self.set_attribute(f,Fluids_Cathode_B_TT_08_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Cathode_B_TT_08_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Cathode_B_TT_10_Celsius"== key:
                            Fluids_Cathode_B_TT_10_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_B_TT_10_Celsius)
                            self.set_attribute(f,Fluids_Cathode_B_TT_10_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Cathode_B_TT_10_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Cathode_B_TT_11_Celsius"== key:
                            Fluids_Cathode_B_TT_11_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_B_TT_11_Celsius)
                            self.set_attribute(f,Fluids_Cathode_B_TT_11_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Cathode_B_TT_11_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Cathode_B_TT_12_Celsius"== key:
                            Fluids_Cathode_B_TT_12_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Cathode_B_TT_12_Celsius)
                            self.set_attribute(f,Fluids_Cathode_B_TT_12_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Cathode_B_TT_12_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Anode_PT_01_barG"== key:
                            Fluids_Anode_PT_01_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_PT_01_barG)
                            self.set_attribute(f,Fluids_Anode_PT_01_barG,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Anode_PT_01_barG"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Anode_TT_01_Celsius"== key:
                            Fluids_Anode_TT_01_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_TT_01_Celsius)
                            self.set_attribute(f,Fluids_Anode_TT_01_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Anode_TT_01_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Anode_A_PT_03_barG"== key:
                            Fluids_Anode_A_PT_03_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_A_PT_03_barG)
                            self.set_attribute(f,Fluids_Anode_A_PT_03_barG,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Anode_A_PT_03_barG"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Anode_A_PT_04_barG"== key:
                            Fluids_Anode_A_PT_04_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_A_PT_04_barG)
                            self.set_attribute(f,Fluids_Anode_A_PT_04_barG,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Anode_A_PT_04_barG"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Anode_A_TT_02_Celsius"== key:
                            Fluids_Anode_A_TT_02_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_A_TT_02_Celsius)
                            self.set_attribute(f,Fluids_Anode_A_TT_02_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Anode_A_TT_02_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Anode_A_TT_03_Celsius"== key:
                            Fluids_Anode_A_TT_03_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_A_TT_03_Celsius)
                            self.set_attribute(f,Fluids_Anode_A_TT_03_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Anode_A_TT_03_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Anode_B_PT_03_barG"== key:
                            Fluids_Anode_B_PT_03_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_B_PT_03_barG)
                            self.set_attribute(f,Fluids_Anode_B_PT_03_barG,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Anode_B_PT_03_barG"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Anode_B_PT_04_barG"== key:
                            Fluids_Anode_B_PT_04_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_B_PT_04_barG)
                            self.set_attribute(f,Fluids_Anode_B_PT_04_barG,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Anode_B_PT_04_barG"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Anode_B_TT_02_Celsius"== key:
                            Fluids_Anode_B_TT_02_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_B_TT_02_Celsius)
                            self.set_attribute(f,Fluids_Anode_B_TT_02_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Anode_B_TT_02_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Anode_B_TT_03_Celsius"== key:
                            Fluids_Anode_B_TT_03_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_B_TT_03_Celsius)
                            self.set_attribute(f,Fluids_Anode_B_TT_03_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Anode_B_TT_03_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Anode_MFT_01_A_p_PSIA"== key:
                            Fluids_Anode_MFT_01_A_p_PSIA=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_MFT_01_A_p_PSIA)
                            self.set_attribute(f,Fluids_Anode_MFT_01_A_p_PSIA,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Anode_MFT_01_A_p_PSIA"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Anode_MFT_01_A_T_Celsius"== key:
                            Fluids_Anode_MFT_01_A_T_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_MFT_01_A_T_Celsius)
                            self.set_attribute(f,Fluids_Anode_MFT_01_A_T_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Anode_MFT_01_A_T_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Anode_MFT_01_A_Vflow_LPM"== key:
                            Fluids_Anode_MFT_01_A_Vflow_LPM=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_MFT_01_A_Vflow_LPM)
                            self.set_attribute(f,Fluids_Anode_MFT_01_A_Vflow_LPM,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Anode_MFT_01_A_Vflow_LPM"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Anode_MFT_01_A_mflow_SLPM"== key:
                            Fluids_Anode_MFT_01_A_mflow_SLPM=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_MFT_01_A_mflow_SLPM)
                            self.set_attribute(f,Fluids_Anode_MFT_01_A_mflow_SLPM,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Anode_MFT_01_A_mflow_SLPM"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Anode_MFT_01_A_mTotal_SL"== key:
                            Fluids_Anode_MFT_01_A_mTotal_SL=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_MFT_01_A_mTotal_SL)
                            self.set_attribute(f,Fluids_Anode_MFT_01_A_mTotal_SL,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Anode_MFT_01_A_mTotal_SL"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Anode_MFT_01_B_p_PSIA"== key:
                            Fluids_Anode_MFT_01_B_p_PSIA=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_MFT_01_B_p_PSIA)
                            self.set_attribute(f,Fluids_Anode_MFT_01_B_p_PSIA,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Anode_MFT_01_B_p_PSIA"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Anode_MFT_01_B_T_Celsius"== key:
                            Fluids_Anode_MFT_01_B_T_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_MFT_01_B_T_Celsius)
                            self.set_attribute(f,Fluids_Anode_MFT_01_B_T_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Anode_MFT_01_B_T_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Anode_MFT_01_B_Vflow_LPM"== key:
                            Fluids_Anode_MFT_01_B_Vflow_LPM=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_MFT_01_B_Vflow_LPM)
                            self.set_attribute(f,Fluids_Anode_MFT_01_B_Vflow_LPM,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Anode_MFT_01_B_Vflow_LPM"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Anode_MFT_01_B_mflow_SLPM"== key:
                            Fluids_Anode_MFT_01_B_mflow_SLPM=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_MFT_01_B_mflow_SLPM)
                            self.set_attribute(f,Fluids_Anode_MFT_01_B_mflow_SLPM,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Anode_MFT_01_B_mflow_SLPM"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Anode_MFT_01_B_mTotal_SL"== key:
                            Fluids_Anode_MFT_01_B_mTotal_SL=mio_data.m_create(Ploted_values,MIOData.Fluids_Anode_MFT_01_B_mTotal_SL)
                            self.set_attribute(f,Fluids_Anode_MFT_01_B_mTotal_SL,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Anode_MFT_01_B_mTotal_SL"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Thermal_PT_01_barG"== key:
                            Fluids_Thermal_PT_01_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_PT_01_barG)
                            self.set_attribute(f,Fluids_Thermal_PT_01_barG,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Thermal_PT_01_barG"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Thermal_PT_02_barG"== key:
                            Fluids_Thermal_PT_02_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_PT_02_barG)
                            self.set_attribute(f,Fluids_Thermal_PT_02_barG,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Thermal_PT_02_barG"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Thermal_PT_03_A_barG"== key:
                            Fluids_Thermal_PT_03_A_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_PT_03_A_barG)
                            self.set_attribute(f,Fluids_Thermal_PT_03_A_barG,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Thermal_PT_03_A_barG"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Thermal_PT_03_B_barG"== key:
                            Fluids_Thermal_PT_03_B_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_PT_03_B_barG)
                            self.set_attribute(f,Fluids_Thermal_PT_03_B_barG,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Thermal_PT_03_B_barG"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Thermal_PT_04_A_barG"== key:
                            Fluids_Thermal_PT_04_A_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_PT_04_A_barG)
                            self.set_attribute(f,Fluids_Thermal_PT_04_A_barG,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Thermal_PT_04_A_barG"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Thermal_PT_04_B_barG"== key:
                            Fluids_Thermal_PT_04_B_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_PT_04_B_barG)
                            self.set_attribute(f,Fluids_Thermal_PT_04_B_barG,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Thermal_PT_04_B_barG"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Thermal_PT_05_barG"== key:
                            Fluids_Thermal_PT_05_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_PT_05_barG)
                            self.set_attribute(f,Fluids_Thermal_PT_05_barG,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Thermal_PT_05_barG"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Thermal_PT_06_barG"== key:
                            Fluids_Thermal_PT_06_barG=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_PT_06_barG)
                            self.set_attribute(f,Fluids_Thermal_PT_06_barG,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Thermal_PT_06_barG"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Thermal_MFT_01_02_lpm"== key:
                            Fluids_Thermal_MFT_01_02_lpm=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_MFT_01_02_lpm)
                            self.set_attribute(f,Fluids_Thermal_MFT_01_02_lpm,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Thermal_MFT_01_02_lpm"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Thermal_MFT_02_lpm"== key:
                            Fluids_Thermal_MFT_02_lpm=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_MFT_02_lpm)
                            self.set_attribute(f,Fluids_Thermal_MFT_02_lpm,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Thermal_MFT_02_lpm"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Thermal_TT_01_01_Celsius"== key:
                            Fluids_Thermal_TT_01_01_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_TT_01_01_Celsius)
                            self.set_attribute(f,Fluids_Thermal_TT_01_01_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Thermal_TT_01_01_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Thermal_TT_03_02_Celsius"== key:
                            Fluids_Thermal_TT_03_02_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_TT_03_02_Celsius)
                            self.set_attribute(f,Fluids_Thermal_TT_03_02_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Thermal_TT_03_02_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Thermal_TT_01_Celsius"== key:
                            Fluids_Thermal_TT_01_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_TT_01_Celsius)
                            self.set_attribute(f,Fluids_Thermal_TT_01_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Thermal_TT_01_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Thermal_TT_05_Celsius"== key:
                            Fluids_Thermal_TT_05_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_TT_05_Celsius)
                            self.set_attribute(f,Fluids_Thermal_TT_05_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Thermal_TT_05_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Thermal_TT_02_01_Celsius"== key:
                            Fluids_Thermal_TT_02_01_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_TT_02_01_Celsius)
                            self.set_attribute(f,Fluids_Thermal_TT_02_01_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Thermal_TT_02_01_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Thermal_TT_04_02_Celsius"== key:
                            Fluids_Thermal_TT_04_02_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_TT_04_02_Celsius)
                            self.set_attribute(f,Fluids_Thermal_TT_04_02_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Thermal_TT_04_02_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Thermal_TT_06_01_Celsius"== key:
                            Fluids_Thermal_TT_06_01_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_TT_06_01_Celsius)
                            self.set_attribute(f,Fluids_Thermal_TT_06_01_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Thermal_TT_06_01_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Thermal_TT_08_02_Celsius"== key:
                            Fluids_Thermal_TT_08_02_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_TT_08_02_Celsius)
                            self.set_attribute(f,Fluids_Thermal_TT_08_02_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Thermal_TT_08_02_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Thermal_TT_07_01_Celsius"== key:
                            Fluids_Thermal_TT_07_01_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_TT_07_01_Celsius)
                            self.set_attribute(f,Fluids_Thermal_TT_07_01_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Thermal_TT_07_01_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Thermal_TT_09_02_Celsius"== key:
                            Fluids_Thermal_TT_09_02_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_TT_09_02_Celsius)
                            self.set_attribute(f,Fluids_Thermal_TT_09_02_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Thermal_TT_09_02_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Thermal_TT_11_Celsius"== key:
                            Fluids_Thermal_TT_11_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_TT_11_Celsius)
                            self.set_attribute(f,Fluids_Thermal_TT_11_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Thermal_TT_11_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Thermal_TT_01_02_Celsius"== key:
                            Fluids_Thermal_TT_01_02_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_TT_01_02_Celsius)
                            self.set_attribute(f,Fluids_Thermal_TT_01_02_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Thermal_TT_01_02_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Thermal_A_MFT_01_lpm"== key:
                            Fluids_Thermal_A_MFT_01_lpm=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_A_MFT_01_lpm)
                            self.set_attribute(f,Fluids_Thermal_A_MFT_01_lpm,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Thermal_A_MFT_01_lpm"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Thermal_A_TT_03_Celsius"== key:
                            Fluids_Thermal_A_TT_03_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_A_TT_03_Celsius)
                            self.set_attribute(f,Fluids_Thermal_A_TT_03_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Thermal_A_TT_03_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Thermal_A_TT_04_Celsius"== key:
                            Fluids_Thermal_A_TT_04_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_A_TT_04_Celsius)
                            self.set_attribute(f,Fluids_Thermal_A_TT_04_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Thermal_A_TT_04_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Thermal_B_MFT_01_lpm"== key:
                            Fluids_Thermal_B_MFT_01_lpm=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_B_MFT_01_lpm)
                            self.set_attribute(f,Fluids_Thermal_B_MFT_01_lpm,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Thermal_B_MFT_01_lpm"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Thermal_B_TT_03_Celsius"== key:
                            Fluids_Thermal_B_TT_03_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_B_TT_03_Celsius)
                            self.set_attribute(f,Fluids_Thermal_B_TT_03_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Thermal_B_TT_03_Celsius"])
                        elif opc_ua_instrument_name + "_MIO_Fluids_Thermal_B_TT_04_Celsius"== key:
                            Fluids_Thermal_B_TT_04_Celsius=mio_data.m_create(Ploted_values,MIOData.Fluids_Thermal_B_TT_04_Celsius)
                            self.set_attribute(f,Fluids_Thermal_B_TT_04_Celsius,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_MIO_Fluids_Thermal_B_TT_04_Celsius"])
                        else:
                            undef_item = mio_data.m_create(Ploted_values,MIOData.undefined_data)
                            self.set_attribute(f,undef_item,"data",[CAMELS_entry,"data",str(key)])
                            undef_item.name = key

                    elif key.startswith(opc_ua_instrument_name+"_HP_CAN"):
                        if opc_ua_instrument_name + "_HP_CAN_Net_A_fbCAN_FSM_iStep"== key:
                            Net_A_fbCAN_FSM_iStep=hp_can_data.m_create(Ploted_values,HP_CANData.Net_A_fbCAN_FSM_iStep)
                            self.set_attribute(f,Net_A_fbCAN_FSM_iStep,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_HP_CAN_Net_A_fbCAN_FSM_iStep"])
                        elif opc_ua_instrument_name + "_HP_CAN_Net_A_RH01_actValues_current_act_A"== key:
                            Net_A_RH01_actValues_current_act_A=hp_can_data.m_create(Ploted_values,HP_CANData.Net_A_RH01_actValues_current_act_A)
                            self.set_attribute(f,Net_A_RH01_actValues_current_act_A,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_HP_CAN_Net_A_RH01_actValues_current_act_A"])
                        elif opc_ua_instrument_name + "_HP_CAN_Net_A_RH01_actValues_power_act_W"== key:
                            Net_A_RH01_actValues_power_act_W=hp_can_data.m_create(Ploted_values,HP_CANData.Net_A_RH01_actValues_power_act_W)
                            self.set_attribute(f,Net_A_RH01_actValues_power_act_W,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_HP_CAN_Net_A_RH01_actValues_power_act_W"])
                        elif opc_ua_instrument_name + "_HP_CAN_Net_A_RH01_actValues_speed_act_rpm"== key:
                            Net_A_RH01_actValues_speed_act_rpm=hp_can_data.m_create(Ploted_values,HP_CANData.Net_A_RH01_actValues_speed_act_rpm)
                            self.set_attribute(f,Net_A_RH01_actValues_speed_act_rpm,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_HP_CAN_Net_A_RH01_actValues_speed_act_rpm"])
                        elif opc_ua_instrument_name + "_HP_CAN_Net_A_RH01_actValues_T_circuit_C"== key:
                            Net_A_RH01_actValues_T_circuit_C=hp_can_data.m_create(Ploted_values,HP_CANData.Net_A_RH01_actValues_T_circuit_C)
                            self.set_attribute(f,Net_A_RH01_actValues_T_circuit_C,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_HP_CAN_Net_A_RH01_actValues_T_circuit_C"])
                        elif opc_ua_instrument_name + "_HP_CAN_Net_A_RH01_actValues_voltage_act_V"== key:
                            Net_A_RH01_actValues_voltage_act_V=hp_can_data.m_create(Ploted_values,HP_CANData.Net_A_RH01_actValues_voltage_act_V)
                            self.set_attribute(f,Net_A_RH01_actValues_voltage_act_V,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_HP_CAN_Net_A_RH01_actValues_voltage_act_V"])
                        elif opc_ua_instrument_name + "_HP_CAN_Net_A_RH01_cmd_mDot_cmd_kgph"== key:
                            Net_A_RH01_cmd_mDot_cmd_kgph=hp_can_data.m_create(Ploted_values,HP_CANData.Net_A_RH01_cmd_mDot_cmd_kgph)
                            self.set_attribute(f,Net_A_RH01_cmd_mDot_cmd_kgph,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_HP_CAN_Net_A_RH01_cmd_mDot_cmd_kgph"])
                        elif opc_ua_instrument_name + "_HP_CAN_Net_A_RH01_cmd_speed_cmd_rpm"== key:
                            Net_A_RH01_cmd_speed_cmd_rpm=hp_can_data.m_create(Ploted_values,HP_CANData.Net_A_RH01_cmd_speed_cmd_rpm)
                            self.set_attribute(f,Net_A_RH01_cmd_speed_cmd_rpm,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_HP_CAN_Net_A_RH01_cmd_speed_cmd_rpm"])
                        elif opc_ua_instrument_name + "_HP_CAN_Net_B_fbCAN_FSM_iStep"== key:
                            Net_B_fbCAN_FSM_iStep=hp_can_data.m_create(Ploted_values,HP_CANData.Net_B_fbCAN_FSM_iStep)
                            self.set_attribute(f,Net_B_fbCAN_FSM_iStep,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_HP_CAN_Net_B_fbCAN_FSM_iStep"])
                        elif opc_ua_instrument_name + "_HP_CAN_Net_B_RH01_actValues_current_act_A"== key:
                            Net_B_RH01_actValues_current_act_A=hp_can_data.m_create(Ploted_values,HP_CANData.Net_B_RH01_actValues_current_act_A)
                            self.set_attribute(f,Net_B_RH01_actValues_current_act_A,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_HP_CAN_Net_B_RH01_actValues_current_act_A"])
                        elif opc_ua_instrument_name + "_HP_CAN_Net_B_RH01_actValues_power_act_W"== key:
                            Net_B_RH01_actValues_power_act_W=hp_can_data.m_create(Ploted_values,HP_CANData.Net_B_RH01_actValues_power_act_W)
                            self.set_attribute(f,Net_B_RH01_actValues_power_act_W,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_HP_CAN_Net_B_RH01_actValues_power_act_W"])
                        elif opc_ua_instrument_name + "_HP_CAN_Net_B_RH01_actValues_speed_act_rpm"== key:
                            Net_B_RH01_actValues_speed_act_rpm=hp_can_data.m_create(Ploted_values,HP_CANData.Net_B_RH01_actValues_speed_act_rpm)
                            self.set_attribute(f,Net_B_RH01_actValues_speed_act_rpm,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_HP_CAN_Net_B_RH01_actValues_speed_act_rpm"])
                        elif opc_ua_instrument_name + "_HP_CAN_Net_B_RH01_actValues_T_circuit_C"== key:
                            Net_B_RH01_actValues_T_circuit_C=hp_can_data.m_create(Ploted_values,HP_CANData.Net_B_RH01_actValues_T_circuit_C)
                            self.set_attribute(f,Net_B_RH01_actValues_T_circuit_C,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_HP_CAN_Net_B_RH01_actValues_T_circuit_C"])
                        elif opc_ua_instrument_name + "_HP_CAN_Net_B_RH01_actValues_voltage_act_V"== key:
                            Net_B_RH01_actValues_voltage_act_V=hp_can_data.m_create(Ploted_values,HP_CANData.Net_B_RH01_actValues_voltage_act_V)
                            self.set_attribute(f,Net_B_RH01_actValues_voltage_act_V,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_HP_CAN_Net_B_RH01_actValues_voltage_act_V"])
                        elif opc_ua_instrument_name + "_HP_CAN_Net_B_RH01_cmd_mDot_cmd_kgph"== key:
                            Net_B_RH01_cmd_mDot_cmd_kgph=hp_can_data.m_create(Ploted_values,HP_CANData.Net_B_RH01_cmd_mDot_cmd_kgph)
                            self.set_attribute(f,Net_B_RH01_cmd_mDot_cmd_kgph,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_HP_CAN_Net_B_RH01_cmd_mDot_cmd_kgph"])
                        elif opc_ua_instrument_name + "_HP_CAN_Net_B_RH01_cmd_speed_cmd_rpm"== key:
                            Net_B_RH01_cmd_speed_cmd_rpm=hp_can_data.m_create(Ploted_values,HP_CANData.Net_B_RH01_cmd_speed_cmd_rpm)
                            self.set_attribute(f,Net_B_RH01_cmd_speed_cmd_rpm,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_HP_CAN_Net_B_RH01_cmd_speed_cmd_rpm"])
                        else:
                            undef_item = hp_can_data.m_create(Ploted_values,HP_CANData.undefined_data)
                            self.set_attribute(f,undef_item,"data",[CAMELS_entry,"data",key])
                            undef_item.name = key
                    
                    elif key.startswith(opc_ua_instrument_name+"_ACTIF"):
                        if opc_ua_instrument_name + "_ACTIF_Anode_GasSupply_state"== key:
                            Anode_GasSupply_state=actif_data.m_create(Ploted_values,ACTIFData.Anode_GasSupply_state)
                            self.set_attribute(f,Anode_GasSupply_state,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Anode_GasSupply_state"])
                        elif opc_ua_instrument_name + "_ACTIF_Anode_PC_01_A_cmd"== key:
                            Anode_PC_01_A_cmd=actif_data.m_create(Ploted_values,ACTIFData.Anode_PC_01_A_cmd)
                            self.set_attribute(f,Anode_PC_01_A_cmd,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Anode_PC_01_A_cmd"])
                        elif opc_ua_instrument_name + "_ACTIF_Anode_PC_01_A_state"== key:
                            Anode_PC_01_A_state=actif_data.m_create(Ploted_values,ACTIFData.Anode_PC_01_A_state)
                            self.set_attribute(f,Anode_PC_01_A_state,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Anode_PC_01_A_state"])
                        elif opc_ua_instrument_name + "_ACTIF_Anode_PC_01_B_cmd"== key:
                            Anode_PC_01_B_cmd=actif_data.m_create(Ploted_values,ACTIFData.Anode_PC_01_B_cmd)
                            self.set_attribute(f,Anode_PC_01_B_cmd,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Anode_PC_01_B_cmd"])
                        elif opc_ua_instrument_name + "_ACTIF_Anode_PC_01_B_state"== key:
                            Anode_PC_01_B_state=actif_data.m_create(Ploted_values,ACTIFData.Anode_PC_01_B_state)
                            self.set_attribute(f,Anode_PC_01_B_state,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Anode_PC_01_B_state"])
                        elif opc_ua_instrument_name + "_ACTIF_Anode_PV_01_A_cmd"== key:
                            Anode_PV_01_A_cmd=actif_data.m_create(Ploted_values,ACTIFData.Anode_PV_01_A_cmd)
                            self.set_attribute(f,Anode_PV_01_A_cmd,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Anode_PV_01_A_cmd"])
                        elif opc_ua_instrument_name + "_ACTIF_Anode_PV_01_A_state"== key:
                            Anode_PV_01_A_state=actif_data.m_create(Ploted_values,ACTIFData.Anode_PV_01_A_state)
                            self.set_attribute(f,Anode_PV_01_A_state,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Anode_PV_01_A_state"])
                        elif opc_ua_instrument_name + "_ACTIF_Anode_PV_01_B_cmd"== key:
                            Anode_PV_01_B_cmd=actif_data.m_create(Ploted_values,ACTIFData.Anode_PV_01_B_cmd)
                            self.set_attribute(f,Anode_PV_01_B_cmd,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Anode_PV_01_B_cmd"])
                        elif opc_ua_instrument_name + "_ACTIF_Anode_PV_01_B_state"== key:
                            Anode_PV_01_B_state=actif_data.m_create(Ploted_values,ACTIFData.Anode_PV_01_B_state)
                            self.set_attribute(f,Anode_PV_01_B_state,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Anode_PV_01_B_state"])
                        elif opc_ua_instrument_name + "_ACTIF_Cathode_AC_01_cmd"== key:
                            Cathode_AC_01_cmd=actif_data.m_create(Ploted_values,ACTIFData.Cathode_AC_01_cmd)
                            self.set_attribute(f,Cathode_AC_01_cmd,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Cathode_AC_01_cmd"])
                        elif opc_ua_instrument_name + "_ACTIF_Cathode_AC_01_state"== key:
                            Cathode_AC_01_state=actif_data.m_create(Ploted_values,ACTIFData.Cathode_AC_01_state)
                            self.set_attribute(f,Cathode_AC_01_state,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Cathode_AC_01_state"])
                        elif opc_ua_instrument_name + "_ACTIF_Cathode_EH_01_cmd"== key:
                            Cathode_EH_01_cmd=actif_data.m_create(Ploted_values,ACTIFData.Cathode_EH_01_cmd)
                            self.set_attribute(f,Cathode_EH_01_cmd,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Cathode_EH_01_cmd"])
                        elif opc_ua_instrument_name + "_ACTIF_Cathode_EH_01_state"== key:
                            Cathode_EH_01_state=actif_data.m_create(Ploted_values,ACTIFData.Cathode_EH_01_state)
                            self.set_attribute(f,Cathode_EH_01_state,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Cathode_EH_01_state"])
                        elif opc_ua_instrument_name + "_ACTIF_Cathode_EH_02_cmd"== key:
                            Cathode_EH_02_cmd=actif_data.m_create(Ploted_values,ACTIFData.Cathode_EH_02_cmd)
                            self.set_attribute(f,Cathode_EH_02_cmd,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Cathode_EH_02_cmd"])
                        elif opc_ua_instrument_name + "_ACTIF_Cathode_EH_02_state"== key:
                            Cathode_EH_02_state=actif_data.m_create(Ploted_values,ACTIFData.Cathode_EH_02_state)
                            self.set_attribute(f,Cathode_EH_02_state,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Cathode_EH_02_state"])
                        elif opc_ua_instrument_name + "_ACTIF_Cathode_MFC_01_00_cmd"== key:
                            Cathode_MFC_01_00_cmd=actif_data.m_create(Ploted_values,ACTIFData.Cathode_MFC_01_00_cmd)
                            self.set_attribute(f,Cathode_MFC_01_00_cmd,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Cathode_MFC_01_00_cmd"])
                        elif opc_ua_instrument_name + "_ACTIF_Cathode_MFC_01_00_state"== key:
                            Cathode_MFC_01_00_state=actif_data.m_create(Ploted_values,ACTIFData.Cathode_MFC_01_00_state)
                            self.set_attribute(f,Cathode_MFC_01_00_state,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Cathode_MFC_01_00_state"])
                        elif opc_ua_instrument_name + "_ACTIF_Cathode_TV_01_A_cmd"== key:
                            Cathode_TV_01_A_cmd=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_01_A_cmd)
                            self.set_attribute(f,Cathode_TV_01_A_cmd,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Cathode_TV_01_A_cmd"])
                        elif opc_ua_instrument_name + "_ACTIF_Cathode_TV_01_A_state"== key:
                            Cathode_TV_01_A_state=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_01_A_state)
                            self.set_attribute(f,Cathode_TV_01_A_state,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Cathode_TV_01_A_state"])
                        elif opc_ua_instrument_name + "_ACTIF_Cathode_TV_01_A_theta_prct"== key:
                            Cathode_TV_01_A_theta_prct=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_01_A_theta_prct)
                            self.set_attribute(f,Cathode_TV_01_A_theta_prct,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Cathode_TV_01_A_theta_prct"])
                        elif opc_ua_instrument_name + "_ACTIF_Cathode_TV_01_B_cmd"== key:
                            Cathode_TV_01_B_cmd=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_01_B_cmd)
                            self.set_attribute(f,Cathode_TV_01_B_cmd,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Cathode_TV_01_B_cmd"])
                        elif opc_ua_instrument_name + "_ACTIF_Cathode_TV_01_B_state"== key:
                            Cathode_TV_01_B_state=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_01_B_state)
                            self.set_attribute(f,Cathode_TV_01_B_state,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Cathode_TV_01_B_state"])
                        elif opc_ua_instrument_name + "_ACTIF_Cathode_TV_01_B_theta_prct"== key:
                            Cathode_TV_01_B_theta_prct=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_01_B_theta_prct)
                            self.set_attribute(f,Cathode_TV_01_B_theta_prct,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Cathode_TV_01_B_theta_prct"])
                        elif opc_ua_instrument_name + "_ACTIF_Cathode_TV_02_A_cmd"== key:
                            Cathode_TV_02_A_cmd=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_02_A_cmd)
                            self.set_attribute(f,Cathode_TV_02_A_cmd,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Cathode_TV_02_A_cmd"])
                        elif opc_ua_instrument_name + "_ACTIF_Cathode_TV_02_A_state"== key:
                            Cathode_TV_02_A_state=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_02_A_state)
                            self.set_attribute(f,Cathode_TV_02_A_state,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Cathode_TV_02_A_state"])
                        elif opc_ua_instrument_name + "_ACTIF_Cathode_TV_02_A_theta_prct"== key:
                            Cathode_TV_02_A_theta_prct=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_02_A_theta_prct)
                            self.set_attribute(f,Cathode_TV_02_A_theta_prct,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Cathode_TV_02_A_theta_prct"])
                        elif opc_ua_instrument_name + "_ACTIF_Cathode_TV_02_B_cmd"== key:
                            Cathode_TV_02_B_cmd=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_02_B_cmd)
                            self.set_attribute(f,Cathode_TV_02_B_cmd,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Cathode_TV_02_B_cmd"])
                        elif opc_ua_instrument_name + "_ACTIF_Cathode_TV_02_B_state"== key:
                            Cathode_TV_02_B_state=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_02_B_state)
                            self.set_attribute(f,Cathode_TV_02_B_state,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Cathode_TV_02_B_state"])
                        elif opc_ua_instrument_name + "_ACTIF_Cathode_TV_02_B_theta_prct"== key:
                            Cathode_TV_02_B_theta_prct=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_02_B_theta_prct)
                            self.set_attribute(f,Cathode_TV_02_B_theta_prct,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Cathode_TV_02_B_theta_prct"])
                        elif opc_ua_instrument_name + "_ACTIF_Cathode_TV_03_A_cmd"== key:
                            Cathode_TV_03_A_cmd=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_03_A_cmd)
                            self.set_attribute(f,Cathode_TV_03_A_cmd,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Cathode_TV_03_A_cmd"])
                        elif opc_ua_instrument_name + "_ACTIF_Cathode_TV_03_A_state"== key:
                            Cathode_TV_03_A_state=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_03_A_state)
                            self.set_attribute(f,Cathode_TV_03_A_state,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Cathode_TV_03_A_state"])
                        elif opc_ua_instrument_name + "_ACTIF_Cathode_TV_03_A_theta_prct"== key:
                            Cathode_TV_03_A_theta_prct=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_03_A_theta_prct)
                            self.set_attribute(f,Cathode_TV_03_A_theta_prct,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Cathode_TV_03_A_theta_prct"])
                        elif opc_ua_instrument_name + "_ACTIF_Cathode_TV_03_B_cmd"== key:
                            Cathode_TV_03_B_cmd=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_03_B_cmd)
                            self.set_attribute(f,Cathode_TV_03_B_cmd,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Cathode_TV_03_B_cmd"])
                        elif opc_ua_instrument_name + "_ACTIF_Cathode_TV_03_B_state"== key:
                            Cathode_TV_03_B_state=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_03_B_state)
                            self.set_attribute(f,Cathode_TV_03_B_state,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Cathode_TV_03_B_state"])
                        elif opc_ua_instrument_name + "_ACTIF_Cathode_TV_03_B_theta_prct"== key:
                            Cathode_TV_03_B_theta_prct=actif_data.m_create(Ploted_values,ACTIFData.Cathode_TV_03_B_theta_prct)
                            self.set_attribute(f,Cathode_TV_03_B_theta_prct,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Cathode_TV_03_B_theta_prct"])
                        elif opc_ua_instrument_name + "_ACTIF_Thermal_AV_01_A_cmd"== key:
                            Thermal_AV_01_A_cmd=actif_data.m_create(Ploted_values,ACTIFData.Thermal_AV_01_A_cmd)
                            self.set_attribute(f,Thermal_AV_01_A_cmd,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Thermal_AV_01_A_cmd"])
                        elif opc_ua_instrument_name + "_ACTIF_Thermal_AV_01_A_state"== key:
                            Thermal_AV_01_A_state=actif_data.m_create(Ploted_values,ACTIFData.Thermal_AV_01_A_state)
                            self.set_attribute(f,Thermal_AV_01_A_state,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Thermal_AV_01_A_state"])
                        elif opc_ua_instrument_name + "_ACTIF_Thermal_AV_01_B_cmd"== key:
                            Thermal_AV_01_B_cmd=actif_data.m_create(Ploted_values,ACTIFData.Thermal_AV_01_B_cmd)
                            self.set_attribute(f,Thermal_AV_01_B_cmd,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Thermal_AV_01_B_cmd"])
                        elif opc_ua_instrument_name + "_ACTIF_Thermal_AV_01_B_state"== key:
                            Thermal_AV_01_B_state=actif_data.m_create(Ploted_values,ACTIFData.Thermal_AV_01_B_state)
                            self.set_attribute(f,Thermal_AV_01_B_state,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Thermal_AV_01_B_state"])
                        elif opc_ua_instrument_name + "_ACTIF_Thermal_CP_01_cmd_prct"== key:
                            Thermal_CP_01_cmd_prct=actif_data.m_create(Ploted_values,ACTIFData.Thermal_CP_01_cmd_prct)
                            self.set_attribute(f,Thermal_CP_01_cmd_prct,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Thermal_CP_01_cmd_prct"])
                        elif opc_ua_instrument_name + "_ACTIF_Thermal_CP_01_state"== key:
                            Thermal_CP_01_state=actif_data.m_create(Ploted_values,ACTIFData.Thermal_CP_01_state)
                            self.set_attribute(f,Thermal_CP_01_state,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Thermal_CP_01_state"])
                        elif opc_ua_instrument_name + "_ACTIF_Thermal_FLKS_01_CP_01_cmd_prct"== key:
                            Thermal_FLKS_01_CP_01_cmd_prct=actif_data.m_create(Ploted_values,ACTIFData.Thermal_FLKS_01_CP_01_cmd_prct)
                            self.set_attribute(f,Thermal_FLKS_01_CP_01_cmd_prct,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Thermal_FLKS_01_CP_01_cmd_prct"])
                        elif opc_ua_instrument_name + "_ACTIF_Thermal_FLKS_01_CP_01_state"== key:
                            Thermal_FLKS_01_CP_01_state=actif_data.m_create(Ploted_values,ACTIFData.Thermal_FLKS_01_CP_01_state)
                            self.set_attribute(f,Thermal_FLKS_01_CP_01_state,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Thermal_FLKS_01_CP_01_state"])
                        elif opc_ua_instrument_name + "_ACTIF_Thermal_FLKS_01_Fan_01_cmd"== key:
                            Thermal_FLKS_01_Fan_01_cmd=actif_data.m_create(Ploted_values,ACTIFData.Thermal_FLKS_01_Fan_01_cmd)
                            self.set_attribute(f,Thermal_FLKS_01_Fan_01_cmd,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Thermal_FLKS_01_Fan_01_cmd"])
                        elif opc_ua_instrument_name + "_ACTIF_Thermal_FLKS_01_Fan_01_state"== key:
                            Thermal_FLKS_01_Fan_01_state=actif_data.m_create(Ploted_values,ACTIFData.Thermal_FLKS_01_Fan_01_state)
                            self.set_attribute(f,Thermal_FLKS_01_Fan_01_state,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Thermal_FLKS_01_Fan_01_state"])
                        elif opc_ua_instrument_name + "_ACTIF_Thermal_MV_01_cmd"== key:
                            Thermal_MV_01_cmd=actif_data.m_create(Ploted_values,ACTIFData.Thermal_MV_01_cmd)
                            self.set_attribute(f,Thermal_MV_01_cmd,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Thermal_MV_01_cmd"])
                        elif opc_ua_instrument_name + "_ACTIF_Thermal_MV_01_state"== key:
                            Thermal_MV_01_state=actif_data.m_create(Ploted_values,ACTIFData.Thermal_MV_01_state)
                            self.set_attribute(f,Thermal_MV_01_state,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Thermal_MV_01_state"])
                        elif opc_ua_instrument_name + "_ACTIF_Thermal_PV_01_cmd"== key:
                            Thermal_PV_01_cmd=actif_data.m_create(Ploted_values,ACTIFData.Thermal_PV_01_cmd)
                            self.set_attribute(f,Thermal_PV_01_cmd,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Thermal_PV_01_cmd"])
                        elif opc_ua_instrument_name + "_ACTIF_Thermal_PV_01_state"== key:
                            Thermal_PV_01_state=actif_data.m_create(Ploted_values,ACTIFData.Thermal_PV_01_state)
                            self.set_attribute(f,Thermal_PV_01_state,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Thermal_PV_01_state"])
                        elif opc_ua_instrument_name + "_ACTIF_Thermal_PV_02_cmd"== key:
                            Thermal_PV_02_cmd=actif_data.m_create(Ploted_values,ACTIFData.Thermal_PV_02_cmd)
                            self.set_attribute(f,Thermal_PV_02_cmd,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Thermal_PV_02_cmd"])
                        elif opc_ua_instrument_name + "_ACTIF_Thermal_PV_02_state"== key:
                            Thermal_PV_02_state=actif_data.m_create(Ploted_values,ACTIFData.Thermal_PV_02_state)
                            self.set_attribute(f,Thermal_PV_02_state,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF_Thermal_PV_02_state"])
                        else:
                            undef_item = actif_data.m_create(Ploted_values,ACTIFData.undefined_data)
                            self.set_attribute(f,undef_item,"data",[CAMELS_entry,"data",str(key)])
                            undef_item.name = key


                    elif key.startswith(opc_ua_instrument_name+"_ACTIF2"):
                        if opc_ua_instrument_name + "_ACTIF2_RH_01_A_state"== key:
                            RH_01_A_state=actif2_data.m_create(Ploted_values,ACTIF2Data.RH_01_A_state)
                            self.set_attribute(f,RH_01_A_state,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF2_RH_01_A_state"])
                        elif opc_ua_instrument_name + "_ACTIF2_RH_01_A_cmd"== key:
                            RH_01_A_cmd=actif2_data.m_create(Ploted_values,ACTIF2Data.RH_01_A_cmd)
                            self.set_attribute(f,RH_01_A_cmd,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF2_RH_01_A_cmd"])
                        elif opc_ua_instrument_name + "_ACTIF2_RH_01_B_state"== key:
                            RH_01_B_state=actif2_data.m_create(Ploted_values,ACTIF2Data.RH_01_B_state)
                            self.set_attribute(f,RH_01_B_state,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF2_RH_01_B_state"])
                        elif opc_ua_instrument_name + "_ACTIF2_RH_01_B_cmd"== key:
                            RH_01_B_cmd=actif2_data.m_create(Ploted_values,ACTIF2Data.RH_01_B_cmd)
                            self.set_attribute(f,RH_01_B_cmd,"data",[CAMELS_entry,"data",opc_ua_instrument_name+"_ACTIF2_RH_01_B_cmd"])
                        else:
                            undef_item = actif2_data.m_create(Ploted_values,ACTIF2Data.undefined_data)
                            self.set_attribute(f,undef_item,"data",[CAMELS_entry,"data",str(key)])
                            undef_item.name = key

                    else:
                        
                        try:
                            undef_item = undef_data.m_create(Ploted_values,Undefined_data.data)
                            self.set_attribute(f,undef_item,"data",[CAMELS_entry,"data",str(key)])
                            undef_item.name = key
                        except:
                            logger.info("could not create element for:"+key)

                    """if isinstance(f[CAMELS_entry]["data"][key], list):
                            undef_item = Undefined_data()
                            undef_item.data= Ploted_values()
                            undef_item.data.name= key
                            undef_item.data.data=f[CAMELS_entry]["data"][key]
                            undef_data.append(undef_item)"""
                else:
                    
                    try:
                        if key not in ["ElapsedTime","time"]:
                            undef_item = undef_data.m_create(Ploted_values,Undefined_data.data)
                            self.set_attribute(f,undef_item,"data",[CAMELS_entry,"data",str(key)])
                            undef_item.name = key
                    except:
                        logger.info("could not create element for:"+key)
                        
                    
                    
        """if isinstance(f[CAMELS_entry]["data"][key], list) and key!="ElapsedTime":
                        undef_item = Undefined_data()
                        undef_item.data= Ploted_values()
                        undef_item.data.name= key
                        undef_item.data.data=f[CAMELS_entry]["data"][key]
                        #self.set_attribute(f,undef_item.data,"data",[CAMELS_entry,"data",])
                        undef_data.append(undef_item)"""

                   
                    
               
                #schema.mio_data.append(mio_data)
                #schema.data.actif_data.append(actif_data)
                #schema.data.actif2_data.append(actif2_data)
                #schema.data.hp_can_data.append(hp_can_data)
        archive.data=schema
        logger.info("h5 was read propperly")
        logger.info(str(os.getcwd()))
    