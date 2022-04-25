import sys
import scraping_classes



google_driver = google_selenium_driver("scraping_papers_and_getting_db_data/temp/screenshot_error_file.png")
try:
    proxy = proxy_site_finder('libgen', google_driver.loaded_driver).verified_proxy_link
    study_example = Study('Stochasticity constrained by deterministic effects of diet and age drive rumen microbiome assembly dynamics')
    paper_finder_test = paper_finder(study_example.study_title, proxy, google_driver.loaded_driver)
   # study_test_2 = Study('Inoculation with rumen fluid in early life accelerates the rumen microbial development and favours the weaning process in goats')
   # paper_finder_test_2 = paper_finder(study_test_2.study_title, proxy, google_driver.loaded_driver)
except BaseException:
    google_driver.take_screenshot()