intensity = 255
decay_rate = 15

food = 150



for i in range(5):
        if i / 2 == 0:
            food += 200
        food = max(intensity - decay_rate, 0)
        print(food)