# fmindex
Creating an FM-index (Ferragina and Manzini) based on Burrows-Wheeler Transform (BWT) of the text.

Step 1. Given a text T, constructs it suffix array SA using DC3 algorithm of Karkainnen and Sanders. This should be O(n).

Step 2. From the suffix array, creates Burrows-Wheeler Transform (BWT).

Step 3. Constructs a wavelet tree over the BWT. 

Step 4. Creates a query algorithm for the wavelet tree - which in turn uses query algorithm for bit-vector.

Step 5. Uses the wavelet tree to implement 'backward' pattern matching using FM-index.
