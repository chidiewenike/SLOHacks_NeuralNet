import time
import random 
from ParkingMetrics import ParkingMetrics

class Car:
    def __init__(self,plate):

        self.return_day = True
        self.in_lot = False
        self.plate = plate
        self.location = ""
        self.arrive_hour = random.randint(8, 12)
        self.arrive_min = 0
        self.leave_hour = self.arrive_hour
        self.leave_min = 0



class Sim_Run():

    def __init__(self,num_cars):
        self.pm = ParkingMetrics('pH_cred.json')
        self.car_list = self.car_gen(num_cars)
        self.day = 5
        self.hour = 7
        self.min = 55
        self.curDate = 0 
        self.day_weight = {}
        self.day_weight["0"] = [False,False,False,False,False,False,True,True,True] # sunday
        self.day_weight["1"] = [False,True,True,True,True,True,True,True,True] # monday
        self.day_weight["2"] = [False,False,False,True,True,True,True,True,True] # tuesday
        self.day_weight["3"] = [False,False,True,True,True,True,True,True,True] # wednesday
        self.day_weight["4"] = [False,False,False,False,True,True,True,True,True] # thursday
        self.day_weight["5"] = [False,False,False,False,False,True,True,True,True] # friday
        self.day_weight["6"] = [False,False,False,False,False,False,False,False,True] # saturday
        self.return_hours = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        self.return_hours += ([16]*5)
        self.return_hours+=([17]*10)
        self.return_hours+=([18]*10)
        self.return_hours+=([19]*10)
        self.return_hours+=([20]*20)
        self.return_hours+=([21]*40)
        self.return_hours+=([22]*60)
        self.return_hours+=([23]*80)
        self.return_hours+=([24]*200)



    def time_lapse(self):
        self.min += 5

        if (self.min == 60):
            self.hour += 1
            self.min = 0

            if (self.hour == 24):
                self.hour = 0
                self.day += 1
                self.curDate += 1

                if (self.day == 7):
                    self.day = 0


    def license_gen(self):
        import random

        plate = ""
        ran_char = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9"]
        
        for i in range(7):
            plate += random.choice(ran_char)

        return plate

    def car_gen(self,num_cars):
        car_list = []
        plate_list = []
        num = 0
        while not (num >= num_cars):
            plate_num = self.license_gen()

            if (plate_num not in plate_list):
                plate_list.append(plate_num)
                num += 1

        for i in range(num_cars):
            car_list.append(Car(plate_list[i]))
        return car_list

    def calc_return(self):
        import math
        import random
        prob_list = []
        for i in range(25):
            for j in range(int(50*(math.exp(2*i/24)/math.exp(2)))):
                prob_list.append(i)
        return (random.choice(prob_list))
        
    def update(self):
        import random

        for i in range(len(self.car_list)):
            if (self.car_list[i].in_lot == True):
                if (self.hour == self.car_list[i].leave_hour and self.min == self.car_list[i].leave_min):
                    self.pm.removeFromLocation(self.car_list[i].plate,self.car_list[i].location)
                    print("Left: " + self.car_list[i].plate)

                    self.car_list[i].arrive_hour = (self.car_list[i].arrive_hour + random.choice(self.return_hours))%24
                    self.car_list[i].arrive_min += random.randint(-1,1)*5
                    if(self.car_list[i].arrive_min == -5):
                        self.car_list[i].arrive_min = 55
                        self.car_list[i].arrive_hour -= 1
                        if (self.car_list[i].arrive_hour == -1):
                            self.car_list[i].arrive_hour = 23  

                    self.car_list[i].return_day = random.choice(self.day_weight[str((self.day+1)%7)])
                    self.car_list[i].in_lot = False
                    print("Scheduled Arrival: " + str(self.car_list[i].arrive_hour+100)[1:]+ ":" + str(self.car_list[i].arrive_min+100)[1:] + " Return Tomorrow? " + str(self.car_list[i].return_day))


            else:
                if ((self.hour == self.car_list[i].arrive_hour) and (self.min == self.car_list[i].arrive_min) and (self.car_list[i].return_day)):
                    self.car_list[i].location = random.choice(self.pm.lotsOpen())
                    self.pm.addToLocation(self.car_list[i].plate,self.car_list[i].location)
                    print("Arrived: " + self.car_list[i].plate)
                    self.car_list[i].leave_hour = (self.car_list[i].arrive_hour + random.randint(2,10)) % 24
                    self.car_list[i].leave_min += random.randint(-1,1)*5
                    if(self.car_list[i].leave_min == -5):
                        self.car_list[i].leave_min = 55
                        self.car_list[i].leave_hour -= 1
                        if (self.car_list[i].leave_hour == -1):
                            self.car_list[i].leave_hour = 23   

                    elif(self.car_list[i].leave_min == 60):
                        self.car_list[i].leave_min = 0
                        self.car_list[i].leave_hour += 1
                        if (self.car_list[i].leave_hour == 24):
                            self.car_list[i].leave_hour = 00     
                        
                    print("Scheduled Departure: " + str(self.car_list[i].leave_hour+100)[1:] + ":" + str(self.car_list[i].leave_min+100)[1:])

                    self.car_list[i].in_lot = True

                elif not(self.car_list[i].return_day) and (self.hour == self.car_list[i].arrive_hour) and (self.min == self.car_list[i].arrive_min):
                    self.car_list[i].return_day = random.choice(self.day_weight[str((self.day+1)%7)])

        self.pm.updateLotCounts("R4",self.curDate, self.day, str(self.hour+100)[1:]+str(self.min+100)[1:])
        self.pm.updateLotCounts("R3",self.curDate, self.day, str(self.hour+100)[1:]+str(self.min+100)[1:])
        self.pm.updateLotCounts("R2",self.curDate, self.day, str(self.hour+100)[1:]+str(self.min+100)[1:])        


sim = Sim_Run(1000)
while(True):
    sim.time_lapse()
    sim.update()
    print(str(sim.hour+100)[1:]+str(sim.min+100)[1:])   
    time.sleep(1)
