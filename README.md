# scrap-pp-journals

To scrape a pile of papers in the format of ***.xml*** (For the purpose of building a corpus.), An easy way to do it is to download them in the format of ***PDF*** first, and then transform them into ***.xml***.

A good transform tool widely used is https://github.com/CeON/CERMINE
terminal after cd run: java -cp cermine-impl-1.12-jar-with-dependencies.jar pl.edu.icm.cermine.ContentExtractor -path /Users/Felicia/1

## Scrape meta and xml from a DB:
***scrap_meta&xml.py*** works as a scraper for meta data and xml url for papers. Result will be stored in several files each contains paper name, meta_data and xml_url
