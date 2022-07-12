# Libarry for Render Llamafax Service.
import logging

LlamaCorpus = {"NN": "llama", "NNS": "llamas"}


def render(Message: dict, Scope: list) -> list:
    """Intakes Message dictionary.
    \nOutputs list of generated statments.
    \nUses Unix time + randomizer to seed randomization.
    """

    def inScope(Chunk=Message["chunk"], Scope=Scope) -> list:
        out = []
        for chunk in Chunk:
            if isinstance(chunk, list):
                for cTup in chunk:
                    if isinstance(cTup, list):
                        word, SoP = cTup
                        if SoP in Scope:
                            out.append(cTup)
        return out

    def processCorp(Corpus: dict = LlamaCorpus) -> list:
        return [(PoS, Word) for PoS, Word in Corpus.items()]

    def generator(
        POSScope=inScope(), Scope=Scope, Base: str = Message["raw"], Corpus=LlamaCorpus
    ):
        # For each POS found parsed from chunks EX ['state', 'NN'] each
        out = []
        logging.info("Generating Statments")
        for PoSTup in POSScope:
            # Splits Pared chunk 2 variables (state) (NN)
            chkWord, chkPoS = tuple(PoSTup)
            # Loops for each PoS in scope (NN) (NNS)
            [
                out.append(
                    Base.replace(
                        chkWord,
                        [word for sop, word in processCorp() if sop == chkPoS][0],
                        1,
                    )
                )
                for scpPoS in Scope
                if scpPoS == chkPoS
            ]
        return out

    return generator()
