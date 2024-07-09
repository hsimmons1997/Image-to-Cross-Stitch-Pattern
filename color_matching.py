import csv
import math

class DMC_Matching:
    def __init__(self):
        self.dmc = {}
        with open('dmc_color_codes.csv', mode = 'r') as infile:
            reader = csv.reader(infile, delimiter=',')
            next(reader, None)
            for rows in reader:
                try:
                    self.dmc = {rows[0]: [int(rows[2]), int(rows[3]), int(rows[4]), rows[1], rows[0]] for rows in reader}
                except ValueError:
                    print(f"Skipping invalid row: {rows}")
                    continue

    def get_color_code(self, color):
        '''
        Retrieve the floss code for the closest color
        :Param color: color to identify
        :Return closest color match to the desired color based on euclidean distance
        '''
        temp = 99999999
        code = ''
        # For each key in the dictionary
        for key in self.dmc:
            # Calculate euclidean distance
            distance = self.euclidean_distance(self.dmc[key], color)
            # If new color is closer than temp, update temp
            if distance < temp:
                code = key
                temp = distance
        return self.dmc[code]

    def get_dmc_rgb_triple(self, color):
        '''
        Retrieve RGB triple for a given color code
        :Param color: Color to get RGB code for
        :Return RGB triple
        '''
        dmc_item = self.get_color_code(color)
        return (dmc_item[0], dmc_item[1], dmc_item[2])

    def euclidean_distance(self, color1, color2):
        '''
        Calculating distance between colors
        :Param color1:
        :Param color2:
        :Return:
        '''
        (r1, g1, b1, name, code) = color1
        (r2, g2, b2) = color2
        distance = math.sqrt(2 * ((r1-r2)**2) + 4*((g1-g2)**2) + 3*((b1-b2)**2))
        return distance

    




















