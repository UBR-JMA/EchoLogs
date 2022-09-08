#Get yes or no input from the user. Returns a boolean.
#Prompt - string: a yes or no question ending with a question mark (Ex: 'Is this a question?')
def GetYesNo(prompt = ''):
    response = ''
    prompt = prompt + ' Y/N: '
    while response != 'Y' and response != 'N':
        response = input(prompt)
        response = response.upper()
    return True if response == 'Y' else False

# Get an integer from the user. Returns an int.
# min - int: the minimum integer the user can choose from.
# max - int: the maximum integer the user can choose from.
# prompt - string: the message used to instruct the user. Default: Pick an integer between min and max. 
def GetInt(min, max, prompt = ''):
    valid_response = False
    response = -1

    # set default prompt if none provided
    if prompt == '':
        prompt = 'Pick an integer between ' + str(min) + ' and ' + str(max) + ': '

    # validate input    
    while valid_response is False:
        try: 
            response = input(prompt)
            response = int(response)
            # must be between min and max
            if response < min or response > max:
                print(f'The number must be an integer between {min} and {max}.')
                valid_response = False
            else:
                valid_response = True
        # must be an integer
        except:
            print(str(response) + ' is not an integer. ')
            valid_response = False

    # return validated integer
    return response


# swap two given elements of a list
def swapPositions(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list

# Situation: a list has all the values needed for a dictionary
# Problem: the keys are values and the values are keys
# Solution: swap the position of each key-value pair in the list
# example: [3, Apples, 6, Bananas] -> [Apples, 3, Bananas, 6] 
def listKeyValueSwap(list):
    for i in range(0, len(list)-1, 2):
        swapPositions(list, i, i+1)
    return list
    
# convert list to dictionary
def convertListToDict(list):
    return {list[i]: list[i + 1] for i in range(0, len(list), 2)}