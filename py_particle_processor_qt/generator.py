from dans_pymodules import IonSpecies
import matplotlib.pyplot as plt
import numpy as np


class GenerateDistribution(object):
    """
    A generator for creating various particle distributions.
    """

    # Calculations to be added to the file where generate is called:
    # rx = np.sqrt(beta[0] * epsilon[0])
    # rxp = -alpha[0] * rx / beta[0]
    #
    # ry = np.sqrt(beta[1] * epsilon[1])
    # ryp = -alpha[1] * ry / beta[1]
    #
    # if beta[0] * gamma[0] < 1.0 or beta[1] * gamma[1] < 1.0:
    #     print("Beta*Gamma < 1: This is not a realistic combination of beta and gamma.")
    #     return 1
    #
    # if beta[0] * gamma[0] - alpha[0] ** 2 != 1.0 or beta[1] * gamma[1] - alpha[1] ** 2 != 1.0:
    #     print("Beta*Gamma - Alpha^2 != 1: This is not a realistic combination of alpha, beta, and gamma")
    #     return 1

    def __init__(self, numpart, species, length, z_pos="Zero", z_mom="Zero",
                 rz=0, rzp=0, ez=0, stddev=1, lamin_ratio=1.0):
        self._numpart = numpart  # number of particles
        self._species = species  # instance of IonSpecies
        self._length = length  # full length of beam (mm)

        # Calculate longitudinal position distribution
        z = np.zeros(self._numpart)
        if z_pos == "Constant":  # Constant z-position
            z = np.full(self._numpart, rz)
        elif z_pos == "Random":  # Randomly distributed z-position
            z = (np.random.random(self._numpart) - 0.5) * self._length
        elif z_pos == "Uniform":  # Uniformly randomly distributed within an ellipse
            beta = 2 * np.pi * np.random.random(self._numpart)
            a = np.ones(self._numpart)
            rand_phi = np.random.random(self._numpart)
            a_z = a * np.sqrt(rand_phi)
            z = a_z * rz * np.cos(beta)
        elif z_pos == "Gaussian":  # Gaussian distribution within an ellipse
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
            alpha = np.arccos(1.0 - 2*np.random.random(self._numpart))
            a = np.sqrt(1.0 - 2*np.cos((alpha - 2.0*np.pi)/3))
            rand_phi = np.random.random(self._numpart)
            a_z = a * np.sqrt(rand_phi)
            z = a_z * rz * np.cos(beta)
        elif z_pos == "Top-hat":
            beta = 2 * np.pi * np.random.random(self._numpart)
            a = np.ones(self._numpart)
            rand_phi = np.random.random(self._numpart)
            a_z = a * np.sqrt(rand_phi)
            z = a_z * rz * np.cos(beta)

        # Calculate longitudinal momentum distribution
        zp = np.zeros(self._numpart)
        if z_mom == "Constant":
            zp = np.full(self._numpart, rzp)
        elif z_mom == "Random":
            zp = (np.random.random(self._numpart) - 0.5) * self._length
        elif z_mom == "Uniform":
            beta = 2 * np.pi * np.random.random(self._numpart)
            a = np.ones(self._numpart)
            rand_phi = np.random.random(self._numpart)
            a_z = a * np.sqrt(rand_phi)
            zp = a_z * (rzp * np.cos(beta) - (ez / rz) * np.sin(beta))
        elif z_mom == "Gaussian":
            z_rand = np.random.normal(0, stddev, self._numpart)
            zp_rand = np.random.normal(0, stddev, self._numpart)
            z_temp = z_rand * rz * .5
            zp = (rzp / rz) * z_temp + (ez / (2 * rz)) * zp_rand

        if z_pos == "Laminar" and z_mom == "Laminar":
            z = (np.random.random(self._numpart) - 0.5) * self._length
            zp = z*lamin_ratio

        self._z = np.abs(z)
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
        rx = r[0]
        rxp = rp[0]
        ry = r[1]
        ryp = rp[1]
        ion = self._species
        emittance = np.array(e_normalized) / ion.gamma() / ion.beta()  # mm-mrad - non-normalized, rms emittance

        # Initialize random variables
        a = np.ones(self._numpart)
        beta_x = 2*np.pi*np.random.random(self._numpart)
        beta_y = 2*np.pi*np.random.random(self._numpart)
        rand_phi = np.random.random(self._numpart)

        # Calculate distribution
        a_x = a*np.sqrt(rand_phi)
        a_y = a*np.sqrt(1 - rand_phi)
        x = a_x*rx*np.cos(beta_x)
        xp = a_x * (rxp * np.cos(beta_x) - (emittance[0] / rx) * np.sin(beta_x))
        y = a_y*ry*np.cos(beta_y)
        yp = a_y * (ryp * np.cos(beta_y) - (emittance[1] / ry) * np.sin(beta_y))

        # Correct for z-position
        x = x + self._z * xp
        y = y + self._z * yp

        data = {'Step#0': {'x': np.array(x),
                           'xp': np.array(xp),
                           'px': np.array(ion.gamma() * ion.beta() * xp),
                           'y': np.array(y),
                           'yp': np.array(yp),
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
        r0x = r[0]
        a0x = rp[0]
        r0y = r[1]
        a0y = rp[1]
        ion = self._species
        emittance = np.array(e_normalized) / ion.gamma() / ion.beta()  # mm-mrad - non-normalized, rms emittance

        # Initialize random variables
        x_rand = np.random.normal(0, stddev, self._numpart)
        y_rand = np.random.normal(0, stddev, self._numpart)
        xp_rand = np.random.normal(0, stddev, self._numpart)
        yp_rand = np.random.normal(0, stddev, self._numpart)

        # Calculate distribution
        x = x_rand*r0x*.5
        xp = (a0x/r0x)*x + (emittance[0]/(2*r0x))*xp_rand
        y = y_rand*r0y*.5
        yp = (a0y/r0y)*y + (emittance[1]/(2*r0y))*yp_rand

        # Correct for z-position
        x = x + self._z * xp
        y = y + self._z * yp

        data = {'Step#0': {'x': np.array(x),
                           'xp': np.array(xp),
                           'px': np.array(ion.gamma() * ion.beta() * xp),
                           'y': np.array(y),
                           'yp': np.array(yp),
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
        rx = r[0]
        rxp = rp[0]
        ry = r[1]
        ryp = rp[1]
        ion = self._species
        emittance = np.array(e_normalized) / ion.gamma() / ion.beta()  # mm-mrad - non-normalized, rms emittance

        # Initialize random variables
        a = np.sqrt(1.5 * np.sqrt(np.random.random(self._numpart)))
        beta_x = 2*np.pi*np.random.random(self._numpart)
        beta_y = 2*np.pi*np.random.random(self._numpart)
        rand_phi = np.random.random(self._numpart)

        # Calculate distribution
        a_x = a*np.sqrt(rand_phi)
        a_y = a*np.sqrt(1 - rand_phi)
        x = a_x*rx*np.cos(beta_x)
        xp = a_x * (rxp * np.cos(beta_x) - (emittance[0] / rx) * np.sin(beta_x))
        y = a_y*ry*np.cos(beta_y)
        yp = a_y * (ryp * np.cos(beta_y) - (emittance[1] / ry) * np.sin(beta_y))

        # Correct for z-position
        x = x + self._z * xp
        y = y + self._z * yp

        data = {'Step#0': {'x': np.array(x),
                           'xp': np.array(xp),
                           'px': np.array(ion.gamma() * ion.beta() * xp),
                           'y': np.array(y),
                           'yp': np.array(yp),
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
        rx = r[0]
        rxp = rp[0]
        ry = r[1]
        ryp = rp[1]
        ion = self._species
        emittance = np.array(e_normalized) / ion.gamma() / ion.beta()  # mm-mrad - non-normalized, rms emittance

        # Initialize random variables
        alpha = np.arccos(1.0 - 2*np.random.random(self._numpart))
        a = np.sqrt(1.0 - 2*np.cos((alpha - 2.0*np.pi)/3))
        beta_x = 2*np.pi*np.random.random(self._numpart)
        beta_y = 2*np.pi*np.random.random(self._numpart)
        rand_phi = np.random.random(self._numpart)

        # Calculate distribution
        a_x = a*np.sqrt(rand_phi)
        a_y = a*np.sqrt(1 - rand_phi)
        x = a_x*rx*np.cos(beta_x)
        xp = a_x * (rxp * np.cos(beta_x) - (emittance[0] / rx) * np.sin(beta_x))
        y = a_y*ry*np.cos(beta_y)
        yp = a_y * (ryp * np.cos(beta_y) - (emittance[1] / ry) * np.sin(beta_y))

        # Correct for z-position
        x = x + self._z * xp
        y = y + self._z * yp

        data = {'Step#0': {'x': np.array(x),
                           'xp': np.array(xp),
                           'px': np.array(ion.gamma() * ion.beta() * xp),
                           'y': np.array(y),
                           'yp': np.array(yp),
                           'py': np.array(ion.gamma() * ion.beta() * yp),
                           'z': np.array(self._z),
                           'pz': np.array(ion.gamma() * ion.beta() * self._zp),
                           'id': range(self._numpart + 1),
                           'attrs': 0}}

        return data

if __name__ == '__main__':
    gen = GenerateDistribution(1000, IonSpecies("H2_1+", 3), 7, "Uniform", "Gaussian", 2, 4, 2)

    r_x = 3.16227
    r_xp = -7.5
    r_y = 1.41421
    r_yp = -2.83
    e_x = 1
    e_y = 0.7

    dist1 = gen.generate_uniform([r_x, r_y], [r_xp, r_yp], [e_x, e_y]).get("Step#0")
    fig = plt.figure()
    plt.suptitle("r_j = {}, r_j' = {}, emittance_j = {}"
                 .format([r_x, r_y], [r_xp, r_yp], [e_x, e_y]))
    # plt.subplot(234)
    # M = np.hypot(dist1["pz"], dist1["px"])
    plt.quiver(dist1["z"], dist1["x"], dist1["pz"], dist1["px"], dist1["pz"], width=0.001)
    plt.xlabel("z")
    plt.ylabel("x")

    # plt.subplot(233)
    # plt.scatter(dist1.get("y"), dist1.get("yp"), marker='.', s=.1)
    # plt.xlabel("y")
    # plt.ylabel("y'")
    # plt.axis("equal")
    #
    # plt.subplot(235)
    # plt.scatter(dist1.get("xp"), dist1.get("yp"), marker='.', s=.1)
    # plt.xlabel("x'")
    # plt.ylabel("y'")
    # plt.axis("equal")
    #
    # plt.subplot(231)
    # plt.scatter(dist1.get("x"), dist1.get("xp"), marker='.', s=.1)
    # plt.xlabel("x")
    # plt.ylabel("x'")
    # plt.axis("equal")
    #
    # plt.subplot(236)
    # plt.scatter(dist1.get("y"), dist1.get("xp"), marker='.', s=.1)
    # plt.xlabel("y")
    # plt.ylabel("x'")
    # plt.axis("equal")
    #
    # plt.subplot(232)
    # plt.scatter(dist1.get("x"), dist1.get("y"), marker='.', s=.1)
    # plt.xlabel("x")
    # plt.ylabel("y")
    # plt.axis("equal")

    plt.show()
