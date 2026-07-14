import h5py
import re
import os
from datetime import datetime
import ast
from nomad.datamodel.datamodel import EntryArchive
from structlog.stdlib import BoundLogger
from nomad.config import config
from nomad.parsing.parser import MatchingParser
from nomad.datamodel.hdf5 import HDF5Wrapper
from test_plugin.schema_packages.schema_package import (
    NewSchemaPackage,
    MIOData,
    ACTIF2Data,
    ACTIFData,
    HP_CANData,
    Ploted_values,
    Undefined_data,
    NomadCamelsDataHandler_data,
)

configuration = config.get_plugin_entry_point(
    'test_plugin.parsers:parser_entry_point'
)


import json

import ast
import numpy as np
import h5py
import re


def find_group_with_keys(group, keys):
    if all(k in group.keys() for k in keys):
        return group
    for _, item in group.items():
        if isinstance(item, h5py.Group):
            result = find_group_with_keys(item, keys)
            if result is not None:
                return result
    return None

def create_parsed_dataset(
    h5file,
    values,
    start,
    length,
    dataset_path,
):
    data = values[start:start + length]

    if dataset_path in h5file:
        del h5file[dataset_path]

    h5file.create_dataset(dataset_path, data=data)

class NewParser(MatchingParser):

    def parse(
        self,
        mainfile: str,
        archive: EntryArchive,
        logger: BoundLogger,
    ) -> None:

        schema = NewSchemaPackage()

        mio_data = schema.m_create(MIOData)
        actif2_data = schema.m_create(ACTIF2Data)
        actif_data = schema.m_create(ACTIFData)
        hp_can_data = schema.m_create(HP_CANData)
        undef_data = schema.m_create(Undefined_data)
        nomadcamelsdatahandler_data = schema.m_create(
            NomadCamelsDataHandler_data
        )

        raw_name = os.path.basename(mainfile)

        schema.file_name = os.path.splitext(
            raw_name
        )[0]

        schema.date = datetime.today().strftime(
            '%Y-%m-%d'
        )

        with h5py.File(mainfile, "r+") as f:

            CAMELS_entry = list(f.keys())[0]

            # -------------------------
            # CAMELS flattened datasets
            # -------------------------

            keys = [
                "NomadCamelsDataHandler_var_lengths",
                "NomadCamelsDataHandler_values_flat",
                "NomadCamelsDataHandler_var_names",
                "NomadCamelsDataHandler_timestamps_flat"
            ]

            group = find_group_with_keys(
                f[CAMELS_entry],
                keys
            )

            if group is not None:
                values_ds = group["NomadCamelsDataHandler_values_flat"][()]
                times_ds = group["NomadCamelsDataHandler_timestamps_flat"][()]

                logger.info(f"values dataset shape = {values_ds.shape}")
                logger.info(f"times dataset shape = {times_ds.shape}")

                # Normalize to a 1D array
                if values_ds.ndim == 2:
                    all_values = values_ds[0]
                else:
                    all_values = values_ds

                if times_ds.ndim == 2:
                    all_times = times_ds[0]
                else:
                    all_times = times_ds
                var_lengths = group[
                    "NomadCamelsDataHandler_var_lengths"
                ][()]

                # Handle serialized list stored as bytes
                if len(var_lengths) == 1 and isinstance(var_lengths[0], (bytes, str)):
                    raw = var_lengths[0]
                    if isinstance(raw, bytes):
                        raw = raw.decode("utf-8")
                    var_lengths = ast.literal_eval(raw)


                var_names = group[
                    "NomadCamelsDataHandler_var_names"
                ][()]

                # Handle serialized list stored as bytes
                if (
                    len(var_names) == 1
                    and isinstance(var_names[0], (bytes, str))
                ):
                    raw = var_names[0]
                    if isinstance(raw, bytes):
                        raw = raw.decode("utf-8")
                    var_names = ast.literal_eval(raw)

                # Otherwise convert NumPy array to a Python list
                elif isinstance(var_names, np.ndarray):
                    var_names = var_names.tolist()

                counter = 0
                start_point = 0

                for var_name in var_names:

                    # Normalize to a Python string
                    if isinstance(var_name, bytes):
                        var_name = var_name.decode("utf-8")
                    else:
                        var_name = str(var_name)

                    match = re.search(
                        r";s=(.*)",
                        var_name
                    )

                    if match is not None:
                        m = match.group(1)
                        m = m.split("/", 1)
                        m[1] = m[1].replace(
                            "/",
                            "_"
                        )
                        var_name = m[1]

                    length = int(
                        var_lengths[0,counter]
                    )

                    if (
                        length > 1
                        and any(
                            c.isalpha()
                            for c in var_name
                        )
                    ):

                        data_item = (
                            nomadcamelsdatahandler_data
                            .m_create(
                                Ploted_values,
                                NomadCamelsDataHandler_data.data
                            )
                        )

                        data_item.name = var_name

                        # IMPORTANT FIX:
                        # point to sliced data, not full flat arrays

                        data_item.slice_start = (
                            start_point
                        )

                        data_item.slice_end = (
                            start_point + length
                        )

                        safe_name = re.sub(r"[^\w.-]", "_", var_name)

                        values_path = f"/parsed/values/{safe_name}"
                        time_path = f"/parsed/time/{safe_name}"

                        create_parsed_dataset(
                            f,
                            all_values,
                            start_point,
                            length,
                            values_path,
                        )

                        create_parsed_dataset(
                            f,
                            all_times,
                            start_point,
                            length,
                            time_path,
                        )

                        logger.info(f"{f[values_path].shape=}")
                        logger.info(f"{f[time_path].shape=}")
                        logger.info(f"{f[values_path].dtype=}")
                        logger.info(f"{f[time_path].dtype=}")
                        data_item.data = f"{raw_name}#{values_path}"
                        data_item.time = f"{raw_name}#{time_path}"
                    start_point += length
                    counter += 1

            # -------------------------
            # instrument datasets
            # -------------------------

            opc_ua_instrument_name = None

            if "instruments" in f[CAMELS_entry]:

                for key in f[
                    CAMELS_entry
                ]["instruments"]:

                    if (
                        "opc" in key
                        and "ua" in key
                    ):
                        opc_ua_instrument_name = str(
                            key
                        )

            time_path = None

            if (
                "time"
                in f[CAMELS_entry]["data"]
            ):
                time_path = f[
                    CAMELS_entry
                ]["data"]["time"].name

            for key in f[CAMELS_entry]["data"]:

                if key in [
                    "ElapsedTime",
                    "time"
                ]:
                    continue

                dataset_path = f[
                    CAMELS_entry
                ]["data"][key].name

                try:

                    if (
                        opc_ua_instrument_name
                        and key.startswith(
                            opc_ua_instrument_name
                        )
                    ):

                        if "_MIO_" in key:

                            item = mio_data.m_create(
                                Ploted_values,
                                MIOData.data
                            )

                        elif "_HP_CAN_" in key:

                            item = hp_can_data.m_create(
                                Ploted_values,
                                HP_CANData.data
                            )

                        elif "_ACTIF2_" in key:

                            item = actif2_data.m_create(
                                Ploted_values,
                                ACTIF2Data.data
                            )

                        elif "_ACTIF_" in key:

                            item = actif_data.m_create(
                                Ploted_values,
                                ACTIFData.data
                            )

                        else:

                            item = undef_data.m_create(
                                Ploted_values,
                                Undefined_data.data
                            )

                    else:

                        item = undef_data.m_create(
                            Ploted_values,
                            Undefined_data.data
                        )

                    item.name = key

                    item.data = (
                        f"{raw_name}#"
                        f"{dataset_path}"
                    )



                    if time_path is not None:

                        item.time = (
                            f"{raw_name}#"
                            f"{time_path}"
                        )

                except Exception as e:

                    logger.info(
                        f"could not create element "
                        f"for {key}: {e}"
                    )

        archive.data = schema

        logger.info(
            "h5 read successfully"
        )


