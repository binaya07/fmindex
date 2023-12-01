import time

def create_burrows_wheeler_transform(input_text):
    start_time = time.time()
    suffix_array = create_suffix_array(input_text)
    bwt_result = ""
    for index in suffix_array:
        bwt_result += input_text[index - 1]
    end_time = time.time()
    execution_time = end_time - start_time
    print("Time taken to create BWT: ", execution_time)
    return bwt_result, execution_time

def create_s12(text):
    # Initialize s1 and s2 using list comprehensions for efficiency
    s1 = [idx for idx in range(len(text)) if idx % 3 == 1]
    s2 = [idx for idx in range(len(text)) if idx % 3 == 2]
    # Return the concatenated list of s1 and s2
    return s1 + s2

def get_triplet(text, idx):
    triplet = []
    for text_idx in range(idx, min(idx + 3, len(text))):
        triplet.append(text[text_idx])
    while len(triplet) < 3 and isinstance(triplet, str):
        triplet.append("$")
    return triplet

def create_inverse_sa(len_text, sa):
    # Initialize the inverse suffix array with -1s
    inverse_sa = [-1] * len_text
    # Populate the inverse suffix array using the suffix array indices
    for idx, value in enumerate(sa):
        inverse_sa[value] = idx
    return inverse_sa

def create_s0(text, s12):
    # Create the s0 unsorted list by selecting indices where (index - 1) % 3 == 0
    s0_unsorted = [idx - 1 for idx in s12 if (idx - 1) % 3 == 0]
    # Handle special case when text length % 3 == 1
    if len(text) % 3 == 1:
        s0_unsorted.insert(0, len(text) - 1)
    # Sort s0 using bucketsort, but only by the first letter
    s0_with_ranks = bucketsort(text, s0_unsorted, s0=True)
    # Extract the sorted indices from s0_with_ranks
    s0 = [x[1] for x in sorted(s0_with_ranks, key=lambda x: x[0])]
    return s0

def create_suffix_array(text):
    # Construct and sort s12 suffixes
    s12_unsorted = create_s12(text)
    s12_with_ranks = bucketsort(text, s12_unsorted)
    s12_ranks = [rank for rank, _ in s12_with_ranks]

    # Check if all ranks are unique
    if len(set(s12_ranks)) == len(s12_ranks):
        # If unique, simply sort s12 by ranks
        s12 = [suffix for _, suffix in sorted(s12_with_ranks, key=lambda x: x[0])]
    else:
        # If not unique, recursively create a suffix array for s12_ranks
        sa_s12 = create_suffix_array(s12_ranks)
        # Map back to original indices
        s12 = [s12_with_ranks[idx][1] for idx in sa_s12]

    # Sort s0 suffixes
    s0 = create_s0(text, s12)

    # Create inverse suffix array for s12
    inverse_sa_s12 = create_inverse_sa(len(text), s12)

    # Merge s0 and s12 suffix arrays
    merged_sa = merge_sa(text, s0, s12, inverse_sa_s12)

    return merged_sa

def bucketsort(current_text, sa, s0=False):
    # Determine the starting index for sorting (triplet index)
    triplet_idx = 0 if s0 else 2

    # Initialize sorted_sa with the input suffix array
    sorted_sa = sa

    # Sort the sa using bucket sort for each character in the triplet
    for i in range(triplet_idx, -1, -1):
        buckets = {}
        for text_idx in sorted_sa:
            triplet = get_triplet(current_text, text_idx)
            char_to_sort = triplet[min(i, len(triplet) - 1)]
            buckets.setdefault(char_to_sort, []).append(text_idx)

        sorted_sa = [idx for key in sorted(buckets.keys()) for idx in buckets[key]]

    # Compute the ranks for each triplet in the sorted suffix array
    ranks = {}
    rank = 1
    for text_idx in sorted_sa:
        triplet_str = ''.join(map(str, get_triplet(current_text, text_idx)))
        if triplet_str not in ranks:
            ranks[triplet_str] = rank
            rank += 1

    # Combine suffix array indices with their ranks
    s12_with_ranks = [(ranks[''.join(map(str, get_triplet(current_text, idx)))], idx) for idx in sa]

    return s12_with_ranks

def merge_sa(text, s0, s12, inverse_sa):
    sa = []
    idx_s0, idx_s12 = 0, 0
    len_text = len(text)

    while idx_s0 < len(s0) and idx_s12 < len(s12):
        current_s0, current_s12 = s0[idx_s0], s12[idx_s12]

        # Direct comparison or comparison using inverse_sa
        if text[current_s0:current_s0 + 2] != text[current_s12:current_s12 + 2]:
            # Choose the smaller character or use inverse_sa for tie-breaker
            if text[current_s0:current_s0 + 2] < text[current_s12:current_s12 + 2]:
                sa.append(current_s0)
                idx_s0 += 1
            else:
                sa.append(current_s12)
                idx_s12 += 1
        else:
            # Use inverse_sa for comparison
            if inverse_sa[current_s0] < inverse_sa[current_s12]:
                sa.append(current_s0)
                idx_s0 += 1
            else:
                sa.append(current_s12)
                idx_s12 += 1

    # Append remaining elements
    sa.extend(s0[idx_s0:] if idx_s0 < len(s0) else s12[idx_s12:])

    return sa