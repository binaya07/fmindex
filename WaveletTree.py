from Node import Node

class WaveletTree:
    def __init__(self, data, block_size=None):
        if data is None:
            raise ValueError("Wavelet tree initialization error: 'data' parameter cannot be None")
        self.__root = Node(data, None, block_size)  # Create the parent node

    def rank_query(self, character, position):
        if character is None or position is None:
            raise ValueError(f"Rank query error: 'character' and 'position' cannot be None (character: {character}, position: {position})")
        if position < 0:
            raise ValueError(f"Rank query error: 'position' cannot be negative (position: {position})")
        return self.__root.get_rank_query(position, character)

