from neo4j import GraphDatabase

class Neo4jConnection:

    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)

    def close(self):
        if self.__driver is not None:
            self.__driver.close()

    def query(self, query, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.__driver.session(database=db) if db is not None else self.__driver.session()
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response
    
# neo4j address : http://147.47.200.145:37474/
dbname = "teamdb10"
uri_param = "bolt://147.47.200.145:37687"
user_param = "team10"
pwd_param = "wannagohome10"

def response_query(cypher):
    # Neo4j 연결
    conn = Neo4jConnection(uri=uri_param, user=user_param, pwd=pwd_param)

    # Cypher 쿼리 입력
    # cypher = 'MATCH (n) return n'

    # Cypher 쿼리 실행 후 결과를 response에 저장
    response = conn.query(cypher, db=dbname)
    # 연결 종료 필수!
    conn.close()
    return response