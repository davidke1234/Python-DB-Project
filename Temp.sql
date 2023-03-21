SELECT "Name", "State", "City"
	FROM public."Business";
	
	SELECT "Name","City" FROM public."Business" WHERE "Name" LIKE '%P%' ORDER BY "Name"
	

	
	SELECT "City" FROM Public."Business" WHERE "Name" = 'Zander''s Capitol Grill'
	
	SELECT "City" FROM Public."Business" WHERE "Name" like 'Hoppin
	
	SELECT "Name" FROM Public."Business" WHERE "Name" LIKE 'Applebee''s Bar & Grill' ORDER BY "Name"
	
	Create Table xBusiness (
	Name varchar(250),
	State varchar(30),
	City varchar(150)
)
go