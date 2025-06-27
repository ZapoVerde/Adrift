# test_technique_mutation_utils.py

from Adrift.utils.technique_mutation_utils import generate_evolution_offer, apply_mutation


def test_apply_mutation_replace_effect():
    base = {"skill": "melee", "effects": ["push"], "modifier": None}
    offers = generate_evolution_offer(base)
    selected = [o for o in offers if o["type"] == "replace_effect"]
    if selected:
        result = apply_mutation(base, selected[0])
        assert result != base
        assert "push" not in result["effects"]
