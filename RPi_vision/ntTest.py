import ntcore
import time

teamNumber = 3636
ntInstance = ntcore.NetworkTableInstance.getDefault()
ntInstance.setServerTeam(teamNumber)
table = ntInstance.getTable("RPiTable")
x = 0.0
xPublisher = ntInstance.getDoubleTopic("x").publish()
xPublisher.set(x)
deltaX = 1
deltaXEntry = table.getIntegerTopic("deltaX").getEntry(deltaX)
deltaXEntry.set(deltaX)

while True:
    deltaX = deltaXEntry.get()
    x += deltaX
    xPublisher.set(x)
    time.sleep(1)
    print(x)
