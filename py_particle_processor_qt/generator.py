import numpy as np
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow
from py_particle_processor_qt.gui.generate_main import Ui_Generate_Main
from py_particle_processor_qt.gui.generate_error import Ui_Generate_Error
from py_particle_processor_qt.gui.generate_envelope import Ui_Generate_Envelope
from py_particle_processor_qt.gui.generate_twiss import Ui_Generate_Twiss
from dans_pymodules import IonSpecies


class GenerateDistribution(object):
    """
    A generator for creating various particle distributions.
    """

    def __init__(self, numpart, species, energy, z_pos="Zero", z_mom="Zero", rz=0.0, ez=0.0, stddev=1.0):
        if isinstance(numpart, str): numpart = int(numpart)
        if isinstance(energy, str): energy = float(energy)
        if isinstance(rz, str): rz = float(rz)
        if ez == "":
            ez = 0.0
        elif isinstance(ez, str):
            ez = float(ez)
        if stddev == "":
            stddev = 1.0
        elif isinstance(stddev, str):
            numpart = float(stddev)
        self._numpart = numpart  # number of particles
        self._species = IonSpecies(species, energy)  # instance of IonSpecies
        self._data = None  # A variable to store the data dictionary

        rzp = self._species.v_m_per_s() * 1e-03  # Should this be 1e-03 (original) or 1e03?

        # Calculate longitudinal position distribution
        z = np.zeros(self._numpart)
        if z_pos == "Constant":  # Constant z-position
            z = np.full(self._numpart, rz)
        elif z_pos == "Uniform along length":  # Randomly distributed z-position
            z = (np.random.random(self._numpart) - 0.5) * rz
        elif z_pos == "Uniform on ellipse":  # Uniformly randomly distributed within an ellipse
            beta = 2 * np.pi * np.random.random(self._numpart)
            a = np.ones(self._numpart)
            rand_phi = np.random.random(self._numpart)
            a_z = a * np.sqrt(rand_phi)
            z = a_z * rz * np.cos(beta)
        elif z_pos == "Gaussian on ellipse":  # Gaussian distribution within an ellipse
            rand = np.random.normal(0, stddev, self._numpart)
            z = rand * rz * .5
        elif z_pos == "Waterbag":  # Waterbag distribution within an ellipse
            beta = 2 * np.pi * np.random.random(self._numpart)
            a = np.sqrt(1.5 * np.sqrt(np.random.random(self._numpart)))
            rand_phi = np.random.random(self._numpart)
            a_z = a * np.sqrt(rand_phi)
            z = a_z * rz * np.cos(beta)
        elif z_pos == "Parabolic":  # Parabolic distribution within an ellipse
            beta = 2 * np.pi * np.random.random(self._numpart)
            alpha = np.arccos(1.0 - 2 * np.random.random(self._numpart))
            a = np.sqrt(1.0 - 2 * np.cos((alpha - 2.0 * np.pi) / 3))
            rand_phi = np.random.random(self._numpart)
            a_z = a * np.sqrt(rand_phi)
            z = a_z * rz * np.cos(beta)

        # Calculate longitudinal momentum distribution
        zp = np.zeros(self._numpart)
        if z_mom == "Constant":
            zp = np.full(self._numpart, rzp)
        elif z_mom == "Uniform along length":
            zp = (np.random.random(self._numpart) - 0.5) * rzp
        elif z_mom == "Uniform on ellipse":
            beta = 2 * np.pi * np.random.random(self._numpart)
            a = np.ones(self._numpart)
            rand_phi = np.random.random(self._numpart)
            a_z = a * np.sqrt(rand_phi)
            zp = a_z * (rzp * np.cos(beta) - (ez / rz) * np.sin(beta))
        elif z_mom == "Gaussian on ellipse":
            z_rand = np.random.normal(0, stddev, self._numpart)
            zp_rand = np.random.normal(0, stddev, self._numpart)
            z_temp = z_rand * rz * .5
            zp = (rzp / rz) * z_temp + (ez / (2 * rz)) * zp_rand

        self._z = z
        self._zp = np.abs(zp)

    # Functions for generating x-x', y-y' distributions and returning step 0 of the dataset

    def generate_uniform(self, r, rp, e_normalized):
        """
        Generates a uniform distribution using the beam envelope's angle and radius.
        :param r: envelope radius in the shape of array [rx, ry] (mm)
        :param rp: envelope angle in the shape of array [rxp, ryp] (mrad)
        :param e_normalized: normalized rms emittance in the shape of array [ex, ey](pi-mm-mrad)
        :return:
        """

        # Initialize parameters
        rx = float(r[0])
        rxp = float(rp[0])
        ry = float(r[1])
        ryp = float(rp[1])
        e_normalized = [float(e_normalized[0]), float(e_normalized[1])]
        ion = self._species
        emittance = np.array(e_normalized) / ion.gamma() / ion.beta()  # mm-mrad - non-normalized, rms emittance

        # Initialize random variables
        a = np.ones(self._numpart)
        beta_x = 2 * np.pi * np.random.random(self._numpart)
        beta_y = 2 * np.pi * np.random.random(self._numpart)
        rand_phi = np.random.random(self._numpart)

        # Calculate distribution
        a_x = a * np.sqrt(rand_phi)
        a_y = a * np.sqrt(1 - rand_phi)
        x = a_x * rx * np.cos(beta_x)
        xp = a_x * (rxp * np.cos(beta_x) - (emittance[0] / rx) * np.sin(beta_x))
        y = a_y * ry * np.cos(beta_y)
        yp = a_y * (ryp * np.cos(beta_y) - (emittance[1] / ry) * np.sin(beta_y))

        # Correct for z-position
        x = x + self._z * xp
        y = y + self._z * yp

        data = {'Step#0': {'x': np.array(x),
                           'px': np.array(ion.gamma() * ion.beta() * xp),
                           'y': np.array(y),
                           'py': np.array(ion.gamma() * ion.beta() * yp),
                           'z': np.array(self._z),
                           'pz': np.array(ion.gamma() * ion.beta() * self._zp),
                           'id': range(self._numpart + 1),
                           'attrs': 0}}

        return data

    def generate_gaussian(self, r, rp, e_normalized, stddev):
        """
        Generates a Gaussian distribution using the beam envelope's angle and radius.
        :param r: envelope radius in the shape of array [rx, ry] (mm)
        :param rp: envelope angle in the shape of array [rxp, ryp] (mrad)
        :param e_normalized: normalized rms emittance in the shape of array [ex, ey](pi-mm-mrad)
        :param stddev: standard deviation for all parameters
        :return:
        """

        # Initialize parameters
        r0x = float(r[0])
        a0x = float(rp[0])
        r0y = float(r[1])
        a0y = float(rp[1])
        stddev = float(stddev)
        e_normalized = [float(e_normalized[0]), float(e_normalized[1])]
        ion = self._species
        emittance = np.array(e_normalized) / ion.gamma() / ion.beta()  # mm-mrad - non-normalized, rms emittance

        # Initialize random variables
        x_rand = np.random.normal(0, stddev, self._numpart)
        y_rand = np.random.normal(0, stddev, self._numpart)
        xp_rand = np.random.normal(0, stddev, self._numpart)
        yp_rand = np.random.normal(0, stddev, self._numpart)

        # Calculate distribution
        x = x_rand * r0x * .5
        xp = (a0x / r0x) * x + (emittance[0] / (2 * r0x)) * xp_rand
        y = y_rand * r0y * .5
        yp = (a0y / r0y) * y + (emittance[1] / (2 * r0y)) * yp_rand

        # Correct for z-position
        x = x + self._z * xp
        y = y + self._z * yp

        data = {'Step#0': {'x': np.array(x),
                           'px': np.array(ion.gamma() * ion.beta() * xp),
                           'y': np.array(y),
                           'py': np.array(ion.gamma() * ion.beta() * yp),
                           'z': np.array(self._z),
                           'pz': np.array(ion.gamma() * ion.beta() * self._zp),
                           'id': range(self._numpart + 1),
                           'attrs': 0}}

        return data

    def generate_waterbag(self, r, rp, e_normalized):
        """
        Generates a waterbag distribution using the beam envelope's angle and radius.
        :param r: envelope radius in the shape of array [rx, ry] (mm)
        :param rp: envelope angle in the shape of array [rxp, ryp] (mrad)
        :param e_normalized: normalized rms emittance in the shape of array [ex, ey](pi-mm-mrad)
        :return:
        """

        # Initialize parameters
        rx = float(r[0])
        rxp = float(rp[0])
        ry = float(r[1])
        ryp = float(rp[1])
        e_normalized = [float(e_normalized[0]), float(e_normalized[1])]
        ion = self._species
        emittance = np.array(e_normalized) / ion.gamma() / ion.beta()  # mm-mrad - non-normalized, rms emittance

        # Initialize random variables
        a = np.sqrt(1.5 * np.sqrt(np.random.random(self._numpart)))
        beta_x = 2 * np.pi * np.random.random(self._numpart)
        beta_y = 2 * np.pi * np.random.random(self._numpart)
        rand_phi = np.random.random(self._numpart)

        # Calculate distribution
        a_x = a * np.sqrt(rand_phi)
        a_y = a * np.sqrt(1 - rand_phi)
        x = a_x * rx * np.cos(beta_x)
        xp = a_x * (rxp * np.cos(beta_x) - (emittance[0] / rx) * np.sin(beta_x))
        y = a_y * ry * np.cos(beta_y)
        yp = a_y * (ryp * np.cos(beta_y) - (emittance[1] / ry) * np.sin(beta_y))

        # Correct for z-position
        x = x + self._z * xp
        y = y + self._z * yp

        data = {'Step#0': {'x': np.array(x),
                           'px': np.array(ion.gamma() * ion.beta() * xp),
                           'y': np.array(y),
                           'py': np.array(ion.gamma() * ion.beta() * yp),
                           'z': np.array(self._z),
                           'pz': np.array(ion.gamma() * ion.beta() * self._zp),
                           'id': range(self._numpart + 1),
                           'attrs': 0}}

        return data

    def generate_parabolic(self, r, rp, e_normalized):
        """
        Generates a parabolic distribution using the beam envelope's angle and radius.
        :param r: envelope radius in the shape of array [rx, ry] (mm)
        :param rp: envelope angle in the shape of array [rxp, ryp] (mrad)
        :param e_normalized: normalized rms emittance in the shape of array [ex, ey](pi-mm-mrad)
        :return:
        """

        # Initialize parameters
        rx = float(r[0])
        rxp = float(rp[0])
        ry = float(r[1])
        ryp = float(rp[1])
        e_normalized = [float(e_normalized[0]), float(e_normalized[1])]
        ion = self._species
        emittance = np.array(e_normalized) / ion.gamma() / ion.beta()  # mm-mrad - non-normalized, rms emittance

        # Initialize random variables
        alpha = np.arccos(1.0 - 2 * np.random.random(self._numpart))
        a = np.sqrt(1.0 - 2 * np.cos((alpha - 2.0 * np.pi) / 3))
        beta_x = 2 * np.pi * np.random.random(self._numpart)
        beta_y = 2 * np.pi * np.random.random(self._numpart)
        rand_phi = np.random.random(self._numpart)

        # Calculate distribution
        a_x = a * np.sqrt(rand_phi)
        a_y = a * np.sqrt(1 - rand_phi)
        x = a_x * rx * np.cos(beta_x)
        xp = a_x * (rxp * np.cos(beta_x) - (emittance[0] / rx) * np.sin(beta_x))
        y = a_y * ry * np.cos(beta_y)
        yp = a_y * (ryp * np.cos(beta_y) - (emittance[1] / ry) * np.sin(beta_y))

        # Correct for z-position
        x = x + self._z * xp
        y = y + self._z * yp

        data = {'Step#0': {'x': np.array(x),
                           'px': np.array(ion.gamma() * ion.beta() * xp),
                           'y': np.array(y),
                           'py': np.array(ion.gamma() * ion.beta() * yp),
                           'z': np.array(self._z),
                           'pz': np.array(ion.gamma() * ion.beta() * self._zp),
                           'id': range(self._numpart + 1),
                           'attrs': 0}}

        return data


# GUI Management
class GeneratorGUI(object):
    def __init__(self, parent):
        self._parent = parent

        # Initialize GUI
        self._generate_main = QMainWindow()
        self._generate_mainGUI = Ui_Generate_Main()
        self._generate_mainGUI.setupUi(self._generate_main)
        self._generate_envelope = QMainWindow()
        self._generate_envelopeGUI = Ui_Generate_Envelope()
        self._generate_envelopeGUI.setupUi(self._generate_envelope)
        self._generate_twiss = QMainWindow()
        self._generate_twissGUI = Ui_Generate_Twiss()
        self._generate_twissGUI.setupUi(self._generate_twiss)
        self._generate_error = QMainWindow()
        self._generate_errorGUI = Ui_Generate_Error()
        self._generate_errorGUI.setupUi(self._generate_error)

        # Connect buttons and signals
        self._settings = {}
        self.apply_settings_main()
        self._generate_mainGUI.buttonBox.accepted.connect(self.callback_ok_main)
        self._generate_mainGUI.buttonBox.rejected.connect(self._generate_main.close)
        self._generate_envelopeGUI.buttonBox.accepted.connect(self.callback_ok_envelope)
        self._generate_envelopeGUI.buttonBox.rejected.connect(self._generate_envelope.close)
        self._generate_twissGUI.buttonBox.accepted.connect(self.callback_ok_twiss)
        self._generate_twissGUI.buttonBox.rejected.connect(self._generate_twiss.close)
        self._generate_errorGUI.buttonBox.accepted.connect(self._generate_error.close)
        self._generate_envelopeGUI.zpos.currentIndexChanged.connect(self.change_zpos_envelope)
        self._generate_envelopeGUI.zmom.currentIndexChanged.connect(self.change_zmom_envelope)
        self._generate_envelopeGUI.xydist.currentIndexChanged.connect(self.change_xy_envelope)
        self._generate_twissGUI.zpos.currentIndexChanged.connect(self.change_zpos_twiss)
        self._generate_twissGUI.zmom.currentIndexChanged.connect(self.change_zmom_twiss)
        self._generate_twissGUI.xydist.currentIndexChanged.connect(self.change_xy_twiss)

        self.data = {}

    def apply_settings_main(self):

        # Number of particles:
        self._settings["numpart"] = self._generate_mainGUI.lineEdit.text()

        # Species:
        info = str(self._generate_mainGUI.comboBox.currentText())
        if info == "Proton":
            self._settings["species"] = "proton"
        elif info == "Electron":
            self._settings["species"] = "electron"
        elif info == "Dihydrogen cation":
            self._settings["species"] = "H2_1+"
        elif info == "Alpha particle":
            self._settings["species"] = "4He_2+"

        # Energy:
        self._settings["energy"] = self._generate_mainGUI.energy.text()

        # Input parameter type:
        self._settings["type"] = str(self._generate_mainGUI.comboBox_2.currentText())

    def apply_settings_envelope(self):
        # Longitudinal parameters
        self._settings["zpos"] = str(self._generate_envelopeGUI.zpos.currentText())
        self._settings["zmom"] = str(self._generate_envelopeGUI.zmom.currentText())
        self._settings["ze"] = self._generate_envelopeGUI.ze.text()
        self._settings["zr"] = self._generate_envelopeGUI.zr.text()
        self._settings["zstddev"] = self._generate_envelopeGUI.zstddev.text()

        # Transverse parameters
        self._settings["xydist"] = str(self._generate_envelopeGUI.xydist.currentText())
        self._settings["eps"] = [self._generate_envelopeGUI.xe.text(), self._generate_envelopeGUI.ye.text()]
        self._settings["r"] = [self._generate_envelopeGUI.xr.text(), self._generate_envelopeGUI.yr.text()]
        self._settings["rp"] = [self._generate_envelopeGUI.xrp.text(), self._generate_envelopeGUI.yrp.text()]
        self._settings["xystddev"] = self._generate_envelopeGUI.ystddev.text()

    # TODO Add error messages to Twiss menu
    def apply_settings_twiss(self):

        # Convert from Twiss to envelope
        zp_beta = self._generate_twissGUI.zpb.text()
        ze = self._generate_twissGUI.ze.text()

        if zp_beta != "" and ze != "":
            zp_beta = float(zp_beta)
            ze = float(ze)
            rz = np.sqrt(zp_beta * ze)
        else:
            rz = float(self._generate_twissGUI.length.text())

        xa = float(self._generate_twissGUI.xa.text())
        xb = float(self._generate_twissGUI.xb.text())
        xe = float(self._generate_twissGUI.xe.text())

        rx = np.sqrt(xb * xe)
        rxp = -xa * rx / xb

        ya = float(self._generate_twissGUI.ya.text())
        yb = float(self._generate_twissGUI.yb.text())
        ye = float(self._generate_twissGUI.ye.text())

        ry = np.sqrt(yb * ye)
        ryp = -ya * ry / yb

        # Longitudinal parameters
        self._settings["zpos"] = str(self._generate_twissGUI.zpos.currentText())
        self._settings["zmom"] = str(self._generate_twissGUI.zmom.currentText())
        self._settings["ze"] = ze
        self._settings["zr"] = rz
        self._settings["zstddev"] = self._generate_twissGUI.zstddev.text()

        # Transverse parameters
        self._settings["xydist"] = str(self._generate_twissGUI.xydist.currentText())
        self._settings["eps"] = [xe, ye]
        self._settings["r"] = [rx, ry]
        self._settings["rp"] = [rxp, ryp]
        if self._generate_twissGUI.xystddev.text() != "":
            self._settings["xystddev"] = float(self._generate_twissGUI.xystddev.text())

    def callback_ok_main(self):
        self.apply_settings_main()
        if self._settings["numpart"] == "" or self._settings["energy"] == "":
            self.run_error()
        else:
            # Open either Twiss or Envelope menu
            if self._settings["type"] == "Envelope":
                self.run_envelope()
            elif self._settings["type"] == "Twiss":
                self.run_twiss()
            self._generate_main.close()

    def callback_ok_envelope(self):
        self.apply_settings_envelope()
        if self._settings["eps"] == ["", ""] or self._settings["r"] == ["", ""] or self._settings["rp"] == ["", ""]:
            self.run_error()
        else:
            if self._settings["zpos"] == "Constant" and self._settings["zmom"] == "Constant":
                g = GenerateDistribution(self._settings["numpart"], self._settings["species"],
                                         self._settings["energy"], self._settings["zpos"], self._settings["zmom"],
                                         self._settings["zr"])
            elif self._settings["zpos"] == "Gaussian" or self._settings["zmom"] == "Gaussian on ellipse":
                g = GenerateDistribution(self._settings["numpart"], self._settings["species"],
                                         self._settings["energy"], self._settings["zpos"], self._settings["zmom"],
                                         self._settings["zr"], self._settings["ez"],
                                         self._settings["zstddev"])
            else:
                g = GenerateDistribution(self._settings["numpart"], self._settings["species"],
                                         self._settings["energy"], self._settings["zpos"], self._settings["zmom"],
                                         self._settings["zr"], self._settings["ez"])
            if self._settings["xydist"] == "Uniform":
                self.data = g.generate_uniform(self._settings["r"], self._settings["rp"], self._settings["eps"])
            elif self._settings["xydist"] == "Gaussian":
                self.data = g.generate_gaussian(self._settings["r"], self._settings["rp"], self._settings["eps"],
                                                self._settings["xystddev"])
            elif self._settings["xydist"] == "Waterbag":
                self.data = g.generate_waterbag(self._settings["r"], self._settings["rp"], self._settings["eps"])
            elif self._settings["xydist"] == "Parabolic":
                self.data = g.generate_parabolic(self._settings["r"], self._settings["rp"], self._settings["eps"])
            self._generate_envelope.close()
            self._parent.add_generated_dataset(data=self.data, settings=self._settings)

    def callback_ok_twiss(self):
        self.apply_settings_twiss()
        if self._settings["eps"] == ["", ""] or self._settings["r"] == ["", ""] or self._settings["rp"] == ["", ""]:
            self.run_error()
        else:
            if self._settings["eps"] == ["", ""] or self._settings["r"] == ["", ""] or self._settings["rp"] == ["", ""]:
                self.run_error()
            else:
                if self._settings["zpos"] == "Constant" and self._settings["zmom"] == "Constant":
                    g = GenerateDistribution(self._settings["numpart"], self._settings["species"],
                                             self._settings["energy"], self._settings["zpos"], self._settings["zmom"],
                                             self._settings["zr"])
                elif self._settings["zpos"] == "Gaussian" or self._settings["zmom"] == "Gaussian on ellipse":
                    g = GenerateDistribution(self._settings["numpart"], self._settings["species"],
                                             self._settings["energy"], self._settings["zpos"], self._settings["zmom"],
                                             self._settings["zr"], self._settings["ez"],
                                             self._settings["zstddev"])
                else:
                    g = GenerateDistribution(self._settings["numpart"], self._settings["species"],
                                             self._settings["energy"], self._settings["zpos"], self._settings["zmom"],
                                             self._settings["zr"], self._settings["ez"])
                if self._settings["xydist"] == "Uniform":
                    self.data = g.generate_uniform(self._settings["r"], self._settings["rp"], self._settings["eps"])
                elif self._settings["xydist"] == "Gaussian":
                    self.data = g.generate_gaussian(self._settings["r"], self._settings["rp"], self._settings["eps"],
                                                    self._settings["xystddev"])
                elif self._settings["xydist"] == "Waterbag":
                    self.data = g.generate_waterbag(self._settings["r"], self._settings["rp"], self._settings["eps"])
                elif self._settings["xydist"] == "Parabolic":
                    self.data = g.generate_parabolic(self._settings["r"], self._settings["rp"], self._settings["eps"])
                self._generate_twiss.close()
                self._parent.add_generated_dataset(data=self.data, settings=self._settings)

    def change_zpos_envelope(self):
        info = str(self._generate_envelopeGUI.zpos.currentText())
        if info != "Constant":
            self._generate_envelopeGUI.ze.setEnabled(True)
            if info == "Gaussian on ellipse":
                self._generate_envelopeGUI.zstddev.setEnabled(True)

    def change_zmom_envelope(self):
        info = str(self._generate_envelopeGUI.zmom.currentText())
        if info != "Constant":
            self._generate_envelopeGUI.ze.setEnabled(True)
            if info == "Gaussian on ellipse":
                self._generate_envelopeGUI.zstddev.setEnabled(True)

    def change_xy_envelope(self):
        info = str(self._generate_envelopeGUI.xydist.currentText())
        if info == "Gaussian":
            self._generate_envelopeGUI.ystddev.setEnabled(True)

    def change_zpos_twiss(self):
        info = str(self._generate_twissGUI.zpos.currentText())
        if info != "Constant":
            self._generate_twissGUI.ze.setEnabled(True)
            self._generate_twissGUI.zpa.setEnabled(True)
            self._generate_twissGUI.zpb.setEnabled(True)
            self._generate_twissGUI.length.setDisabled(True)
            if info == "Gaussian on ellipse":
                self._generate_twissGUI.zstddev.setEnabled(True)

    def change_zmom_twiss(self):
        info = str(self._generate_twissGUI.zmom.currentText())
        if info != "Constant":
            self._generate_twissGUI.ze.setEnabled(True)
            if info == "Gaussian on ellipse":
                self._generate_twissGUI.zstddev.setEnabled(True)

    def change_xy_twiss(self):
        info = str(self._generate_twissGUI.xydist.currentText())
        if info == "Gaussian":
            self._generate_twissGUI.xystddev.setEnabled(True)

    def run(self):
        # --- Calculate the positions to center the window --- #
        screen_size = self._parent.screen_size()
        _x = 0.5 * (screen_size.width() - self._generate_main.width())
        _y = 0.5 * (screen_size.height() - self._generate_main.height())

        # --- Show the GUI --- #
        self._generate_main.show()
        self._generate_main.move(_x, _y)

    def run_error(self):
        # --- Calculate the positions to center the window --- #
        screen_size = self._parent.screen_size()
        _x = 0.5 * (screen_size.width() - self._generate_error.width())
        _y = 0.5 * (screen_size.height() - self._generate_error.height())

        # --- Show the GUI --- #
        self._generate_error.show()
        self._generate_error.move(_x, _y)

    def run_envelope(self):
        # --- Calculate the positions to center the window --- #
        screen_size = self._parent.screen_size()
        _x = 0.5 * (screen_size.width() - self._generate_envelope.width())
        _y = 0.5 * (screen_size.height() - self._generate_envelope.height())

        # --- Show the GUI --- #
        self._generate_envelope.show()
        self._generate_envelope.move(_x, _y)

    def run_twiss(self):
        # --- Calculate the positions to center the window --- #
        screen_size = self._parent.screen_size()
        _x = 0.5 * (screen_size.width() - self._generate_twiss.width())
        _y = 0.5 * (screen_size.height() - self._generate_twiss.height())

        # --- Show the GUI --- #
        self._generate_twiss.show()
        self._generate_twiss.move(_x, _y)
