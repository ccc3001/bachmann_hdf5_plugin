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

from nomad.datamodel.hdf5 import HDF5Reference


def create_parsed_dataset(
    archive,
    values,
    start,
    length,
    dataset_path,
):
    data = values[start:start + length]

    HDF5Reference.write_dataset(
        archive,
        data,
        dataset_path,
    )

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
        datasets_to_write = []
        with h5py.File(mainfile, "r") as f:

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
                logger.info(f"values_ds.shape = {values_ds.shape}")
                logger.info(f"times_ds.shape = {times_ds.shape}")
                logger.info(f"values_ds.dtype = {values_ds.dtype}")
                logger.info(f"times_ds.dtype = {times_ds.dtype}")
                if values_ds.ndim == 2:
                    all_values = values_ds[0]
                else:
                    all_values = values_ds
                # Normalize to a 1D array
                if times_ds.ndim == 2:
                    all_times = times_ds[0]
                else:
                    all_times = times_ds

                # Normalize timestamps
                if all_times.dtype.kind in ("S", "U", "O"):
                    raw = all_times.reshape(-1)[0]

                    if isinstance(raw, bytes):
                        raw = raw.decode()

                    # Serialized list?
                    if raw.startswith("["):
                        all_times = np.array(ast.literal_eval(raw), dtype=np.float64)
                    else:
                        all_times = np.asarray(all_times, dtype=np.float64)

                experiment_start = np.min(all_times)
                var_lengths = group["NomadCamelsDataHandler_var_lengths"][()]

                logger.info(f"var_lengths type = {type(var_lengths)}")
                logger.info(f"var_lengths shape = {getattr(var_lengths, 'shape', None)}")


                # Convert to a simple 1D integer array
                if var_lengths.dtype.kind in ("S", "U", "O"):
                    raw = var_lengths.reshape(-1)[0]

                    if isinstance(raw, bytes):
                        raw = raw.decode()

                    var_lengths = np.array(ast.literal_eval(raw), dtype=int)

                else:
                    var_lengths = np.asarray(var_lengths).reshape(-1).astype(int)

                logger.info(f"len(var_lengths) = {len(var_lengths)}")
                logger.info(f"sum(var_lengths) = {var_lengths.sum()}")
                var_names = group["NomadCamelsDataHandler_var_names"][()]

                if var_names.dtype == object:
                    var_names = var_names[0]

                elif var_names.ndim == 2:
                    var_names = var_names[0]

                elif var_names.ndim == 1:
                    pass

                else:
                    raise ValueError(
                        f"Unsupported var_names shape: {var_names.shape}"
                    )

                var_names = [
                    n.decode() if isinstance(n, bytes) else str(n)
                    for n in var_names
                ]

                logger.info(f"len(var_names) = {len(var_names)}")
                logger.info(f"first names = {var_names[:5]}")

                start_point = 0

                for counter, var_name in enumerate(var_names):

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

                    if var_lengths.ndim == 1:
                        length = int(var_lengths[counter])

                    elif var_lengths.ndim == 2:
                        length = int(var_lengths[0, counter])

                    else:
                        raise ValueError(
                            f"Unsupported var_lengths shape: {var_lengths.shape}"
                        )

                    logger.info(
                        f"{counter}: "
                        f"name={var_name}, "
                        f"start={start_point}, "
                        f"length={length}, "
                        f"end={start_point + length}"
                    )
                    logger.info(
                        f"value slice length = "
                        f"{len(all_values[start_point:start_point + length])}"
                    )

                    logger.info(
                        f"time slice length = "
                        f"{len(all_times[start_point:start_point + length])}"
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


                        safe_name = re.sub(r"[^\w.-]", "_", var_name)

                        group_path = f"/parsed/{safe_name}"

                        values_path = f"{group_path}/values"
                        time_path = f"{group_path}/time"

                        datasets_to_write.append(
                            {
                                "values_path": values_path,
                                "time_path": time_path,
                                "values": all_values[start_point:start_point + length],
                                "times": all_times[start_point:start_point + length]-experiment_start,
                            }
                        )
                        data_item.data = f"{raw_name}#{values_path}"
                        data_item.time = f"{raw_name}#{time_path}"
                    start_point += length
            logger.info("===== FINAL CHECK =====")
            if "start_point" in locals():
                logger.info(f"final start_point = {start_point}")
            else:
                logger.info("start_point was never initialized")

            if "all_values" in locals():
                logger.info(f"len(all_values) = {len(all_values)}")
            else:
                logger.info("all_values was never initialized")

            if "all_times" in locals():
                logger.info(f"len(all_times) = {len(all_times)}")
            else:
                logger.info("start_point was never initialized")
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
        for ds in datasets_to_write:
            logger.info(f"Writing to {raw_name}#{ds['values_path']}")
            logger.info(f"values shape = {ds['values'].shape}")
            HDF5Reference.write_dataset(
                archive,
                ds["values"],
                f"{raw_name}#{ds['values_path']}"
            )

            HDF5Reference.write_dataset(
                archive,
                ds["times"],
                f"{raw_name}#{ds['time_path']}"
            )
        with h5py.File(mainfile, "r+") as f:

            for ds in datasets_to_write:

                group_path = os.path.dirname(ds["values_path"])

                grp = f[group_path]

                grp.attrs["NX_class"] = "NXdata"
                grp.attrs["signal"] = "values"
                grp.attrs["axes"] = "time"
        archive.data = schema

        logger.info(
            "h5 read successfully"
        )


