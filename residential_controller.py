class Column:
    def __init__(self, _id, _amountOfFloors, _amountOfElevators):
        self.ID = _id 
        self.status = 'online'
        self.amountOfFloors = _amountOfFloors
        self.elevatorList = []
        self.callButtonList = []
        self.createElevators(_amountOfFloors, _amountOfElevators)
        self.createCallButtons(_amountOfFloors)

    def createElevators(self, _amountOfFloors, _amountOfElevators):
        elevatorID = 1
        for i in range(_amountOfElevators):
            self.elevatorList.append(Elevator(elevatorID, _amountOfFloors)) 
            elevatorID += 1

    def createCallButtons(self, _amountOfFloors):
        buttonFloor = 1
        callButtonID = 1
        for i in range(_amountOfFloors):
            if buttonFloor < _amountOfFloors:
                callButton = CallButton(callButtonID, buttonFloor, 'up')
                self.callButtonList.append(callButton)
                callButtonID += 1
            if buttonFloor > 1:
                self.callButtonList.append(CallButton(callButtonID, buttonFloor, 'down'))
                callButtonID += 1
            buttonFloor += 1

    def requestElevator(self, floor, direction):
        elevator = self.findElevator(floor, direction)
        elevator.floorRequestList.append(floor)
        elevator.sortFloorList()
        elevator.move()

        return elevator

    
    
    def findElevator(self, requestedFloor, requestedDirection):
        bestElevatorInformation = {
            'bestElevator': 0,
            'bestScore': 5,
            'referanceGap': 10000000, 
        }
            
        for elevator in self.elevatorList:
            if requestedFloor == elevator.currentFloor and elevator.status == 'stopped' and requestedDirection == elevator.direction:
                bestElevatorInformation = self.checkIfElevatorIsBetter(1, elevator, bestElevatorInformation, requestedFloor)

            elif requestedFloor > elevator.currentFloor and elevator.direction == 'up' and requestedDirection == elevator.direction: 
                bestElevatorInformation = self.checkIfElevatorIsBetter(2, elevator, bestElevatorInformation, requestedFloor)

            elif requestedFloor < elevator.currentFloor and elevator.direction == 'down' and requestedDirection == elevator.direction:
                bestElevatorInformation = self.checkIfElevatorIsBetter(2, elevator, bestElevatorInformation, requestedFloor)

            elif elevator.status == 'idle':
                bestElevatorInformation = self.checkIfElevatorIsBetter(3, elevator, bestElevatorInformation, requestedFloor)

            else:
                bestElevatorInformation = self.checkIfElevatorIsBetter(4, elevator, bestElevatorInformation, requestedFloor)


        return bestElevatorInformation['bestElevator']
       
       
       
    def checkIfElevatorIsBetter(self, scoreToCheck, newElevator, bestElevatorInformation, floor):
        if scoreToCheck < bestElevatorInformation['bestScore']:
            bestElevatorInformation['bestScore'] = scoreToCheck
            bestElevatorInformation['bestElevator'] = newElevator
            bestElevatorInformation['referenceGap'] = abs(newElevator.currentFloor - floor)
        elif bestElevatorInformation['bestScore'] == scoreToCheck:
            gap = abs(newElevator.currentFloor - floor)
            if bestElevatorInformation['referenceGap'] > gap:
                bestElevatorInformation['bestElevator'] = newElevator
                bestElevatorInformation['referenceGap'] = gap 

        return bestElevatorInformation 







class Elevator:
    def __init__(self, _id, _amountOfFloors):
        self.ID = _id 
        self.amountOfFloors = _amountOfFloors
        self.status = 'status'
        self.currentFloor = 1
        self.direction = None
        self.door = Door(_id)
        self.floorRequestButtonList = []
        self.floorRequestList = []
        self.createFloorRequestButton(_amountOfFloors)

    def createFloorRequestButton(self, _amountOfFloors):
        buttonfloor = 1
        floorRequestButtonID = 1
        for i in range (_amountOfFloors):
            self.floorRequestButtonList.append(FloorRequestButton(floorRequestButtonID, buttonfloor))
            buttonfloor += 1
            floorRequestButtonID += 1

    def requestFloor(self, floor):  
        self.floorRequestList.append(floor)
        self.sortFloorList()
        self.move()

    def move(self):
        while len(self.floorRequestList) != 0:
            destination = self.floorRequestList[0]
            self.status = 'moving'
            if (self.currentFloor < destination):
                self.direction = 'up'
                self.sortFloorList()
                while (self.currentFloor < destination):
                    self.screenDisplay = self.currentFloor
                    self.currentFloor += 1 

            elif (self.currentFloor > destination):
                self.destination = 'down'
                self.sortFloorList()
                while (self.currentFloor > destination):
                    self.screenDisplay = self.currentFloor
                    self.currentFloor -= 1

            self.status = 'stopped'
            self.floorRequestList.pop(0)       

        self.status = 'idle' 

    def sortFloorList(self):
        if (self.direction == 'up'):
            self.floorRequestList.sort()
        elif (self.direction == 'down'):
            self.floorRequestList.sort(reverse=True)





class CallButton:
    def __init__(self, _id, _floor, _direction):
        self.ID = _id 
        self.floor = _floor
        self.status = 'status'
        self.direction = _direction 


class FloorRequestButton:
    def __init__(self, _id, _floor):
        self.ID = _id
        self.status = 'status'
        self.floor = _floor


class Door:
    def __init__(self, _id):
        self.ID = _id
        self.status = 'status'
