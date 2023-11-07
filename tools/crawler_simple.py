from sys import argv
import requests
from bs4 import BeautifulSoup
import yaml


target = argv[1]
output_file = argv[2]


def crawl_target(start_url, output_file):
    response = requests.get(start_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    with open(output_file, 'a') as file:
        for link in soup.find_all('a', href=True):
            url = link['href']
            if url:  # Implement this method with whatever logic based on your needs. TODO: check url valid and in scope
                file.write(url + '\n')
                print("Logged URL:", url)
                # Here you can add recursion or queuing to follow the URL


if __name__ == '__main__':
    print("Crawling target:", target)
    print("Output file:", output_file)
    crawl_target(target, output_file)