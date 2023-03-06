from numpy import array, arctan2, cos, sin, pi, sqrt, matmul, exp


class Univector:
    # % These functions are needed to develop the univector field, and can be found at the paper:
    # % "Evolutionary Univector Field-based Navigation with Collision Avoidance for Mobile Robot"

    def __init__(self):
        # ? Constants learned from EP
        self.d_e = 8#6  # Constante relacionada ao tamanho das espirais
        self.k_r = 10#7  # Constante de suavização do campo
        self.delta = 5  # Variancia da gaussiana de obstaculo
        self.k_o = 0.5  # Constante de proporcionalidade velocidade do obstaculo
        self.d_min = 5  # * => modified: EP = 3.48          # Distancia mínima em que o campo se torna puro repulsivo

    def rot_matrix(self, alpha):  # Função que retorna uma matriz de rotação
        return array(((cos(alpha), -sin(alpha)), (sin(alpha), cos(alpha))))

    def phi_h_cw(self, x, y, xg, yg):  # Função que retorna o campo espiral hiperbólico horário
        rho = sqrt((x - xg) ** 2 + (y - yg) ** 2)
        theta = arctan2(y - yg, x - xg)

        if rho > self.d_e:
            phi = theta - 0.5 * pi * (2 - ((self.d_e + self.k_r) / (rho + self.k_r)))

        else:
            phi = theta - 0.5 * pi * sqrt(rho / self.d_e)

        phi = arctan2(sin(phi), cos(phi))  # ? Trick to mantain phi between [-pi,pi]

        return phi

    def phi_h_ccw(self, x, y, xg, yg):  # Função que retorna o campo espiral hiperbólico anti-horário
        rho = sqrt((x - xg) ** 2 + (y - yg) ** 2)
        theta = arctan2(y - yg, x - xg)

        if rho > self.d_e:
            phi = theta + 0.5 * pi * (2 - ((self.d_e + self.k_r) / (rho + self.k_r)))
        else:
            phi = theta + 0.5 * pi * sqrt(rho / self.d_e)

        phi = arctan2(sin(phi), cos(phi))  # ? Trick to mantain phi between [-pi,pi]

        return phi

    def n_n(self, phi):  # Vetor diretor Nh de um angulo phi dado
        return array([[cos(phi)], [sin(phi)]])

    def gaussian_func(self, r):  # Função gaussiana
        return exp(-0.5 * (r / self.delta) ** 2)

    # % This is the hyperbolic vector field which yields us to the target position with the desired posture
    # % without avoiding any obstacle
    def hip_vec_field(self, robot, target):
        matrix = array(((cos(-target.theta), -sin(-target.theta)),
                        (sin(-target.theta), cos(-target.theta))))  # Matrizes de rotação necessárias
        matrix2 = array(((cos(target.theta), -sin(target.theta)), (sin(target.theta), cos(target.theta))))

        vet_pos = [[robot.xPos], [robot.yPos]]  # Transformando posição em vetor
        target_pos = [[target.xPos], [target.yPos]]

        vet_pos = array(vet_pos) - array(target_pos)  # Translação do sistema coordenado
        vet_pos = matmul(matrix, vet_pos)  # Rotação do sistema coordenado

        x = vet_pos[0]  # Atribuição do novo (x,y)
        y = vet_pos[1]
        y = y[0]
        x = x[0]

        yl = y + self.d_e  # Calculo do campo com base no artigo
        yr = y - self.d_e

        n_cw = self.n_n(self.phi_h_cw(x, y + self.d_e, 0, 0))
        n_ccw = self.n_n(self.phi_h_ccw(x, y - self.d_e, 0, 0))
        n_cw = [[n_cw[0]], [n_cw[1][0]]]
        n_ccw = [[n_ccw[0][0]], [n_ccw[1][0]]]

        if -self.d_e <= y < self.d_e:
            x_phi = 0.5 * (abs(yl) * n_ccw[0][0] + abs(yr) ** 1 * n_cw[0][0]) / self.d_e
            y_phi = 0.5 * (abs(yl) * n_ccw[1][0] + abs(yr) ** 1 * n_cw[1][0]) / self.d_e
            phi = arctan2(y_phi, x_phi)
            phi = phi[0]
        elif y < -self.d_e:
            phi = self.phi_h_cw(x, y + self.d_e, 0, 0)
        else:
            phi = self.phi_h_ccw(x, y - self.d_e, 0, 0)

        vec_phi = matmul(matrix2, [[cos(phi)], [sin(phi)]])  # Rotação para retornar ao sistema original
        phi = arctan2(vec_phi[1], vec_phi[0])

        return phi

    # % This is the 'N_Posture' vector field which yields us to the target position with the desired posture
    # % without avoiding any obstacle
    def n_vec_field(self, robot, target, n=8, d=2, have_face=False):
        rx = target.xPos + d * cos(target.theta)
        ry = target.yPos + d * sin(target.theta)
        pg_ang = arctan2(target.yPos - robot.yPos, target.xPos - robot.xPos)
        pr_ang = arctan2(ry - robot.yPos, rx - robot.xPos)
        alpha = arctan2(sin(pr_ang - pg_ang), cos(pr_ang - pg_ang))
        phi = arctan2(sin(pg_ang - n * alpha), cos(pg_ang - n * alpha))
        return phi

    # % This is the vector field which let us avoid a moving obstacle, but don't yields us to the target position
    def ao_vec_field(self, robot, obst):
        sx = self.k_o * (
                    obst.v * cos(obst.theta) - robot.v * cos(robot.theta))  # ? Components of the shifting vector, where
        sy = self.k_o * (obst.v * sin(obst.theta) - robot.v * sin(robot.theta))  # ? S=k_o*(V_obst-V_robot)
        s = sqrt(sx ** 2 + sy ** 2)
        d = robot.dist(obst)
        if d >= s:
            px = obst.xPos + sx
            py = obst.yPos + sy
        else:
            px = obst.xPos + (d / s) * sx
            py = obst.yPos + (d / s) * sy
        phi = arctan2(robot.yPos - py, robot.xPos - px)
        return phi

    # % This is the composed vector field, which mix both move-to-target (hyperbolic) and avoid-obstacle vector field
    # % using a gaussian function
    def univec_field_h(self, robot, target, obst):
        d = robot.dist(obst)
        if d <= self.d_min:
            phi = self.ao_vec_field(robot, obst)
        else:
            phi = self.gaussian_func(d - self.d_min) * self.ao_vec_field(robot, obst)
            phi += (1 - self.gaussian_func(d - self.d_min)) * self.hip_vec_field(robot, target)
        return phi

    # % This is the composed vector field, which mix both move-to-target ('N_Posture') and avoid-obstacle vector field
    # % using a gaussian function
    def univec_field_n(self, robot, target, obst, n=8, d=2):
        if robot.dist(obst) <= self.d_min:
            robot.flagTrocaFace = True
            phi = self.ao_vec_field(robot, obst)
        else:
            robot.flagTrocaFace = False
            phi = self.gaussian_func(robot.dist(obst) - self.d_min) * self.ao_vec_field(robot, obst)
            phi += (1 - self.gaussian_func(robot.dist(obst) - self.d_min)) * self.n_vec_field(robot, target, n, d,
                                                                                              have_face=False)
        return phi
