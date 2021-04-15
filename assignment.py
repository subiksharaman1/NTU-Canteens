import pygame
from PIL import Image
import time
import pandas as pd
import math


# load dataset for keyword dictionary - provided
def load_stall_keywords(data_location="canteens.xlsx"):
    # get list of canteens and stalls
    canteen_data = pd.read_excel(data_location, trim_ws=True)
    canteens = canteen_data['Canteen'].unique()
    canteens = sorted(canteens, key=str.lower)

    stalls = canteen_data['Stall'].unique()
    stalls = sorted(stalls, key=str.lower)

    keywords = {}
    for canteen in canteens:
        keywords[canteen] = {}

    copy = canteen_data.copy()
    copy.drop_duplicates(subset="Stall", inplace=True)
    stall_keywords_intermediate = copy.set_index('Stall')['Keywords'].to_dict()
    stall_canteen_intermediate = copy.set_index('Stall')['Canteen'].to_dict()

    for stall in stalls:
        stall_keywords = stall_keywords_intermediate[stall]
        stall_canteen = stall_canteen_intermediate[stall]
        keywords[stall_canteen][stall] = stall_keywords

    return keywords

# load dataset for price dictionary - provided
def load_stall_prices(data_location: object = "canteens.xlsx") -> object:
    # get list of canteens and stalls
    canteen_data = pd.read_excel(data_location, trim_ws=True)
    canteens = canteen_data['Canteen'].unique()
    canteens = sorted(canteens, key=str.lower)

    stalls = canteen_data['Stall'].unique()
    stalls = sorted(stalls, key=str.lower)

    prices = {}
    for canteen in canteens:
        prices[canteen] = {}

    copy = canteen_data.copy()
    copy.drop_duplicates(subset="Stall", inplace=True)
    stall_prices_intermediate = copy.set_index('Stall')['Price'].to_dict()
    stall_canteen_intermediate = copy.set_index('Stall')['Canteen'].to_dict()

    for stall in stalls:
        stall_price = stall_prices_intermediate[stall]
        stall_canteen = stall_canteen_intermediate[stall]
        prices[stall_canteen][stall] = stall_price

    return prices


# load dataset for location dictionary - provided
def load_canteen_location(data_location="canteens.xlsx"):
    # get list of canteens
    canteen_data = pd.read_excel(data_location, trim_ws=True)
    canteens = canteen_data['Canteen'].unique()
    canteens = sorted(canteens, key=str.lower)

    # get dictionary of {canteen:[x,y],}
    canteen_locations = {}
    for canteen in canteens:
        copy = canteen_data.copy()
        copy.drop_duplicates(subset="Canteen", inplace=True)
        canteen_locations_intermediate = copy.set_index('Canteen')['Location'].to_dict()
    for canteen in canteens:
        canteen_locations[canteen] = [int(canteen_locations_intermediate[canteen].split(',')[0]),
                                      int(canteen_locations_intermediate[canteen].split(',')[1])]

    return canteen_locations


# get user's location with the use of PyGame - provided
def get_user_location_interface():
    # get image dimensions
    image_location = 'NTUcampus.jpg'
    pin_location = 'pin.png'
    screen_title = "NTU Map"
    image = Image.open(image_location)
    image_width_original, image_height_original = image.size
    scaled_width = image_width_original
    scaled_height = image_height_original
    pinIm = pygame.image.load(pin_location)
    pinIm_scaled = pygame.transform.scale(pinIm, (60, 60))
    # initialize pygame
    pygame.init()
    # set screen height and width to that of the image
    screen = pygame.display.set_mode([image_width_original, image_height_original])
    # set title of screen
    pygame.display.set_caption(screen_title)
    # read image file and rescale it to the window size
    screenIm = pygame.image.load(image_location)

    # add the image over the screen object
    screen.blit(screenIm, (0, 0))
    # will update the contents of the entire display window
    pygame.display.flip()

    # loop for the whole interface remain active
    while True:
        # checking if input detected
        pygame.event.pump()
        event = pygame.event.wait()
        # closing the window
        if event.type == pygame.QUIT:
            pygame.display.quit()
            mouseX_scaled = None
            mouseY_scaled = None
            break
        # resizing the window
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(
                event.dict['size'], pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
            screen.blit(pygame.transform.scale(screenIm, event.dict['size']), (0, 0))
            scaled_height = event.dict['h']
            scaled_width = event.dict['w']
            pygame.display.flip()
        # getting coordinate
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # get outputs of Mouseclick event handler
            (mouseX, mouseY) = pygame.mouse.get_pos()
            # paste pin on correct position
            screen.blit(pinIm_scaled, (mouseX - 25, mouseY - 45))
            pygame.display.flip()
            # return coordinates to original scale
            mouseY_scaled = int(mouseX * 1281 / scaled_width)
            mouseX_scaled = int(mouseY * 1550 / scaled_height)
            # delay to prevent message box from dropping down
            time.sleep(0.2)
            break

    pygame.quit()
    pygame.init()
    return mouseX_scaled, mouseY_scaled

# Keyword-based Search Function - to be implemented
def search_by_keyword(keywords):
    #To prompt user for input
    keyword_input = input("Enter type of food: ").lower().split(" ")

    #To print error message
    if keyword_input == [''] or keyword_input == ['','']:
        print("No input found. Please try again.")
    else:
        FoodStalls = {}
        for stall_canteen in keywords:
            for stall in keywords[stall_canteen]:
                keyword_to_check = keywords[stall_canteen][stall].lower().split(", ")
                count = 0
                for each_keyword in keyword_input:
                    if each_keyword in keyword_to_check:
                        count += 1
                        FoodStalls[stall_canteen + " - " + stall] = count

        # To print results
        print("Food stalls found: " + str(len(FoodStalls)))
        if len(FoodStalls) == 0:
            print("No food stall found with input keyword."); return
        else:
            for n in range(len(keyword_input), 0, -1):
                print("Food stalls that match", n, "keywords: ");
                count = 0
                for x in FoodStalls:
                    if FoodStalls[x] == n:
                        print(x)
                        count += 1
                if count == 0:
                    print("None")

# Price-based Search Function - to be implemented
def search_by_price(keywords):
    # To prompt user for input
    prices = load_stall_prices()
    keyword_input = input("Enter type of food: ").lower().split(" ")

    # To print error message
    if keyword_input == [''] or keyword_input == ['', '']:
        print("No input found. Please try again.")
    # Otherwise
    else:
        FoodStalls = []
        def myFunc(sort):
            return sort["Price"]
        for stall_canteen in keywords:
            for stall in keywords[stall_canteen]:
                keyword_to_check = keywords[stall_canteen][stall].lower().split(", ")
                for each_keyword in keyword_input:
                    if each_keyword in keyword_to_check:
                        FoodStalls.append({
                            "Canteen & Stall": stall_canteen + " - " + stall,
                            "Price": prices[stall_canteen][stall]
                        })
        FoodStalls.sort(key=myFunc)

        # To print results
        print("Food stalls found: " + str(len(FoodStalls)))
        if len(FoodStalls) == 0:
            print("No food stall found with input keyword.")
        else:
            for x in FoodStalls:
                print(x["Canteen & Stall"] + ", $" + str(x["Price"]))

# Location-based Search Function - to be implemented
def search_nearest_canteens(user_locations, k):

    # To assign coordinates to each user, A and B
    coordA = user_locations[0]
    coordB = user_locations[1]

    # To print error messages for invalid inputs of k
    try:
        int(float(k))
    except ValueError:
        k = input("Invalid input. Try again. ")
    while float(k).is_integer() == False:
            k = input("Invalid input. Try again. ")
    if int(float(k)) < 1:
        k = 1

    # To proceed if input is valid
    if int(float(k)) >= 1:
        FoodStalls = []

        def myFunc(sort):
            return sort["Distance Sum"]

        for canteen in canteen_locations:
            x = canteen_locations[canteen][0]
            y = canteen_locations[canteen][1]
            dA = math.sqrt((coordA[0] - x) ** 2 + (coordA[1] - y) ** 2)
            dB = math.sqrt((coordB[0] - x) ** 2 + (coordB[1] - y) ** 2)
            FoodStalls.append({
                "Canteen": canteen,
                "Distance Sum": dA + dB
            })
        FoodStalls.sort(key=myFunc)

        # To print results
        print("We found", int(float(k)), "canteens. From nearest to furthest:")
        for i in range(0,int(float(k))):
            print(FoodStalls[i]["Canteen"])


# Any additional function to assist search criteria

# Main Python Program Template
# dictionary data structures
canteen_stall_keywords = load_stall_keywords("canteens.xlsx")
canteen_stall_prices = load_stall_prices("canteens.xlsx")
canteen_locations = load_canteen_location("canteens.xlsx")


# main program template - provided
def main():
    loop = True

    while loop:
        print("=======================")
        print("F&B Recommendation Menu")
        print("1 -- Display Data")
        print("2 -- Keyword-based Search")
        print("3 -- Price-based Search")
        print("4 -- Location-based Search")
        print("5 -- Exit Program")
        print("=======================")
        option = int(input("Enter option [1-5]: "))

        if option == 1:
            # print provided dictionary data structures
            print("1 -- Display Data")
            print("Keyword Dictionary: ", canteen_stall_keywords)
            print("Price Dictionary: ", canteen_stall_prices)
            print("Location Dictionary: ", canteen_locations)
        elif option == 2:
            # keyword-based search
            print("Keyword-based Search")

            # call keyword-based search function
            keywords = load_stall_keywords()
            search_by_keyword(keywords)
        elif option == 3:
            # price-based search
            print("Price-based Search")

            # call price-based search function
            keywords = load_stall_keywords()
            search_by_price(keywords)
        elif option == 4:
            # location-based search
            print("Location-based Search")

            # call PyGame function to get two users' locations
            userA_location = get_user_location_interface()
            print("User A's location (x, y): ", userA_location)
            userB_location = get_user_location_interface()
            print("User B's location (x, y): ", userB_location)

            # call location-based search function
            user_locations = [userA_location, userB_location]
            k = input("How many canteens would you like to find? ")
            search_nearest_canteens(user_locations, k)
        elif option == 5:
            # exit the program
            print("Exiting F&B Recommendation")
            loop = False

main()
