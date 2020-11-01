from linkedinscraper import spreadsheet
import time
from linkedinscraper.scraper import LinkedInScraper
from linkedinscraper.spreadsheet import Spreadsheet

def main():
    user = input('Please enter your Linkedin username\n\t ==>').strip()
    passw = input('Please enter your Linkedin password\n\t ==>').strip()
    school = input('Please enter the name of the school you would like to search\n(Example: Yale University)\n\t ==>').strip()
    query = input('Please enter the attribute of the alumni that you are looking for\n\t ==>').strip()
    driver_path = input('Please enter the file path of your browser driver\n\t ==>').strip()
    excel_file_path = input('Please enter the desired path for your output spreadsheet\n\t ==>').strip()
    before = time.time()
    scraper = LinkedInScraper(user,passw,query,school,driver_path)
    scraper.gotoschool()
    scraper.search_people()
    scraper.get_names_and_urls()
    scraper.add_additional_info
    spreadsheet = Spreadsheet(excel_file_path)
    spreadsheet.fill_from_people(scraper.people)
    spreadsheet.save()
    

    after = time.time()
    runtime = after - before
    print('Number of Profiles assessed => ',)
    print('Program Runtime => ',runtime,' seconds.')

if __name__ == "__main__":
    main()