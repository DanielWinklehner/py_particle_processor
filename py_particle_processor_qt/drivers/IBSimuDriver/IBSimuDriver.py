from ..arraywrapper import ArrayWrapper
from ..abstractdriver import AbstractDriver
from dans_pymodules import IonSpecies, ParticleDistribution
import numpy as np
import scipy.constants as const
from PyQt5.QtWidgets import QInputDialog


amu_kg = const.value("atomic mass constant")  # (kg)
amu_mev = const.value("atomic mass constant energy equivalent in MeV")  # (MeV)
clight = const.value("speed of light in vacuum")  # (m/s)


class IBSimuDriver(AbstractDriver):
    def __init__(self, parent=None, debug=False):
        super(IBSimuDriver, self).__init__()
        # IBSimu particle file: I (A), M (kg), t, x (m), vx (m/s), y (m), vy (m/s), z (m), vz (m/s)

        self._debug = debug
        self._program_name = "IBSimu"
        self._parent = parent

    def import_data(self, filename, species):

        # TODO: There is a lot of looping going on, the fewer instructions the better. -PW

        if self._debug:
            print("Importing data from program: {}".format(self._program_name))

        try:

            datasource = {}
            data = {}

            with open(filename, 'rb') as infile:

                lines = infile.readlines()

            npart = len(lines)

            current = np.empty(npart)
            mass = np.empty(npart)
            x = np.empty(npart)
            y = np.empty(npart)
            z = np.empty(npart)
            vx = np.empty(npart)
            vy = np.empty(npart)
            vz = np.empty(npart)

            for i, line in enumerate(lines):
                current[i], mass[i], _, x[i], vx[i], y[i], vy[i], z[i], vz[i] = [float(item) for item in
                                                                                 line.strip().split()]

            masses = np.sort(np.unique(mass))  # mass in MeV, sorted in ascending order (protons before h2+)

            particle_distributions = []

            for i, m in enumerate(masses):

                m_mev = m / amu_kg * amu_mev

                species_indices = np.where((mass == m) & (vz > 5.0e5))  # TODO: v_z selection should be in IBSimu -DW

                ion = IonSpecies("Species {}".format(i + 1),
                                 mass_mev=m_mev,
                                 a=m_mev / amu_mev,
                                 z=np.round(m_mev / amu_mev, 0),
                                 q=1.0,
                                 current=np.sum(current[species_indices]),
                                 energy_mev=1)  # Note: Set energy to 1 for now, will be recalculated

                # ParticleDistribution corretly calculates the mean energy
                particle_distributions.append(
                    ParticleDistribution(ion=ion,
                                         x=x[species_indices],
                                         y=y[species_indices],
                                         z=z[species_indices],
                                         vx=vx[species_indices],
                                         vy=vy[species_indices],
                                         vz=vz[species_indices]
                                         ))

                print(particle_distributions[-1].calculate_emittances()["summary"])

            n_species = len(particle_distributions)

            if n_species > 1:

                items = []
                for dist in particle_distributions:
                    items.append("a = {:.5f}, q = {:.1f}".format(dist.ion.a(), dist.ion.q()))

                item, ok = QInputDialog.getItem(self._parent,
                                                "IBSimu Import",
                                                "Found {} ion species, which one do you want?".format(n_species),
                                                items, 0, False)

                index = np.where(np.array(items) == item)[0][0]

            else:

                index = 0

            pd = particle_distributions[index]
            species = pd.ion
            npart = len(pd.x)

            step_str = "Step#{}".format(0)
            datasource[step_str] = {}
            datasource[step_str]["x"] = ArrayWrapper(pd.x)
            datasource[step_str]["y"] = ArrayWrapper(pd.y)
            datasource[step_str]["z"] = ArrayWrapper(pd.z)
            datasource[step_str]["px"] = ArrayWrapper(pd.vx/clight / np.sqrt(1.0 - (pd.vx/clight)**2.0))
            datasource[step_str]["py"] = ArrayWrapper(pd.vy/clight / np.sqrt(1.0 - (pd.vy/clight)**2.0))
            datasource[step_str]["pz"] = ArrayWrapper(pd.vz/clight / np.sqrt(1.0 - (pd.vz/clight)**2.0))
            v_mean_sq = pd.vx**2.0 + pd.vy**2.0 + pd.vz**2.0
            datasource[step_str]["E"] = ArrayWrapper(
                (1.0 / np.sqrt(1.0 - (v_mean_sq / clight ** 2.0)) - 1.0) * species.mass_mev())

            data["datasource"] = datasource
            data["ion"] = species
            data["energy"] = species.energy_mev() * species.a()
            data["mass"] = species.a()
            data["charge"] = species.q()
            data["steps"] = 1
            data["current"] = species.current()
            data["particles"] = npart

            if self._debug:
                print("Found {} steps in the file.".format(data["steps"]))
                print("Found {} particles in the file.".format(data["particles"]))

            return data

        except Exception as e:

            print("Exception happened during particle loading with {} "
                  "ImportExportDriver: {}".format(self._program_name, e))

        return None

        # try:
        #
        #     datasource = {}
        #     data = {}
        #
        #     with open(filename, 'rb') as infile:
        #
        #         _n = 7  # Length of the n-tuples to unpack from the values list
        #         key_list = ["x", "y", "z", "px", "py", "pz", "E"]  # Things we want to save
        #
        #         firstline = infile.readline()
        #         lines = infile.readlines()
        #         raw_values = [float(item) for item in firstline.strip().split()]
        #         nsteps = int((len(raw_values) - 1) / _n)  # Number of steps
        #         npart = len(lines) + 1
        #
        #         # Fill in the values for the first line now
        #         _id = int(raw_values.pop(0))
        #
        #         for step in range(nsteps):
        #             step_str = "Step#{}".format(step)
        #
        #             datasource[step_str] = {}
        #
        #             for key in key_list:
        #                 datasource[step_str][key] = ArrayWrapper(np.zeros(npart))
        #
        #             values = raw_values[(step * _n):(_n + step * _n)]
        #
        #             gamma = values[6] / species.mass_mev() + 1.0
        #             beta = np.sqrt(1.0 - np.power(gamma, -2.0))
        #             v_tot = np.sqrt(values[3] ** 2.0 + values[4] ** 2.0 + values[5] ** 2.0)
        #
        #             values[0:3] = [r for r in values[0:3]]
        #             values[3:6] = [beta * gamma * v / v_tot for v in values[3:6]]  # Convert velocity to momentum
        #
        #             for idx, key in enumerate(key_list):
        #                 datasource[step_str][key][_id - 1] = values[idx]
        #
        #         # Now for every other line
        #         for line in lines:
        #
        #             raw_values = [float(item) for item in line.strip().split()]  # Data straight from the text file
        #             _id = int(raw_values.pop(0))  # Particle ID number
        #
        #             for step in range(nsteps):
        #                 step_str = "Step#{}".format(step)
        #                 values = raw_values[(step * _n):(_n + step * _n)]
        #
        #                 gamma = values[6] / species.mass_mev() + 1.0
        #                 beta = np.sqrt(1.0 - gamma ** (-2.0))
        #                 v_tot = np.sqrt(values[3] ** 2.0 + values[4] ** 2.0 + values[5] ** 2.0)
        #
        #                 values[0:3] = [r for r in values[0:3]]
        #                 values[3:6] = [beta * gamma * v / v_tot for v in values[3:6]]  # Convert velocity to momentum
        #
        #                 for idx, key in enumerate(key_list):
        #                     datasource[step_str][key][_id - 1] = values[idx]
        #
        #         species.calculate_from_energy_mev(datasource["Step#0"]["E"][0])
        #
        #         data["datasource"] = datasource
        #         data["ion"] = species
        #         data["mass"] = species.a()
        #         data["charge"] = species.q()
        #         data["steps"] = len(datasource.keys())
        #         data["current"] = None
        #         data["particles"] = len(datasource["Step#0"]["x"])
        #
        #         if self._debug:
        #             print("Found {} steps in the file.".format(data["steps"]))
        #             print("Found {} particles in the file.".format(data["particles"]))
        #
        #         return data
        #
        # except Exception as e:
        #
        #     print("Exception happened during particle loading with {} "
        #           "ImportExportDriver: {}".format(self._program_name, e))
        #
        # return None

    def export_data(self, dataset, filename):

        print("Sorry, exporting not implemented yet!")
        # if self._debug:
        #     print("Exporting data for program: {}".format(self._program_name))
        #
        # datasource = dataset.get_datasource()
        # ion = dataset.get_ion()
        # nsteps = dataset.get_nsteps()
        # npart = dataset.get_npart()
        #
        # with open(filename + ".txt", "w") as outfile:
        #     for i in range(npart):
        #         outstring = "{} ".format(i)
        #         for step in range(nsteps):
        #             _px = datasource.get("Step#{}".format(step)).get("px")[i]
        #             _py = datasource.get("Step#{}".format(step)).get("py")[i]
        #             _pz = datasource.get("Step#{}".format(step)).get("pz")[i]
        #
        #             _vx, _vy, _vz = (clight * _px / np.sqrt(_px ** 2.0 + 1.0),
        #                              clight * _py / np.sqrt(_py ** 2.0 + 1.0),
        #                              clight * _pz / np.sqrt(_pz ** 2.0 + 1.0))
        #
        #             outstring += "{} {} {} {} {} {} {} ".format(datasource.get("Step#{}".format(step)).get("x")[i],
        #                                                      datasource.get("Step#{}".format(step)).get("y")[i],
        #                                                      datasource.get("Step#{}".format(step)).get("z")[i],
        #                                                      _vx, _vy, _vz, ion.energy_mev())
        #         outfile.write(outstring + "\n")
