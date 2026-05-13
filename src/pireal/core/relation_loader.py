from pireal.core.relation import Relation


def load_relations(data: dict) -> list[Relation]:
    """
    Convierte el dict parseado por sanitize_data en una lista de Relation.
    """
    relations = []
    for table in data.get("tables", []):
        relation = Relation()
        relation.name = table["name"]
        relation.header = table["header"]
        for row in table.get("tuples", []):
            relation.insert(row)
        relations.append(relation)
    return relations
