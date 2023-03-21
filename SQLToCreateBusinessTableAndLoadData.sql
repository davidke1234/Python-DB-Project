--copy Business (name,state,city) FROM 'D:\WSU\451 DB\Project\milestone1DB.csv' 
--DELIMITER ',' CSV

drop table Business

Create Table Business (
	business_id guid PK
	name varchar(50)
	address varchar(50)
	city  varchar(30)
	state char(2)
	postal_code varchar(20)
	latitude Decimal(12,9)
	longitude Decimal(12,9)
	stars Decimal(4,2)
	review_count int
	is_open bit
)

select * from business

BUSINESS - good
business_id guid PK
name varchar(50)
address varchar(50)
city  varchar(30)
state char(2)
postal_code varchar(20)
latitude Decimal(12,9)
longitude Decimal(12,9)
stars Decimal(4,2)
review_count int
is_open bit

CATEGORIES
Id int PK
business_id guid FK
categoryName varchar(20)

HOURS
Id int PK
business_id guid FK
day varchar(10)
startTime varchar(15) 
endTime varchar(15) 

ATTRIBUTES
Id int PK
business_id guid FK
attributeName varchar(40)
attributeValue varchar(20