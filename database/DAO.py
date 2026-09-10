from database.DB_connect import DBConnect
from model.Constructor import Constructor


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = ("SELECT distinct year "
                 "FROM seasons s  "
                 "ORDER BY year")

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllConstructors(yearsDa, yearsA):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT DISTINCT c.constructorId AS constructorId, 
                            c.constructorRef AS constructorRef, 
                            c.name AS name,
                            c.nationality AS nationality,
                            MIN(d.dob) AS oldest_driver_dob
            FROM constructors c, results rs, races rc, drivers d
            WHERE c.constructorId = rs.constructorId 
                AND rs.position IS NOT NULL 
                AND rs.raceId = rc.raceId 
                AND d.driverId = rs.driverId
                AND rc.year BETWEEN %s AND %s
            GROUP BY c.constructorId
        """

        cursor.execute(query,(yearsDa, yearsA))
        for row in cursor:
            results.append(Constructor(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getConstructionsDriversPairs(yearDa, yearA):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT p1.constructorId AS id1, p2.constructorId AS id2, COUNT(DISTINCT p1.driverId) AS weight
                FROM (SELECT DISTINCT rc.raceId AS raceId, rs.constructorId AS constructorId, rs.driverId AS driverId
                      FROM results rs,races rc
                      WHERE rs.position IS NOT NULL 
                        AND rs.raceId = rc.raceId
                        AND rc.year BETWEEN %s AND %s) p1,
                     (SELECT DISTINCT rc.raceId AS raceId, rs.constructorId AS constructorId, rs.driverId AS driverId
                      FROM results rs, races rc
                      WHERE rs.position IS NOT NULL
                        AND rs.raceId = rc.raceId
                        AND rc.year BETWEEN %s AND %s) p2
                WHERE p1.driverId = p2.driverId
                  AND p1.raceId <> p2.raceId
                  AND p1.constructorId < p2.constructorId
                GROUP BY p1.constructorId, p2.constructorId
                """

        cursor.execute(query, (yearDa, yearA, yearDa, yearA))
        for row in cursor:
            results.append((row["id1"], row["id2"], row["weight"]))
        cursor.close()
        conn.close()
        return results





