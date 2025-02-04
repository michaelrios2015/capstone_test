weight = [10, 20, 30]
profit = [60, 100, 120]
W = 50

def knapSack(W, weight, profit):
    # so in theory you would need to check every permuation that works
    # and then compare all of those prices, in practice I am fairly certain the is 
    # not an np sovable problem or something like that I forget the name so we are just approximate it
    # anyway so I will just fill it with the most expensive item 

    tot_profit = 0 
    tot_weight = 0
    knapSack = []
    full = False

    while not full or len(profit) > 1: 
        # find the maxium profit item
        max_value = max(profit)
        print(max_value)
    
    # find the index of that 
        index = profit.index(max_value)
        print(index)

    # see if it fits
        if W >= weight[index]:
        # put the item into the knapsack   
            tot_profit =+ max_value
            tot_weight =+ weight[index]

        # check to see if the knapsak is full
            if tot_weight == W:
                full = True
            W =- weight[index]   

        # # now we earse it becuase it has either been put in the knapsack or it weighed too much    
        del weight[index]
        del profit[index]

        print(weight)


knapSack(W, weight, profit)