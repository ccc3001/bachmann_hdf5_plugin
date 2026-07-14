from nomad.config import config
from nomad.datamodel.data import ArchiveSection
from nomad.metainfo import (
    Quantity,
    SchemaPackage,
    Section,
    SubSection,
    SectionProxy,
)
from nomad.datamodel.hdf5 import (
    HDF5Reference,
    H5WebAnnotation,
    HDF5Dataset
)
import numpy as np

configuration = config.get_plugin_entry_point(
    'test_plugin.schema_packages:schema_package_entry_point'
)

m_package = SchemaPackage()


class Ploted_values(ArchiveSection):

    m_def = Section(
        a_h5web=H5WebAnnotation(
            signal='data',
            #axes=['time'],
        )
    )

    name = Quantity(type=str)

    data = Quantity(
        type=HDF5Reference
    )

    time = Quantity(
        type=HDF5Reference
    )


class MIOData(ArchiveSection):
    data = SubSection(
        section=SectionProxy("Ploted_values"),
        repeats=True
    )


class ACTIFData(ArchiveSection):
    data = SubSection(
        section=SectionProxy("Ploted_values"),
        repeats=True
    )


class ACTIF2Data(ArchiveSection):
    data = SubSection(
        section=SectionProxy("Ploted_values"),
        repeats=True
    )


class HP_CANData(ArchiveSection):
    data = SubSection(
        section=SectionProxy("Ploted_values"),
        repeats=True
    )


class Undefined_data(ArchiveSection):
    data = SubSection(
        section=SectionProxy("Ploted_values"),
        repeats=True
    )


class NomadCamelsDataHandler_data(ArchiveSection):

    m_def = Section(
        a_h5web=H5WebAnnotation(
            paths=["data/*"]
        )
    )

    data = SubSection(
        section=SectionProxy("Ploted_values"),
        repeats=True
    )

class NewSchemaPackage(ArchiveSection):

    nomadcamelsdatahandler_data = SubSection(
        section=SectionProxy(
            "NomadCamelsDataHandler_data"
        )
    )

    undef_data = SubSection(
        section=SectionProxy("Undefined_data")
    )

    mio_data = SubSection(
        section=SectionProxy("MIOData")
    )

    actif_data = SubSection(
        section=SectionProxy("ACTIFData")
    )

    actif2_data = SubSection(
        section=SectionProxy("ACTIF2Data")
    )

    hp_can_data = SubSection(
        section=SectionProxy("HP_CANData")
    )

    file_name = Quantity(type=str)
    date = Quantity(type=str)

m_package.__init_metainfo__()