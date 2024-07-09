'''Code based on https://github.com/PaulMakesStuff/Python_Cross_Stitch/tree/master
Defining a class to generate scalable vector graphics (SVG) elements for the cross-stitch patterns'''

class SVG:
    def __init__(self, black_white = False, minor_lines = False, symbols = True):
        self.black_white = black_white
        self.minor_lines = minor_lines
        self.symbols = symbols
        self.xml = ''

    def get_rgb(self, color):
        return f'rgb({color[0]},{color[1]},{color[2]})'
    
    def get_rgb_from_dmc_item(self, item):
        return 'rgb('+str(item[0])+','+str(item[1])+','+str(item[2])+');'

    def gen_glyph(self, num, x, y, scale=1):
        glyphs = {
            0: "M4 4L16 16",
            1: "M4 16L16 4M4 10L 16 10",
            2: "M7 7L7 13 13 13 13 7Z' fill = 'black",
            3: "M4 4L10 16L16 4 Z",
            4: "M4 4L16 16M4 16 L16 4",
            5: "M4 4L4 16 16 16 16 4Z",
            6: "M4 4L10 16L16 4 Z' fill = 'black",
            7: "M10 4L6 10 10 16 14 10Z' fill = 'black",
            8: "M8 8L8 12 12 12 12 8Z",
            9: "M4 4L16 16M4 16 L16 4M10 4L10 16M4 10L16 10",
            10: "M4 4L4 16 16 16 16 4Z' fill = 'black"
        }
        path = glyphs.get(num, '')
        return f"<path class='glyph' d='{path}' transform='translate({x} {y}) scale({scale})'/>" if path else ''

    def add_rect(self, palette, index, x, y, size):
        glyph_scale = size / 20.0
        fill = 'fill:rgb(255,255,255);' if self.black_white else 'fill:'+self.get_rgb_from_dmc_item(palette[index])
        stroke = 'stroke:rgb(20,20,20);stroke-width:1;' if self.minor_lines else 'stroke:none;'
        sym = self.gen_glyph(index, x, y, glyph_scale) if self.symbols else ''
        self.xml += '<rect x="'+str(x)+'" y="'+str(y)+'" width="'+str(size)+'" height="'+str(size)+'" style="'+fill+stroke+'"/>' + sym

    def prep_for_drawing(self, width, height):
        self.xml += f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" style="fill:none;">'
        self.xml += '<style>.svg_txt{font-size:20px;}.glyph{stroke:#000000;stroke-width:1;stroke:1;}</style>'

    def mid_arrows(self, size, width, height):
        h = str(size/2)
        f = str(size)
        self.xml += "<path d=\"M0 "+h+"L"+f+" "+h+"M"+h+" 0L"+f+" "+h+" "+h+" "+f+"\" stroke=\"black\" stroke-width=\"2\" fill=\"none\" transform='translate(0 " + str(height/2) + ")'/>"
        self.xml += "<path d=\"M"+h+" 0L"+h+" "+f+" M"+f+" "+h+"L"+h+" "+f+" 0 "+h+"\" stroke=\"black\" stroke-width=\"2\" fill=\"none\" transform='translate(" + str(width/2) + " 0)'/>"
    
    def major_gridlines(self, size, width, height):
        for x in range(size + size * 10, width, size * 10):
            self.xml += "<line x1=\"" + str(x) + "\" y1=\"" + str(size) + "\" x2=\"" + str(x) + "\" y2=\"" + str(height) + "\" style=\"stroke:black;stroke-width:2\" />"
        for y in range(size + size * 10, height, size * 10):
            self.xml += "<line x1=\"" + str(size) + "\" y1=\"" + str(y) + "\" x2=\"" + str(width) + "\" y2=\"" + str(y) + "\" style=\"stroke:black;stroke-width:2\" />"
            
    def add_key_color(self, x, y, size, index, colour):
        # key
        glyph_scale = size / 20.0
        fill = 'fill:rgb(255,255,255);' if self.black_white else 'fill:rgb('+str(colour[0])+', '+str(colour[1])+', '+str(colour[2])+');'
        stroke = 'stroke:rgb(20,20,20);stroke-width:1;' if self.minor_lines else 'stroke:none;'
        sym = self.gen_glyph(index, x, y, glyph_scale) if self.symbols else ''
        self.xml += '<rect x="0" y="'+str(y)+'" width="'+str(size)+'" height="'+str(size)+'" style="'+fill+stroke+'"/>' + sym
        # color name
        self.xml += '<rect x="'+str(size)+'" y="'+str(y)+'" width="'+str(size* 10)+'" height="'+str(size)+'" style="fill:rgb(255,255,255);stroke:black;stroke-width:1;"/>'
        self.xml += '<text x = "' + str(x + size * 1.5) + '" y = "' + str(y + size / 2.0) + '" fill="black">' + colour[3] + '</text>'
        # color code
        self.xml += '<rect x="'+str(size*11)+'" y="'+str(y)+'" width="'+str(size* 2)+'" height="'+str(size)+'" style="fill:rgb(255,255,255);stroke:black;stroke-width:1;"/>'
        self.xml += '<text x = "' + str(size* 11 + (size/2.0)) + '" y = "' + str(y + size / 2.0) + '" fill="black">' + colour[4] + '</text>'

    def save(self, filename):
        self.xml += '</svg>'
        with open(filename, 'w') as f:
            f.write(self.xml)

'''
    def add_key_colour(self, x, y, size, index, color):
        glyph_scale = size / 20.0
        fill = f'fill:rgb(255,255,255);' if self.black_white else f'fill:{self.get_rgb(color)}'
        stroke = 'stroke:rgb(20,20,20);stroke-width:1;' if self.minor_lines else 'stroke:none;'
        sym = self.gen_glyph(index, x, y, glyph_scale) if self.symbols else ''

        # Key colour rectangle
        self.xml += f'<rect x="0" y="{y}" width="{size}" height="{size}" style="{fill}{stroke}"/>{sym}'
        
        # Colour name
        self.xml += f'<rect x="{size}" y="{y}" width="{size*10}" height="{size}" style="fill:rgb(255,255,255);stroke:black;stroke-width:1;"/>'
        self.xml += f'<text x="{x + size * 1.5}" y="{y + size / 2}" fill="black">{color[3]}</text>'
        
        # Colour code
        self.xml += f'<rect x="{size*11}" y="{y}" width="{size*2}" height="{size}" style="fill:rgb(255,255,255);stroke:black;stroke-width:1;"/>'
        self.xml += f'<text x="{size*11 + size / 2}" y="{y + size / 2}" fill="black">{color[4]}</text>'
'''