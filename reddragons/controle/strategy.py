from .action import *
from numpy import *


class Strategy:
    def __init__(self, robot0, robot1, robot2, robot_enemy_0, robot_enemy_1, robot_enemy_2, ball, mray, strategy):
        self.robot0 = robot0
        self.robot1 = robot1
        self.robot2 = robot2
        self.robotEnemy0 = robot_enemy_0
        self.robotEnemy1 = robot_enemy_1
        self.robotEnemy2 = robot_enemy_2
        self.ball = ball
        self.mray = mray
        self.penaltyDefensive = False
        self.penaltyOffensive = False
        self.strategy = strategy

    def decider(self):
        if self.strategy == 'default':
            self.coach()
        elif self.strategy == 'twoAttackers':
            self.coach2()
        else:
            print("Algo deu errado na seleção de estratégias")

    def coach2(self):
        """Picks a strategy depending on the status of the field"""
        # For the time being, the only statuses considered are which side of the field the ball is in
        if self.penaltyDefensive:
            self.penalty_mode_defensive()
        elif self.penaltyOffensive:
            self.penalty_mode_offensive_spin()
        else:
            if self.mray:
                if self.ball.xPos > 85:
                    self.stg_def_v2()
                else:
                    self.stg_att_v2()
            else:
                if self.ball.xPos > 85:
                    self.stg_att_v2()
                else:
                    self.stg_def_v2()

    def coach(self):
        """Picks a strategy depending on the status of the field"""
        # For the time being, the only statuses considered are which side of the field the ball is in
        if self.penaltyDefensive:
            self.penalty_mode_defensive()
        elif self.penaltyOffensive:
            self.penalty_mode_offensive_spin()
        else:
            if self.mray:
                if self.ball.xPos > 85:
                    self.basic_stg_def_2()
                else:
                    self.basic_stg_att()
            else:
                if self.ball.xPos > 85:
                    self.basic_stg_att()
                else:
                    self.basic_stg_def_2()

    def basic_stg_def(self):
        """Basic original strategy with goalkeeper advance"""
        if not self.mray:
            if self.ball.xPos < 30 and 30 < self.ball.yPos < 110:
                defender_penalty(self.robot0, self.ball, leftSide=not self.mray)
                screen_out_ball(self.robot1, self.ball, 55, left_side=not self.mray)
            else:
                shoot(self.robot1, self.ball, left_side=not self.mray, friend1=self.robot0, friend2=self.robot2,
                             enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
                screen_out_ball(self.robot0, self.ball, 14, left_side=not self.mray, upper_lim=81, lower_lim=42)
        else:
            if self.ball.xPos > 130 and 30 < self.ball.yPos < 110:
                defender_penalty(self.robot0, self.ball, leftSide=not self.mray)
                screen_out_ball(self.robot1, self.ball, 55, left_side=not self.mray)
            else:
                shoot(self.robot1, self.ball, left_side=not self.mray, friend1=self.robot0, friend2=self.robot2,
                             enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
                screen_out_ball(self.robot0, self.ball, 14, left_side=not self.mray, upper_lim=81, lower_lim=42)
        screen_out_ball(self.robot2, self.ball, 110, left_side=not self.mray, upper_lim=120, lower_lim=10)

    def basic_stg_att(self):
        """Basic alternative strategy"""
        defender_spin(self.robot2, self.ball, left_side=not self.mray, friend1=self.robot0, friend2=self.robot1,
                             enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
        screen_out_ball(self.robot1, self.ball, 60, left_side=not self.mray, upper_lim=120, lower_lim=10)
        screen_out_ball(self.robot0, self.ball, 14, left_side=not self.mray, upper_lim=81, lower_lim=42)

    def basic_stg_def_2(self):
        """Basic original strategy with goalkeeper advance and spin"""
        if not self.mray:
            if self.ball.xPos < 40 and 30 < self.ball.yPos < 110:
                defender_penalty(self.robot0, self.ball, leftSide=not self.mray)
                screen_out_ball(self.robot1, self.ball, 55, left_side=not self.mray)
            else:
                defender_spin(self.robot1, self.ball, left_side=not self.mray, friend1=self.robot0,
                                     friend2=self.robot2,
                                     enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
                screen_out_ball(self.robot0, self.ball, 14, left_side=not self.mray, upper_lim=81, lower_lim=42)
        else:
            if self.ball.xPos > 130 and 30 < self.ball.yPos < 110:
                defender_penalty(self.robot0, self.ball, leftSide=not self.mray)
                screen_out_ball(self.robot1, self.ball, 55, left_side=not self.mray)
            else:
                defender_spin(self.robot1, self.ball, left_side=not self.mray, friend1=self.robot0,
                                     friend2=self.robot2,
                                     enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
                screen_out_ball(self.robot0, self.ball, 14, left_side=not self.mray, upper_lim=81, lower_lim=42)
        screen_out_ball(self.robot2, self.ball, 110, left_side=not self.mray, upper_lim=120, lower_lim=10)
        if ((abs(self.robot0.theta) < deg2rad(10)) or (abs(self.robot0.theta) > deg2rad(170))) and (
                self.robot0.xPos < 20 or self.robot0.xPos > 150):
            self.robot0.contStopped += 1
        else:
            self.robot0.contStopped = 0

    def stg_def_v2(self):
        """Strategy with 2 robots moving with Master-Slave in defensive side"""
        if not self.mray:
            if self.ball.xPos < 40 and 30 < self.ball.yPos < 110:
                defender_penalty(self.robot0, self.ball, leftSide=not self.mray)
                self.two_attackers()
            else:
                self.two_attackers()
                screen_out_ball(self.robot0, self.ball, 16, left_side=not self.mray, upper_lim=84, lower_lim=42)
        else:
            if self.ball.xPos > 130 and 30 < self.ball.yPos < 110:
                defender_penalty(self.robot0, self.ball, leftSide=not self.mray)
                self.two_attackers()
            else:
                self.two_attackers()
                screen_out_ball(self.robot0, self.ball, 16, left_side=not self.mray, upper_lim=84, lower_lim=42)

        if ((abs(self.robot0.theta) < deg2rad(10)) or (abs(self.robot0.theta) > deg2rad(170))) and (
                self.robot0.xPos < 20 or self.robot0.xPos > 150):
            self.robot0.contStopped += 1
        else:
            self.robot0.contStopped = 0

    def stg_att_v2(self):
        """Strategy with 2 robots moving with Master-Slave in offensive side"""
        self.two_attackers()
        screen_out_ball(self.robot0, self.ball, 16, left_side=not self.mray, upper_lim=84, lower_lim=42)

    def stg_full_att(self):
        """Crazy test attack strategy"""
        shoot(self.robot2, self.ball, left_side=not self.mray, friend1=self.robot0, friend2=self.robot1,
                     enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
        shoot(self.robot1, self.ball, left_side=not self.mray, friend1=self.robot1, friend2=self.robot2,
                     enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
        screen_out_ball(self.robot0, self.ball, 10, left_side=not self.mray)

    def penalty_mode_defensive(self):
        """Strategy to defend penalty situations"""
        defender_penalty(self.robot0, self.ball, left_side=not self.mray, friend1=self.robot1,
                                friend2=self.robot2,
                                enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
        shoot(self.robot1, self.ball, left_side=not self.mray, friend1=self.robot0, friend2=self.robot2,
                     enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
        shoot(self.robot2, self.ball, left_side=not self.mray, friend1=self.robot0, friend2=self.robot1,
                     enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
        if not self.mray:
            if self.ball.xPos > 48 or self.ball.yPos < 30 or self.ball.yPos > 100:
                self.penaltyDefensive = False
        else:
            if self.ball.xPos < 112 or self.ball.yPos < 30 or self.ball.yPos > 100:
                self.penaltyDefensive = False

    def penalty_mode_offensive(self):
        """Strategy to convert penalty offensive situations"""
        screen_out_ball(self.robot0, self.ball, 10, left_side=not self.mray)
        shoot(self.robot1, self.ball, left_side=not self.mray, friend1=self.robot0, friend2=self.robot2,
                     enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
        attack_penalty(self.robot2, self.ball, leftSide=not self.mray, friend1=self.robot0, friend2=self.robot1,
                              enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
        if sqrt((self.ball.xPos - self.robot2.xPos) ** 2 + (self.ball.yPos - self.robot2.yPos) ** 2) > 20:
            self.penaltyOffensive = False

    def penalty_mode_offensive_spin(self):
        """Strategy to convert penalty offensive situations"""
        screen_out_ball(self.robot0, self.ball, 10, left_side=not self.mray)
        shoot(self.robot1, self.ball, left_side=not self.mray, friend1=self.robot0, friend2=self.robot2,
                     enemy1=self.robotEnemy0, enemy2=self.robotEnemy1, enemy3=self.robotEnemy2)
        if not self.robot2.dist(self.ball) < 9:
            girar(self.robot2, 100, 100)
        else:
            if self.robot2.teamYellow:
                if self.robot2.yPos < 65:
                    girar(self.robot2, 0, 100)
                else:
                    girar(self.robot2, 100, 0)
            else:
                if self.robot2.yPos > 65:
                    girar(self.robot2, 0, 100)
                else:
                    girar(self.robot2, 100, 0)
        if sqrt((self.ball.xPos - self.robot2.xPos) ** 2 + (self.ball.yPos - self.robot2.yPos) ** 2) > 30:
            self.penaltyOffensive = False

    def two_attackers(self):
        """Strategy to move 2 robots at same time with Master-Slave"""
        master_slave(self.robot0, self.robot1, self.robot2, self.ball, self.robotEnemy0, self.robotEnemy1,
                            self.robotEnemy2)
