from neo4j import GraphDatabase
import logging

from app.core.config import config
    
class Neo4jConnection:
    def __init__(self, uri, user, password):
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            self.driver.verify_connectivity()
            logging.info("Connection established successfully.")
        except Exception as e:
            logging.error(f"Connection failed: {e}")

    def close(self):
        if self.driver:
            self.driver.close()

    def query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record.data() for record in result]


# singleton connection (recommended)
neo4j_conn = Neo4jConnection(
    uri=config.NEO4J_URI,
    user=config.NEO4J_USER,
    password=config.NEO4J_PASSWORD
)