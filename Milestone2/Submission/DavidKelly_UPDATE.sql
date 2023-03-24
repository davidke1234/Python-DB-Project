
------ Update numCheckins ------
update business 
set numcheckins = subquery.sumCheckins
from	
	(select businessId, sum(checkincount) as sumCheckins from businessCheckin
	group by businessId) as subquery
where business.businessId = subquery.businessId;

------ Update reviewCount ------
update business 
set reviewCount = subquery.reviewCount
from	
	(select businessId, count(*) as reviewCount from businessReview
	group by businessId) as subquery
where business.businessId = subquery.businessId;

------ Update reviewRating ------
update business 
set reviewRating = subquery.avgStars
from	
	(select br.businessId, avg(r.stars) as avgStars from businessReview br
	join review r on r.reviewId = br.reviewId
	group by br.businessId) as subquery
where business.businessId = subquery.businessId;

