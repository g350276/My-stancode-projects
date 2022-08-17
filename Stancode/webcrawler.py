"""
File: webcrawler.py
Name: Marinda
--------------------------
This file collects more data from
https://www.ssa.gov/oact/babynames/decades/names2010s.html
https://www.ssa.gov/oact/babynames/decades/names2000s.html
https://www.ssa.gov/oact/babynames/decades/names1990s.html
Please print the number of top200 male and female on Console
You should see:
---------------------------
2010s
Male Number: 10890537
Female Number: 7939153
---------------------------
2000s
Male Number: 12975692
Female Number: 9207577
---------------------------
1990s
Male Number: 14145431
Female Number: 10644002
"""

import requests
from bs4 import BeautifulSoup


def main():
    """
    To sum up male and female numbers from websites of "200 Top names" of each years and print.
    """
    for year in ['2010s', '2000s', '1990s']:
        print('---------------------------')
        print(year)
        url = 'https://www.ssa.gov/oact/babynames/decades/names'+year+'.html'

        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, features="html.parser")

        # ----- Write your code below this line ----- #
        male_num = 0
        female_num = 0
        tags = soup.find_all('table', {'class': 't-stripe'})

        for tag in tags:
            line = tag.tbody.text  # 取 <tbody> 中間的文字
            s = line.split()

            # Male number
            for i in range(2, 1000, 5):
                remove_comma1 = s[i].split(',')
                remove_comma2 = ''.join(remove_comma1)
                male_num += int(remove_comma2)

            # Female number
            for i in range(4, 1000, 5):
                remove_comma1 = s[i].split(',')
                remove_comma2 = ''.join(remove_comma1)
                female_num += int(remove_comma2)

        print(f"Male Number: {male_num}")
        print(f"Female Number: {female_num}")


if __name__ == '__main__':
    main()
