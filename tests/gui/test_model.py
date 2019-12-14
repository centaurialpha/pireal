import random
import string

from pireal.core.relation import Relation
from pireal.gui.model_view_delegate import RelationModel


def test_model(qtmodeltester):
    relation = Relation()
    relation.header = ['header_1', 'header_2']
    for _ in range(100):
        name = ''.join([random.choice(string.ascii_letters) for _ in range((3))])
        number = ''.join([random.choice([str(i) for i in range(10)]) for _ in range(3)])
        relation.content.add((number, name))
    model = RelationModel(relation)
    model.editable = False
    qtmodeltester.check(model, force_py=True)
