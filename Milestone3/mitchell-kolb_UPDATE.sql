
--SQL script file containing all UPDATE TABLE statements. Name this file “<your-name>_UPDATE.sql”

--Calculate and update the “numCheckins”, “reviewcount”, and “reviewrating” attributes for each business.
--“numCheckins” value for a business should be updated to the sum of all check-in counts for that business. Similarly, “reviewcount” should be updated to the number of reviews provided for that business (Note that you will overwrite the values extracted from the JSON data). “reviewrating” is the average of the review star ratings provided for each business. You should query the review table to calculate the number of reviews and avg review rating for each business. Similarly, you should query the check-in table to calculate the total number of check-ins. In grading, points will be deducted if you don’t update these values.





-- Update the numCheckins attribute for each business
UPDATE business AS businesstable
SET numCheckins = IFNULL((
    SELECT SUM(checkincount)
    FROM checkin AS checkintable
    WHERE checkintable.business_id = businesstable.business_id
), 0);

-- Update the reviewcount and reviewrating attributes for each business
UPDATE business AS businesstable
SET reviewcount = (
    SELECT COUNT(*)
    FROM review AS reviewtable
    WHERE reviewtable.business_id = businesstable.business_id
),
reviewrating = IFNULL((
    SELECT AVG(stars)
    FROM review AS reviewtable
    WHERE reviewtable.business_id = businesstable.business_id
), 0);
