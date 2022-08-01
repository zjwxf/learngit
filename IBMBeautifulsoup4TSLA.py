from bs4 import BeautifulSoup
import pandas as pd
import requests
import xml
import matplotlib 
import plotly
url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
data  = requests.get(url).text
soup = BeautifulSoup(data, 'html5lib') #html5lib
tesla_data = pd.DataFrame(columns=["Date", "Revenue"])
# First we isolate the body of the table which contains all the information
# Then we loop through each row and find all the column values for each row
for row in soup.find("tbody").find_all('tr'):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text
    tesla_data = tesla_data.append({"Date":date,  "Revenue":revenue}, ignore_index=True)    
print(soup.find_all('title'))
print(tesla_data.tail())
make_graph()

url = "https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue"
data  = requests.get(url).text
soup = BeautifulSoup(data, 'html.parser') #html.parser
gme_data = pd.DataFrame(columns=["Date", "Revenue"])
# First we isolate the body of the table which contains all the information
# Then we loop through each row and find all the column values for each row
for row in soup.find("tbody").find_all('tr'):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text
    gme_data = gme_data.append({"Date":date,  "Revenue":revenue}, ignore_index=True)    
print(soup.find_all('title'))
print(gme_data.tail())





CREATE TABLE PETSALE (
    ID INTEGER NOT NULL,
    PET CHAR(20),
    SALEPRICE DECIMAL(6,2),
    PROFIT DECIMAL(6,2),
    SALEDATE DATE
    );
    
CREATE TABLE PET (
    ID INTEGER NOT NULL,
    ANIMAL VARCHAR(20),
    QUANTITY INTEGER
    );
    
INSERT INTO PETSALE VALUES
(1,'Cat',450.09,100.47,'2018-05-29'),
(2,'Dog',666.66,150.76,'2018-06-01'),
(3,'Parrot',50.00,8.9,'2018-06-04'),
(4,'Hamster',60.60,12,'2018-06-11'),
(5,'Goldfish',48.48,3.5,'2018-06-14');
    
INSERT INTO PET VALUES
    (1,'Cat',3),
    (2,'Dog',4),
    (3,'Hamster',2);
    
SELECT * FROM PETSALE;
SELECT * FROM PET;

ALTER TABLE PETSALE
ADD COLUMN QUANTITY INTEGER;

SELECT * FROM PETSALE;

UPDATE PETSALE SET QUANTITY = 9 WHERE ID = 1;
UPDATE PETSALE SET QUANTITY = 3 WHERE ID = 2;
UPDATE PETSALE SET QUANTITY = 2 WHERE ID = 3;
UPDATE PETSALE SET QUANTITY = 6 WHERE ID = 4;
UPDATE PETSALE SET QUANTITY = 24 WHERE ID = 5;

SELECT * FROM PETSALE;


ALTER TABLE PETSALE
DROP COLUMN PROFIT;

SELECT * FROM PETSALE;
ALTER TABLE PETSALE
ALTER COLUMN PET SET DATA TYPE VARCHAR(20);

SELECT * FROM PETSALE;

ALTER TABLE PETSALE
ALTER COLUMN PET SET DATA TYPE VARCHAR(20);

SELECT * FROM PETSALE;