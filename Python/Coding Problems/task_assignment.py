#!/usr/bin/env python3


'''
PLEASE NOTE: THIS CODE USES NUMPY, SO IF YOU DON'T HAVE IT, IT WILL RUN INTO AN ERROR WHEN YOU RUN. 
INSTALL NUMPY IN YOUR PATH BY USING python3 -m pip install numpy.
You may have to upgrade pip: pip install --user --upgrade pip 
'''

from heapq import heapify, heappush, heappop

import numpy as np

task_List = [[10,15,4,12,9],[7,18,3,10,16],[4,5,14,12,10],[17,2,18,6,21],[21,18,2,10,25]]

# Helper function for guaranteed future cost
def get_gfc(Q):
  gfc = 0

  # Simply goes through each list in the Q table, and picks the minimum
  for i in range(0,len(Q)):
    gfc += min(Q[i])

  return gfc

# Helper function for feasible future cost
# Same as U_Global
def get_ffc(Q):
  ffc = 0
  tasks_taken = []

  # Pointer i looks at each worker P
  for i in range(0,len(Q)):

    temp_min = max(Q[i])
    temp_index = 0

    # Pointer j looks at each task T for worker P
    for j in range(0, len(Q[i])):
      if (Q[i][j] < temp_min and j not in tasks_taken):
        temp_min = Q[i][j]
        temp_index = j
    
    ffc += temp_min
    tasks_taken.append(temp_index)

  return ffc

def get_csf(jobs, temp_tasks):

    csf = 0

    for i in range(0, len(temp_tasks)):
        csf += jobs[i][temp_tasks[i]]

    return csf


# B & B
# returns a list of assigned jobs
def job_assignment(jobs):

    u_global = get_ffc(task_List)
    print("u_global: ", u_global)

    minimal_total_cost = 0
    solutions_investigated = 0

    P = []
    heapify(P)

    # Let's start with a base case:

    temp_Q = []

    # i points to task i 
    for i in range(0, len(jobs)):
        # There will be 3 elements in q as a tuple
        # int lq (CSF + GFC), int uq (CSF + FFC), and task_assigned as a list, which stores tasks assigned to P_index
        # Currently CSF is 0 + task time of worker 1 in task list 
        # and the task_assigned should just contain 1 element for worker 1, at index 0, the index of the task assigned

        updated_table = np.array(jobs)
        updated_table = np.delete(updated_table, (0), axis = 0)
        updated_table = np.delete(updated_table, (i), axis = 1)

        #print("i: ", i)
        #print("CSF: ", jobs[0][i])
        #print("GFC: ", GFC(updated_table))
        #print("FFC: ", FFC(updated_table))

        q = (jobs[0][i] + get_gfc(updated_table), jobs[0][i] + get_ffc(updated_table), [i])
        if q[1] < u_global:
            u_global = q[1]
        temp_Q.append( q )


    # Discard and update partial solutions
    for i in range(0, len(temp_Q)):
        # If lower bound is higher than global upper bound
        if temp_Q[i][0] < u_global:
            heappush(P, temp_Q[i])
            solutions_investigated += 1

    #print(P)


    # Stores complete solutions
    S = []
    heapify(S)

    while (P != []):

        # else
        temp_P = [] # Stores viable partial solutions
        heapify(temp_P)

        for p in P:

            if len(p[2]) != 5:

                # We try assigning the remaining tasks to the next worker index in p[2],
                # that is going to be at len(p[2]) + 1
                # and we will do it in a for loop looping through the remaining tasks, len(jobs[0] - (len(p[2]) + 1))


                full_tasks = np.arange(len(jobs[0]))
                assigned_tasks = np.array(p[2])

                # Deletes the tasks already assigned

                remaining_tasks = np.setdiff1d(full_tasks,assigned_tasks)

                #print("remaining tasks ", remaining_tasks)

                
                #print(remaining_tasks)
                # Create a new list where p[2] concats with all possible remaining tasks at worker n
                for g in range(0, len(remaining_tasks)):
                    #print(g)
                    #print("p[2]", assigned_tasks)
                    #print("remaining task", remaining_tasks[g])

                    temp_tasks = np.append(assigned_tasks,remaining_tasks[g])  
                    #print("temp_tasks",temp_tasks)
                
                    #print("temp_tasks",temp_tasks)

                    #print("="*30)


                    # To calculate lq and uq, we get the GFC and FFC of the tasks_List up to the ith row and columns listed in p[2]
                    updated_table = np.array(jobs)

                    #print(updated_table)

                    # delete np arrays up to row i
                    deleting_rows = []
                    #print(p[2])
                    for i in range(0, len(temp_tasks)):
                        deleting_rows.append(i)
                    #print(deleting_rows)
                    updated_table = np.delete(updated_table, deleting_rows, axis = 0)
                    

                    # delete column j in p[2]
                    deleting_columns = []
                    for j in range(0, len(temp_tasks)):
                        deleting_columns.append(temp_tasks[j])
                    
                    updated_table = np.delete(updated_table, deleting_columns, axis = 1)

                    #print("="* 30) 

                    #print(updated_table)
                    #print(" temp tasks: ", temp_tasks)

                    CSF = get_csf(jobs,temp_tasks)

                    #print("CSF ",CSF)

                    lq = CSF + get_gfc(updated_table)
                    uq = CSF + get_ffc(updated_table)

                    #print("lq, uq ", lq, uq)


                    # check if its bounds are within u_global
                    if lq <= u_global:
                        
                        # also update u_global if uq is smaller
                        if uq <= u_global:
                            u_global = uq
                    
                        # since it's within u_global, we add it to the list of viable solutions
                        heappush(temp_P, (lq,uq,temp_tasks.tolist()))
                        solutions_investigated += 1
                        # print("got to the end ",temp_P)

                    print("updated u_global: ", u_global)

            # If the tasks are all assigned, it is a complete solution 
            else:
                heappush(S, p)

            P = []
            heapify(P)

            P = temp_P

            #print("P: ", P)


    print("Solution is: ",S[0])
    minimal_total_cost = get_csf(jobs,S[0][2])

    return minimal_total_cost, S[0][2], solutions_investigated


# Brute force
# returns a list of assigned jobs
# simply does not check for u_global updates
def brute_force(jobs):

    minimal_total_cost = 0
    solutions_investigated = 0


    P = []
    heapify(P)

    # Let's start with a base case:

    temp_Q = []

    # i points to task i 
    for i in range(0, len(jobs)):
        # There will be 3 elements in q as a tuple
        # int lq (CSF + GFC), int uq (CSF + FFC), and task_assigned as a list, which stores tasks assigned to P_index
        # Currently CSF is 0 + task time of worker 1 in task list 
        # and the task_assigned should just contain 1 element for worker 1, at index 0, the index of the task assigned

        updated_table = np.array(jobs)
        updated_table = np.delete(updated_table, (0), axis = 0)
        updated_table = np.delete(updated_table, (i), axis = 1)

        #print("i: ", i)
        #print("CSF: ", jobs[0][i])
        #print("GFC: ", GFC(updated_table))
        #print("FFC: ", FFC(updated_table))

        q = (jobs[0][i] + get_gfc(updated_table), jobs[0][i] + get_ffc(updated_table), [i])
        temp_Q.append( q )

    for i in range(0, len(temp_Q)):
        heappush(P, temp_Q[i])
        solutions_investigated += 1

    #print(P)


    # Stores complete solutions
    S = []
    heapify(S)

    while (P != []):

        # else
        temp_P = [] # Stores viable partial solutions
        heapify(temp_P)

        for p in P:

            if len(p[2]) != 5:

                # We try assigning the remaining tasks to the next worker index in p[2],
                # that is going to be at len(p[2]) + 1
                # and we will do it in a for loop looping through the remaining tasks, len(jobs[0] - (len(p[2]) + 1))


                full_tasks = np.arange(len(jobs[0]))
                assigned_tasks = np.array(p[2])

                # Deletes the tasks already assigned

                remaining_tasks = np.setdiff1d(full_tasks,assigned_tasks)

                #print("remaining tasks ", remaining_tasks)

                
                #print(remaining_tasks)
                # Create a new list where p[2] concats with all possible remaining tasks at worker n
                for g in range(0, len(remaining_tasks)):
                    #print(g)
                    #print("p[2]", assigned_tasks)
                    #print("remaining task", remaining_tasks[g])

                    temp_tasks = np.append(assigned_tasks,remaining_tasks[g])  
                    #print("temp_tasks",temp_tasks)
                
                    #print("temp_tasks",temp_tasks)

                    #print("="*30)


                    # To calculate lq and uq, we get the GFC and FFC of the tasks_List up to the ith row and columns listed in p[2]
                    updated_table = np.array(jobs)

                    #print(updated_table)

                    # delete np arrays up to row i
                    deleting_rows = []
                    #print(p[2])
                    for i in range(0, len(temp_tasks)):
                        deleting_rows.append(i)
                    #print(deleting_rows)
                    updated_table = np.delete(updated_table, deleting_rows, axis = 0)
                    

                    # delete column j in p[2]
                    deleting_columns = []
                    for j in range(0, len(temp_tasks)):
                        deleting_columns.append(temp_tasks[j])
                    
                    updated_table = np.delete(updated_table, deleting_columns, axis = 1)

                    #print("="* 30) 

                    #print(updated_table)
                    #print(" temp tasks: ", temp_tasks)

                    CSF = get_csf(jobs,temp_tasks)

                    #print("CSF ",CSF)

                    lq = CSF + get_gfc(updated_table)
                    uq = CSF + get_ffc(updated_table)

                    #print("lq, uq ", lq, uq)

                    # Then we only pop the element in the heap
                    # heappop(P)

                    heappush(temp_P, (lq,uq,temp_tasks.tolist()))
                    solutions_investigated += 1


            # If the tasks are all assigned, it is a complete solution 
            else:
                heappush(S, p)

            P = []
            heapify(P)

            P = temp_P

            #print("P: ", P)


    print("Solution is: ",S[0])
    minimal_total_cost = get_csf(jobs,S[0][2])

    return minimal_total_cost, S[0][2], solutions_investigated


#print(job_assignment(task_List))
# Solution is:  (27, 27, [4, 3, 0, 1, 2])
# (27, [4, 3, 0, 1, 2], 10)
#print(brute_force(task_List))
# Solution is:  (27, 27, [4, 3, 0, 1, 2])
# (27, [4, 3, 0, 1, 2], 325)


