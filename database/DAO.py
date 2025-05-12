from database.DB_connect import DBConnect
from model.airport import Airport


class DAO:

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * from airports a order by a.AIRPORT asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(nMin, idMapAirports):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t.ID, t.IATA_CODE, count(*) as N
                    from (select a.ID, a.IATA_CODE, f.AIRLINE_ID, count(*)
		                    from airports a, flights f 
		                    where a.ID = f.ORIGIN_AIRPORT_ID or a.ID = f.DESTINATION_AIRPORT_ID 
                            group by a.ID, a.IATA_CODE, f.AIRLINE_ID) t
                    group by t.ID, t.IATA_CODE
                    having N >= %s
                    order by N asc"""

        cursor.execute(query, (nMin, ))

        for row in cursor:
            result.append(idMapAirports[row["ID"]])  # metto dentro il risultato gli Airports attraverso l'idMap

        cursor.close()
        conn.close()
        return result
