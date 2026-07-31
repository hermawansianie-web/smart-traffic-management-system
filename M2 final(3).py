"""
Milestone2
Team L2B
Author: Simran Maharana (35322217)
        Sianie Hermawan (35544945)
        Bryant Christian Gunawan (35663405)
        Zixuan Cheng (34824677)
        Yuchao Tian (35322659)

Manager: Bigumjith Dias
"""
import time
import random
from pymata4 import pymata4
import matplotlib.pyplot as plt

distCm = 2
trigPin = 11
echoPin = 12
correctPin = "1234"
maxPinAttempts = 3
pedestrianButton=13
distanceHistory = []
maxHistory = 20
speeds = []

mainGreen=2
mainYellow=3
mainRed=4
sideGreen=5
sideYellow=6
sideRed=7
pedestrianGreen=8
pedestrianFlash=9
pedestrianRed=10

stageOneTime=30
stageTwoTime=3
stageThreeTime=3
stageFourTime=30
stageFiveTime=13
stageSixTime=3

store = [0]
pedestrianPresses = 0
buttonReleased=True

def led_pins(board):
    board.set_pin_mode_digital_output(mainGreen)
    board.set_pin_mode_digital_output(mainYellow)
    board.set_pin_mode_digital_output(mainRed)
    board.set_pin_mode_digital_output(sideGreen)
    board.set_pin_mode_digital_output(sideYellow)
    board.set_pin_mode_digital_output(pedestrianGreen)
    board.set_pin_mode_digital_output(sideRed)
    board.set_pin_mode_digital_output(pedestrianRed)
    board.set_pin_mode_digital_input(pedestrianButton)

def sonar_call_back(data):
    value = data[distCm]
    store[0] = value

def sonar_report():
    return store[0]

def sonarSetup(myBoard, triggerPin, echoPin):
    myBoard.set_pin_mode_sonar(triggerPin, echoPin, sonar_call_back, timeout=200000)
    time.sleep(0.1)

def poll_traffic_sensor(board, silent=False):
    board.sonar_read(trigPin)
    time.sleep(0.1)
    time.time()
    distance = sonar_report()
    
    if not silent:
        print(f"vehicle distance: {distance:.2f} cm")

    if distance is not None:
        distanceHistory.append(distance)
        if len(distanceHistory) > maxHistory:
            distanceHistory.pop(0)
    return distance

def distance_rate(board):
    prev_distance_data = board.sonar_read(trigPin)
    while prev_distance_data is None:
        time.sleep(0.01)
        prev_distance_data = board.sonar_read(trigPin)

    prev_distance = prev_distance_data[0]
    prev_time = time.time()

    try:
        while True:
            distance_data = board.sonar_read(trigPin)
            now = time.time()

            if distance_data is not None:
                distance = distance_data[0]
                delta_d = abs(distance - prev_distance)
                delta_t = now - prev_time

                if delta_t > 0:
                    speed = delta_d / delta_t 
                    speeds.append(speed)
                    print(f"Speed: {speed:.2f} cm/s")

                    prev_distance = distance
                    prev_time = now

            time.sleep(0.1)  

    except KeyboardInterrupt:
        print("Stopped by user.")
        print("Collected speeds:", speeds)
        board.shutdown()

def poll_pedestrian_sensor(board, silent=True):
    global pedestrianPresses, buttonReleased  
    result = board.digital_read(pedestrianButton)
    
    if result[0] == 0 and buttonReleased:  
        pedestrianPresses += 1
        if not silent:  
            print(f"The button has been pressed {pedestrianPresses} times")
        buttonReleased = False 
        time.sleep(0.1)  
    elif result[0] == 1:
        buttonReleased = True
         
def polling_loop(board):
    print("Starting polling loop...")
    startLoopTime = time.time()

    poll_pedestrian_sensor(board)
    time.sleep(random.uniform(1, 5))

    endLoopTime = time.time()
    elapsedTime = endLoopTime - startLoopTime
    print(f"Polling loop cycle completed in {elapsedTime:.2f} seconds.")

def traffic_light_simulation(board):
    global pedestrianPresses,stageOneTime, stageTwoTime, stageThreeTime, stageFourTime, stageFiveTime, stageSixTime
    while True:
        try:
            print('Stage 1: Main road green')
            board.digital_write(mainGreen,1)
            board.digital_write(mainRed,0)
            board.digital_write(mainYellow,0)
            board.digital_write(sideRed,1)
            board.digital_write(sideGreen,0)
            board.digital_write(sideYellow,0)
            board.digital_write(pedestrianRed,1)
            board.digital_write(pedestrianGreen,0)
            for _ in range(stageOneTime):  
                poll_traffic_sensor(board, silent=False)
                poll_pedestrian_sensor(board, silent=False)
                poll_pedestrian_sensor(board)
                time.sleep(1)
            
            print(' Stage 2: Main road yellow')
            board.digital_write(mainYellow,1)
            board.digital_write(mainRed,0)
            board.digital_write(mainGreen,0)
            board.digital_write(pedestrianRed,1)
            board.digital_write(pedestrianGreen,0) 
            board.digital_write(sideRed,0)
            board.digital_write(sideGreen,0)
            board.digital_write(sideRed,1)
            for _ in range(stageTwoTime):  
                poll_traffic_sensor(board, silent=False)
                poll_pedestrian_sensor(board, silent=True)
                poll_traffic_sensor(board) 
                time.sleep(1)

            print(' Stage 3 : Main road red')
            board.digital_write(mainRed,1)
            board.digital_write(mainYellow,0)
            board.digital_write(mainGreen,0)
            board.digital_write(sideRed,1)
            board.digital_write(sideGreen,0)
            board.digital_write(sideYellow,0)
            board.digital_write(pedestrianRed,1)
            board.digital_write(pedestrianGreen,0)
            for _ in range(stageThreeTime):  
                poll_traffic_sensor(board, silent=False)
                poll_pedestrian_sensor(board, silent=False) 
                poll_pedestrian_sensor(board)
                time.sleep(1)
            print(f'pedestrian presses at stage 3 : {pedestrianPresses}')
            pedestrianPresses=0

            print( 'Stage 4: Main road red')
            board.digital_write(sideRed,0)
            board.digital_write(sideGreen,1)
            board.digital_write(sideYellow,0)
            board.digital_write(pedestrianGreen,1)
            board.digital_write(pedestrianRed,0)
            board.digital_write(mainRed,1)
            board.digital_write(mainYellow,0)
            board.digital_write(mainGreen,0)
            for _ in range(stageFourTime):  
                poll_traffic_sensor(board, silent=False)
                poll_pedestrian_sensor(board, silent=True)
                poll_traffic_sensor(board) 
                time.sleep(1)

            print(' Stage 5 : Main road Red')
            board.digital_write(sideGreen,0)
            board.digital_write(sideYellow,1)
            board.digital_write(sideRed,0)
            board.digital_write(pedestrianGreen,1)
            board.digital_write(pedestrianRed,0)
            board.digital_write(mainRed,1)
            board.digital_write(mainGreen,0)
            board.digital_write(mainYellow,0)
            for _ in range(stageFiveTime):
                board.digital_write(pedestrianGreen, 1)
                time.sleep(0.33)
                board.digital_write(pedestrianGreen, 0)
                time.sleep(0.33) 

            for _ in range(3):  
                poll_traffic_sensor(board, silent=False)
                poll_pedestrian_sensor(board, silent=True)
                poll_traffic_sensor(board) 
                time.sleep(1)

            print(' Stage 6 : Main road red')
            board.digital_write(sideYellow,0)
            board.digital_write(sideRed,1)
            board.digital_write(sideGreen,0)
            board.digital_write(pedestrianGreen,0)
            board.digital_write(pedestrianRed,1)
            board.digital_write(mainRed,1)
            board.digital_write(mainGreen,0)
            board.digital_write(mainYellow,0)
            for _ in range(stageSixTime):  
                poll_traffic_sensor(board, silent=False)
                poll_pedestrian_sensor(board, silent=True) 
                poll_traffic_sensor(board)
                time.sleep(1)

            choice = input("Press Enter to restart or type 'menu' to return: ")
            if choice.lower() == "menu":
                board.digital_write(mainRed,0)
                board.digital_write(mainGreen,0)
                board.digital_write(mainYellow,0)
                board.digital_write(sideGreen,0)
                board.digital_write(sideRed,0)
                board.digital_write(sideYellow,0)
                board.digital_write(pedestrianGreen,0)
                board.digital_write(pedestrianRed,0)
                break

        except KeyboardInterrupt:
            print("\nInterrupted. Shutting down...")
            board.digital_write(pedestrianRed,0)
            board.digital_write(mainRed,0)
            board.digital_write(mainGreen,0)
            board.digital_write(mainYellow,0)
            board.digital_write(sideGreen,0)
            board.digital_write(sideRed,0)
            board.digital_write(sideYellow,0)
            board.digital_write(pedestrianGreen,0)
            board.digital_write(pedestrianRed,0)
            return

def traffic_graph(board):
    try:
        while True:
            poll_pedestrian_sensor(board)
        
            if len(distanceHistory) >= 20:
                seconds = list(range(1, 21))
                plt.plot(seconds, distanceHistory[-20:], "r--")
                plt.xlabel("Second(s)")
                plt.ylabel("Distance (cm)")
                plt.title("Traffic Distance - Last 20 Seconds")
                plt.ylim(0, 60)
                plt.legend(["Traffic Distance"])
                plt.show()
                plt.pause(0.1)

            else:
                distance = poll_traffic_sensor (board)
                print(f"\nNot enough data to generate the graph. Only {len(distanceHistory)} readings available.")
                print(f"vehicle distance: {distance:.2f} cm")
                print("waiting for more data")
                
            print(f"Pedestrian Button Presses: {pedestrianPresses}")
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nReturning to Main Menu...")
        plt.close()

def stage_time_adjustment():
    global stageOneTime, stageTwoTime, stageThreeTime, stageFourTime, stageFiveTime, stageSixTime
    print("Enter The Stage to modify:\n1\n2\n3\n4\n5\n6")
    chooseStage=int(input())
    if chooseStage==1:
        while True:
            newTime=int(input("\nInput new duration (between 15-45 seconds):"))
            if 15<=newTime<=45:
                stageOneTime=newTime
                return stageOneTime
            else:
                print("Invalid Input, Input should be 15-45 seconds")
                continue
    elif chooseStage==2:
        while True:
            newTime=int(input("\nInput new duration (between 3-6 seconds):"))
            if 3<=newTime<=6:
                stageTwoTime=newTime
                return stageTwoTime
            else:
                print("Invalid Input, Input should be 3-6 seconds")
                continue
    elif chooseStage==3:
        while True:
            newTime=int(input("\nInput new duration (between 3-6 seconds):"))
            if 3<=newTime<=6:
                stageThreeTime=newTime
                return stageThreeTime
            else:
                print("Invalid Input, Input should be 3-6 seconds")
                continue
    elif chooseStage==4:
        while True:
            newTime=int(input("\nInput new duration (between 15-45 seconds):"))
            if 15<=newTime<=45:
                stageFourTime=newTime
                return stageFourTime
            else:
                print("Invalid Input, Input should be 15-45 seconds")
                continue
    elif chooseStage==5:
        while True:
            newTime=int(input("\nInput new duration (between 3-6 seconds):"))
            if 3<=newTime<=6:
                stageFiveTime=newTime
                return stageFiveTime
            else:
                print("Invalid Input, Input should be between 3-6 seconds")
                continue
    elif chooseStage==6:
        while True:
            newTime=int(input("\nInput new duration (between 3-6 seconds):"))
            if 3<=newTime<=6:
                stageSixTime=newTime
                return stageSixTime
            else:
                print("Invalid Input, Input should be 3-6 seconds")
                continue
def change_Password():
    global correctPin
    while True:
        newPassword=int(input("Please Enter New 4 Digit Passcode:\n"))
        currentPassword=int(correctPin)
        if newPassword==currentPassword:
            print("New password cannot be the same with the current password, please try again.")
            continue
        elif len(str(newPassword))!=4:
            print("Passcode must be 4 digits, please try again.")
            continue
        elif newPassword!=currentPassword:
            while True:
                confirmation=int(input("Confirm new Pin:\n"))
                if confirmation==newPassword:
                    correctPin=str(newPassword)
                    return correctPin
                elif confirmation!=newPassword:
                    print("Error, input should match new Pin, please try again.")
                    continue

        else:
            print("Invalid Input, please try again.")
def system_main_menu(board):
    while True:
        userInput = int(input("Main Menu:\n1. Normal Operation\n2. Data Observation Mode\n3. Maintenance Adjustment Mode\n4. Exit\nSelect an option (1-4):"))

        if userInput == 1:
            print('Normal Operation Mode selected. Starting Traffic Light Simulation...')
            traffic_light_simulation(board)  
            poll_pedestrian_sensor(board)
            distance_rate(board)
            polling_loop(board)
        elif userInput == 2:
            print('Data Observation Mode selected.')
            traffic_graph(board)
        elif userInput == 3:
            print('Maintenance Adjustment Mode selected.')
            maintenance_adjustment_mode()  
        elif userInput == 4:
            print('Exiting the system. Goodbye!')
            break
        else:
            print('Invalid input. Please try again.')

def maintenance_adjustment_mode():
    global correctPin, stageOneTime, stageTwoTime, stageThreeTime, stageFourTime, stageFiveTime, stageSixTime
    cooldownTime = 120
    cooldownTimeMin = round(cooldownTime / 60, 2)
    times = 0

    while times <= 2:
        try:
            attempt =input("Enter PIN:\n")
            if attempt == correctPin:
                print("Access granted. Entering Maintenance Mode...")
                break
            else:
                times += 1
                if times > 2:
                    print(f"MAM unavailable, please try again in {cooldownTimeMin} minutes.")
                    time.sleep(cooldownTime)
                    return
                else:
                    print("Invalid. Please try again.")
        except KeyboardInterrupt:
            print("\nReturning to main menu")
            return
        except ValueError:
            print("PIN must be a number. Please try again.")

    while True:
        try:
            print("\n--- Maintenance Mode ---")
            print("1. Calibrate System")
            print("2. Change Pin")
            print("3. Simulation Time Adjustment")
            print("4. Return to Main Menu")

            choice = input("Select an option: ")

            if choice == "1":
                print("Calibrating system...")

            elif choice == "2":
                change_Password()
                print("Pin has been changed.")
                
            elif choice == "3":
                stage_time_adjustment()
                print("Updating system settings...")

                
            elif choice == "4":
                print("Exiting Maintenance Mode...")
                return
            else:
                print("Invalid input. Please try again.")
        except KeyboardInterrupt:
            print("\nExiting Maintenance Mode...")
            return

def main():
    board=pymata4.Pymata4()
    led_pins(board)
    sonarSetup (board,trigPin,echoPin)
    system_main_menu(board)
    board.shutdown()

if __name__ == "__main__":
    main()

