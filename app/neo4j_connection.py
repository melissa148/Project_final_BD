from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def execute_query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            # Extraer todos los datos ANTES de consumir el resultado
            records = [record.data() for record in result]
            result.consume()  # Solo consume después de extraer los registros
            return records
