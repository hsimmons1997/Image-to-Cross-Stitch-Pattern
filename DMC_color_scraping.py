from bs4 import BeautifulSoup
import requests
import code

colors = []

class colorizer:
    END = '\033[0m'
    GREEN = '\033[92m'

'''Run the scraper adn write the CSV we want'''

def main():
    scrape_colors()
    write_csv()
    print(colorizer.GREEN + 'All done!\r\n' + colorizer.END)

'''Fills out the colors by scraping them from https://threadcolors.com/ '''

def scrape_colors():
    global colors
    url_to_scrape = 'https://threadcolors.com/'
    print('r\n\Requesting page...')
    response = requests.get(url_to_scrape)
    print('Parsing HTML')
    root_parse_tree = BeautifulSoup(response.text, 'lxml')
    print('Finding color table')
    table = root_parse_tree.find('table', id = 'closest-colors')
    
    if table:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 7:  # Ensure enough cells are present
                floss_id = cells[1].get_text().strip()
                floss_name = cells[2].find('a').get_text().strip()  # Extracting text from <a> tag
                r_value = cells[3].get_text().strip()
                g_value = cells[4].get_text().strip()
                b_value = cells[5].get_text().strip()
                hex_code = cells[6].get_text().strip()
                color = (floss_id, floss_name, r_value, g_value, b_value, hex_code)
                colors.append(color)
            else:
                print(f"Skipping row due to insufficient data: {row}")
    else:
        print("Color table not found.")

def write_csv():
    print('\nOpening CSV file...')
    with open('dmc_color_codes.csv', 'w') as file_handle:
        print('Writing CSV file...')
        file_handle.write('floss_id, color_name, r_value, g_value, b_value, hex_code\r\n')
        for color in colors:
            file_handle.write(f"{color[0]}, {color[1]}, {color[2]}, {color[3]}, {color[4]}, {color[5]}\r\n")
    print('CSV file write completed.')

if __name__ == '__main__':
    main()
