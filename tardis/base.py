# functions that are important for the general usage of TARDIS

import logging


logger = logging.getLogger(__name__)


def run_tardis(
    config,
    atom_data=None,
    packet_source=None,
    simulation_callbacks=[],
    virtual_packet_logging=False,
    log_level=None,
    specific=None,
):
    """
    This function is one of the core functions to run TARDIS from a given
    config object.

    It will return a model object containing

    Parameters
    ----------
    config : str or dict or tardis.io.config_reader.Configuration
        filename of configuration yaml file or dictionary or TARDIS Configuration object
    atom_data : str or tardis.atomic.AtomData
        if atom_data is a string it is interpreted as a path to a file storing
        the atomic data. Atomic data to use for this TARDIS simulation. If set to None, the
        atomic data will be loaded according to keywords set in the configuration
        [default=None]
    virtual_packet_logging : bool
        option to enable virtual packet logging
        [default=False]

    Returns
    -------
    Simulation
    """
    from tardis.io.logger.logger import logging_state
    from tardis.io.config_reader import Configuration
    from tardis.io.atom_data.base import AtomData
    from tardis.simulation import Simulation

    if isinstance(config, Configuration):
        tardis_config = config
    else:
        try:
            tardis_config = Configuration.from_yaml(config)
        except TypeError:
            logger.debug(
                "TARDIS Config not available via YAML. Reading through TARDIS Config Dictionary"
            )
            tardis_config = Configuration.from_config_dict(config)

    logging_state(log_level, tardis_config, specific)

    if atom_data is not None:
        try:
            atom_data = AtomData.from_hdf(atom_data)
        except TypeError:
            logger.debug(
                "Atom Data Cannot be Read from HDF. Setting to Default Atom Data"
            )
            atom_data = atom_data

    simulation = Simulation.from_config(
        tardis_config,
        packet_source=packet_source,
        atom_data=atom_data,
        virtual_packet_logging=virtual_packet_logging,
    )
    for cb in simulation_callbacks:
        simulation.add_callback(*cb)

    simulation.run()

    return simulation
