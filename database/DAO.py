from database.DB_connect import DBConnect
from model.team import Team


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        res = []
        query = """select distinct t.`year` as years
                    from teams t 
                    where t.`year` > 1979
                    order by t.`year` desc """

        cursor.execute(query)

        for row in cursor:
            res.append(row['years'])

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getTeamsOfYear(year):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        res = []
        query = """select *
                    from teams t 
                    where t.`year` = %s """

        cursor.execute(query, (year,))

        for row in cursor:
            res.append(Team(**row))

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getSalaryofTeams(year, idMap):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        res = []
        query = """select t.teamCode, t.ID, sum(s.salary ) as totSalary
                from salaries s, appearances a , teams t 
                where s.`year` = t.`year` and t.`year` = a.`year` 
                and a.`year` = %s
                and t.ID = a.teamID 
                and s.playerID = a.playerID 
                group by t.teamCode """

        cursor.execute(query, (year,))

        results = {}
        for row in cursor:
            #res.append(idMap[row['ID']], idMap[row['totSalary']])
            results[idMap[row['ID']]] = row['totSalary']
        cursor.close()
        conn.close()
        return results
