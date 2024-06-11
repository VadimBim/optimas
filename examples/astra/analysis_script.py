"""Defines the analysis function that runs after the simulation.

This is an example calculation of the bunch length in µm, a combined
normalized transverse emittance, and the emittances in both transverse planes.
"""

import numpy as np


# Function to analyze the simulation result
def analyze_simulation(simulation_directory, output_params):
    """Analyze the simulation output.

    This method analyzes the output generated by the simulation to
    obtain the value of the optimization objective and other analyzed
    parameters, if specified. The value of these parameters has to be
    given to the `output_params` dictionary.

    Parameters
    ----------
    simulation_directory : str
        Path to the simulation folder where the output was generated.
    output_params : dict
        Dictionary where the value of the objectives and analyzed parameters
        will be stored. There is one entry per parameter, where the key
        is the name of the parameter given by the user.

    Returns
    -------
    dict
        The `output_params` dictionary with the results from the analysis.

    """
    try:
        # Read back results from files
        s, t, x_av, x_rms, xp_rms, em_n_x, x_xp = np.loadtxt(
            simulation_directory + "/ASTRA_example.Xemit.001", unpack=True
        )
        s, t, y_av, y_rms, yp_rms, em_n_y, y_yp = np.loadtxt(
            simulation_directory + "/ASTRA_example.Yemit.001", unpack=True
        )
        x, y, z, px, py, pz, t, charge, idx, flag = np.loadtxt(
            simulation_directory + "/ASTRA_example.0250.001", unpack=True
        )
        z[1:] = z[1:] + z[0]  # adding the position of the reference particle

        output_params["bunch_length"] = np.std(z) * 1e6
        output_params["emittance"] = np.log10(
            em_n_x[-1] * em_n_y[-1] * 1e12
        )  # normalized emittances in µm, logarithm for better optimization
        output_params["emittance_x"] = em_n_x[-1]
        output_params["emittance_y"] = em_n_y[-1]
    except Exception as exc:
        logf = open("exception.log", "w")
        logf.write(
            "Failed to open or evaluate {0}: {1}\n".format(
                str(simulation_directory), str(exc)
            )
        )
    return output_params


# Not needed, for debugging only
if __name__ == "__main__":
    analyze_simulation("path_to_simulation_result", {})