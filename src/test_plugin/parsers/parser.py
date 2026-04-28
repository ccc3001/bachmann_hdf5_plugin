import h5py
import json
import numpy as np
import ast
import pandas as pd
import re
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
from test_plugin.schema_packages.schema_package import NewSchemaPackage,MIOData,ACTIF2Data,ACTIFData,HP_CANData,Ploted_values,Undefined_data,NomadCamelsDataHandler_data

configuration = config.get_plugin_entry_point(
    'test_plugin.parsers:parser_entry_point'
)
def find_group_with_keys(group, keys):
    # Check current group
    if all(k in group.keys() for k in keys):
        return group

    # Recurse into subgroups
    for name, item in group.items():
        if isinstance(item, h5py.Group):
            result = find_group_with_keys(item, keys)
            if result is not None:
                return result

    return None

def parse_string(s):
    try:
        # Try JSON first
        return json.loads(s)
    except json.JSONDecodeError:
        try:
            # Fallback: Python literal (handles None, True, etc.)
            return ast.literal_eval(s)
        except Exception as e:
            raise ValueError(f"Could not parse string: {e}")

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
        nomadcamelsdatahandler_data=schema.m_create(NomadCamelsDataHandler_data)
        with h5py.File(mainfile, "r") as f:

            CAMELS_entry = next((x for x in list(f.keys()) if x.startswith("CAMELS_")), None)

            keys = [
                "NomadCamelsDataHandler_var_lengths",
                "NomadCamelsDataHandler_values_flat",
                "NomadCamelsDataHandler_var_names",
                "NomadCamelsDataHandler_timestamps_flat"
            ]

            group = find_group_with_keys(f[CAMELS_entry], keys)

            if group is not None:
                var_lengths = group["NomadCamelsDataHandler_var_lengths"][()]
                flat_values = group["NomadCamelsDataHandler_values_flat"][()]
                var_names = group["NomadCamelsDataHandler_var_names"][()]
                flat_timestamps = group["NomadCamelsDataHandler_timestamps_flat"][()]
                raw_var_names = var_names[0].decode("utf-8")
                var_names_parsed = ast.literal_eval(raw_var_names)
                counter=0
                start_point=0

                logger.info(len(var_names_parsed))

                for var_name in var_names_parsed:
                    match = re.search(r";s=(.*)", var_name)
                    if match is not None:
                        m = match.group(1)
                        m = m.split("/", 1)
                        m[1] = m[1].replace("/", "_")
                    var_name=m[1]

                    if var_lengths[0, counter]>1 and any(c.isalpha() for c in var_name):
                        data_item = nomadcamelsdatahandler_data.m_create(
                            Ploted_values,
                            NomadCamelsDataHandler_data.data
                        )

                        data_item.data=flat_values[0,start_point:(start_point-1+var_lengths[0,counter])]
                        data_item.time=flat_timestamps[0,start_point:(start_point-1+var_lengths[0,counter])]
                        data_item.name= var_name
                        if not hasattr(nomadcamelsdatahandler_data, 'start_time') or  nomadcamelsdatahandler_data.start_time is None or    nomadcamelsdatahandler_data.start_time >= data_item.time[0]:

                            nomadcamelsdatahandler_data.start_time = data_item.time[0]
                        if not hasattr(nomadcamelsdatahandler_data, 'end_time') or  nomadcamelsdatahandler_data.end_time is None or nomadcamelsdatahandler_data.start_time <= data_item.time[len(data_item.time)-1]:
                           nomadcamelsdatahandler_data.end_time= data_item.time[len(data_item.time)-1]

                    start_point+=var_lengths[0,counter]
                    counter+=1

            if "NomadCamelsDataHandler_end_collection" in f[CAMELS_entry]["data"]:
                data= f[CAMELS_entry]["data"]["NomadCamelsDataHandler_end_collection"][()]
                logger.info(len(data))
                logger.info(len(data[0]))
                parsed_data = json.loads(data[0])


                for key in parsed_data.keys():
                    match = re.search(r";s=(.*)", key)
                    if match is not None:
                        m = match.group(1)
                        m = m.split("/", 1)
                        m[1] = m[1].replace("/", "_")

                        values = parsed_data[key]["values"]
                        timestamps = parsed_data[key]["timestamps"]
                        # Check if first element is a list (2D data)
                        if isinstance(values[0], list):
                            # Convert each inner list safely
                            numeric_values = np.array(
                                [np.asarray(pd.to_numeric(inner, errors='coerce'), dtype=np.float64)
                                for inner in values],
                                dtype=np.float64
                            )
                        else:
                            # Single dimension case (1D array)
                            numeric_values = np.asarray(
                                pd.to_numeric(values, errors='coerce'),
                                dtype=np.float64
    )

                        # Convert timestamps to float array
                        numeric_timestamps = np.array(timestamps, dtype=np.float64)

                        # Create the data item
                        data_item = nomadcamelsdatahandler_data.m_create(
                            Ploted_values,
                            NomadCamelsDataHandler_data.data
                        )
                        if not hasattr(nomadcamelsdatahandler_data, 'start_time') or  nomadcamelsdatahandler_data.start_time is None or    nomadcamelsdatahandler_data.start_time >= numeric_timestamps[0]:

                            nomadcamelsdatahandler_data.start_time = numeric_timestamps[0]
                        if not hasattr(nomadcamelsdatahandler_data, 'end_time') or  nomadcamelsdatahandler_data.end_time is None or nomadcamelsdatahandler_data.start_time <= numeric_timestamps[len(numeric_timestamps)-1]:
                           nomadcamelsdatahandler_data.end_time= numeric_timestamps[len(numeric_timestamps)-1]

                        data_item.data = numeric_values
                        data_item.time = numeric_timestamps
                        data_item.name = m[1]

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
                            undef_item = mio_data.m_create(Ploted_values,MIOData.data)
                            self.set_attribute(f,undef_item,"data",[CAMELS_entry,"data",str(key)])
                            clean_name= re.sub(r"^.*MIO_", "", key)
                            undef_item.name = clean_name

                    elif key.startswith(opc_ua_instrument_name+"_HP_CAN"):
                            undef_item = hp_can_data.m_create(Ploted_values,HP_CANData.data)
                            self.set_attribute(f,undef_item,"data",[CAMELS_entry,"data",key])
                            clean_name= re.sub(r"^.*HP_CAN_", "", key)
                            undef_item.name = clean_name

                    elif key.startswith(opc_ua_instrument_name+"_ACTIF"):
                            undef_item = actif_data.m_create(Ploted_values,ACTIFData.data)
                            self.set_attribute(f,undef_item,"data",[CAMELS_entry,"data",str(key)])
                            clean_name= re.sub(r"^.*ACTIF_", "", key)
                            undef_item.name = clean_name


                    elif key.startswith(opc_ua_instrument_name+"_ACTIF2"):
                            undef_item = actif2_data.m_create(Ploted_values,ACTIF2Data.data)
                            self.set_attribute(f,undef_item,"data",[CAMELS_entry,"data",str(key)])
                            clean_name= re.sub(r"^.*ACTIF2_", "", key)
                            undef_item.name = clean_name

                    else:
                        try:
                            undef_item = undef_data.m_create(Ploted_values,Undefined_data.data)
                            self.set_attribute(f,undef_item,"data",[CAMELS_entry,"data",str(key)])
                            undef_item.name = key
                        except:
                            logger.info("could not create element for:"+key)

                else:

                    try:
                        if key not in ["ElapsedTime","time"]:
                            undef_item = undef_data.m_create(Ploted_values,Undefined_data.data)
                            self.set_attribute(f,undef_item,"data",[CAMELS_entry,"data",str(key)])
                            undef_item.name = key
                    except:
                        logger.info("could not create element for:"+key)
        archive.data=schema
        logger.info("h5 was read propperly")
        logger.info(str(os.getcwd()))
