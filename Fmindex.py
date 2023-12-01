class Fmindex:
    def __init__(self, bwt_list):
        self.bwt_list = bwt_list
        self.dict = self.create_dict()

    def create_dict(self):
        # Efficiently creating the dictionary by mapping characters to their first occurrence
        return {char: sorted(self.bwt_list).index(char) for char in set(self.bwt_list)}

    def match(self, pattern, wavelet_tree, bwt_len):
        s, e = 0, bwt_len
        for char in reversed(pattern):
            if char in self.dict:
                s = self.dict[char] + wavelet_tree.rank_query(char, s)
                e = self.dict[char] + wavelet_tree.rank_query(char, e)

                # If s exceeds e, pattern not found
                if s > e:
                    return 0
            else:
                # Character not in dictionary means pattern not found
                return 0

        return e - s

