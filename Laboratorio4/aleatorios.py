from random import randint
import random
# for i in range(60):
#     print(randint(1,9))

vector = [24,32,40,45,48,50,52,55,60,70,75,77,78,80,88,90,100,125,175]
for i in range(60):
    print(random.sample(vector,1))
