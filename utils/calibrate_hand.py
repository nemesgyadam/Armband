import os
clear = lambda: os.system("cls")

fist_min = None
fist_max = None
degree_center = None
degree_min = None
degree_max = None

class Calibrator:
    def __init__(self):
        self.fist_min = None
        self.fist_max = None
        self.degree_center = None
        self.degree_min = None
        self.degree_max = None
        self.calibrate_step = 0
        self.done = False

    def step(self, kalman_value, distance, k):
        if self.calibrate_step==0:
            clear()
            print("Please put your hand in the center of the screen")
            print("In relaxed, open position")
            print("Press space to continue")
            self.calibrate_step += 1
            return
        
        if self.calibrate_step == 1:
            if k == 32:
                self.fist_max = distance
                self.degree_center = kalman_value
                clear()
                print("Fist max set to {}".format(self.fist_max))
                print("Degree center set to {}".format(self.degree_center))
                self.calibrate_step +=1
                return
        
        if self.calibrate_step == 2:
            clear()
            print("Please put your hand in the center of the screen")
            print("In fist position")
            print("Press space to continue")
            self.calibrate_step += 1
            return
        
        if self.calibrate_step == 3:
            if k == 32:
                self.fist_min = distance
                clear()
                print("Fist min set to {}".format(self.fist_min))
                self.calibrate_step +=1
                return
        
        if self.calibrate_step == 4:
            clear()
            print("Please turn your hand to the left")
            print("Press space to continue")
            self.calibrate_step += 1
            return
        
        if self.calibrate_step == 5:
            if k == 32:
                self.degree_max = kalman_value
                print("Degree max set to {}".format(self.degree_max))
                self.calibrate_step +=1
                return
        
        if self.calibrate_step == 6:
            clear()
            print("Please turn your hand to the right")
            print("Press space to continue")
            self.calibrate_step += 1
            return
        
        if self.calibrate_step == 7:
            if k == 32:
                clear()
                self.degree_min = kalman_value
                print("Configuration done")
                print("Degree center: {}".format(self.degree_center))
                print("Degree min: {}".format(self.degree_min))
                print("Degree max: {}".format(self.degree_max))
                print()
                print("Fist min: {}".format(self.fist_min))
                print("Fist max: {}".format(self.fist_max))
                self.done = True
                return
