# Import libraries
import numpy as np
from matplotlib.patches import Rectangle, Circle
from matplotlib.lines import Line2D

class RobotSimulation:
    def __init__(self, ax, delta, escala):
        self.ax = ax
        self.escala = escala
        self.delta = delta

        self.phi = 120 * (np.pi / 180)        # Angle of the wheel in radians
        self.L = 1.5 * self.escala            # Length of the robot arm scaled
        self.r_rueda = 0.25 * self.escala     # Radius of the wheel scaled
        self.ancho_rueda = 0.25 * self.escala # Width of the wheel scaled
        self.posicion_vertice = np.array([self.L, - self.r_rueda]) # Position of the wheel vertex in local coordinates
        self.artists = [] # List to store graphical objects for plot the robot
        
        # Positions of the wheels in local coordinates
        self.posiciones_ruedas = np.array([
            [self.L, 0],
            [self.L * np.cos(self.phi), self.L * np.sin(self.phi)],
            [self.L * np.cos(2 * self.phi), self.L * np.sin(2 * self.phi)]
        ])

    # Rotate a point by a given angle around the origin
    def rotate_point(self, point, angle):
        rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                    [np.sin(angle), np.cos(angle)]])
        return np.dot(point, rotation_matrix.T)

    # Draw the robot at the given global position and orientation
    def draw_robot(self, P):
        x_global, y_global, theta = P
        self.clear_robot() # Clear previous robot drawings

        # plot the point
        posiciones_absolutas_ruedas = self.rotate_point(self.posiciones_ruedas, P[2]) + np.array([x_global, y_global])
        circle = Circle((x_global, y_global), radius=2.0*self.escala, color='black', fill=False) 
        self.ax.add_patch(circle)
        self.artists.append(circle)

        # Plot each wheel and their connections with the point 
        for i in range(0, 3):
            angulo_rotacion_vertice = theta + self.phi * i
            posicion_absoluta_vertice = self.rotate_point(self.posicion_vertice, angulo_rotacion_vertice) + np.array([x_global, y_global])
            rect = Rectangle((posicion_absoluta_vertice[0], posicion_absoluta_vertice[1]), self.ancho_rueda, 2 * self.r_rueda, angle=(angulo_rotacion_vertice) * (180 / np.pi), edgecolor='black', facecolor='none')
            self.ax.add_patch(rect)
            self.artists.append(rect)

            line = Line2D([x_global, posiciones_absolutas_ruedas[i][0]],
                          [y_global, posiciones_absolutas_ruedas[i][1]], color='black')
            self.ax.add_line(line)
            self.artists.append(line)

            point = self.ax.plot(x_global, y_global, 'ko', markersize=8 * self.escala)
            self.artists.append(point[0])

    # Remove all previously drawn elements of the robot
    def clear_robot(self):
        for artist in self.artists:
            artist.remove()
        self.artists = []