#!/usr/bin/env python3

'''
We create a binary tree with Node objects, with a list of '0' and '1' indicating if an item is taken.
'''


# Initialize the different classes
class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

class Item:
    def __init__(self, value, mass, unit_value):
        self.value = value
        self.mass = mass
        self.unit_value = unit_value


# Create a list of items
items = []

items.append(Item(10,2,5))
items.append(Item(10,4,2.5))
items.append(Item(12,6,2))
items.append(Item(18,9,2))

# test
# print(items[0].value)

# capacity
c = 15

total_value = 0
for i in range(0, len(items)):
    total_value += items[i].value


# Helper function to find GFC
# Same as greedy's partial items for knapsack
def GFC(items, mass=c):
    # return this value
    greed_value = 0

    temp_capacity = mass

    # if we can take the whole item, we take it
    # otherwise we take whatever unit is left

    for item in items:
        if item.mass <= temp_capacity:
            greed_value += item.value
            temp_capacity -= item.mass
        else:
            greed_value += (item.unit_value * temp_capacity)
            temp_capacity = 0
    return greed_value

# Helper function to find FFC
# Just the greedy problem 
def FFC(items, mass=c):
    # return this value
    greed_value = 0

    temp_capacity = mass

    # if we can take the whole item, we take it
    # otherwise we leave it

    for item in items:
        if item.mass <= temp_capacity:
            greed_value += item.value
            temp_capacity -= item.mass

    return greed_value

# print(GFC(items[2:]))
# print(FFC(items))

# print(x)

l_global = total_value - GFC(items)
u_global = total_value - FFC(items)

print(u_global, l_global)
root = Node([None] * len(items))

root.left = Node([0] + [None] * (len(items)-1))

root.right = Node([1] + [None] * (len(items)-1))

# stores all the partial solutions
P = []
P.append(root.left)
P.append(root.right)

# iterates through P
# for p in P:
    # print("p.data: ",p.data)
    # temp_left = p.data[:]
    # temp_left[1] = 0
    # p.left = Node(temp_left)
    
    # temp_right = p.data[:]
    # temp_right[1] = 1
    # p.right = Node(temp_right)

    # print("p.left.data",p.left.data)
    # print("p.right.data", p.right.data)
    # ===================================
    # print(p.data[1])
    # print(p.left)
    # print(p.right)

# print(root.data)
# print(root.left.data)
# print(root.right.data)

# Now we begin constructing the tree

# index of the items we're taking or leaving


n = 1

while (n < len(items)):

    print(n)

    temp_P = []

    for p in P:

        print("p.data", p.data)

        # taken_list = p.left.data[:n]

        # We check if this solution is actually viable:
        mass = p.data[:n]
        for i in range(0,n):
            mass[i] = mass[i] * items[i].mass

        mass = sum(mass)
        print("mass ",mass)
        
        # If the solution is actually viable, we calculate lq and uq
        if mass <= c:
            # We need CSF + GFC for lq
            CSF = p.data[:n]
            for i in range(0,n):
                CSF[i] = CSF[i] * items[i].value
            CSF = sum(CSF)
            print("CSF ",CSF)

            print("n",n)
            gfc = GFC(items[n:],c-mass)
            ffc = FFC(items[n:],c-mass)

            print("GFC ",gfc)
            print("FFC ",ffc)

            lq = total_value - gfc - CSF
            uq = total_value - ffc - CSF

            print("lq ",lq)
            print("uq ",uq)

            # Then we only continue down left and right with the solution if its lq is smaller than u_global
            if lq <= u_global:
                # also update u_global if uq is smaller
                if uq < u_global:
                    u_global = uq
                
                temp_left = p.data[:]
                temp_left[n] = 0
                p.left = Node(temp_left)
                temp_P.append(p.left)

                temp_right = p.data[:]
                temp_right[n] = 1
                p.right = Node(temp_right)
                temp_P.append(p.right)

    print("updated u_global ", u_global)
    P = temp_P[:]
    n += 1

for p in P:
    print(p.data)


'''data_test = [0,1,None,None]
CSF = data_test[:2]

for i in range(0,2):
    CSF[i] = CSF[i] * items[i].value

print("CSF: ",CSF)
print("Sum of CSF ", sum(CSF))'''



# If we come to a upper bound that is greater than u_global, discard it

