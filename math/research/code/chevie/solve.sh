#python3 py/extract_icc_labels.py
#python3 py/find_permutations.py
#python3 py/csv_families.py
#python3 py/csv_icc.py
#python3 py/csv_invert.py icc

python3 py/permute_vectors.py all
python3 py/csv_multiply.py icc all
python3 py/test_solved.py all

#python3 py/permute_vectors.py defectless
#python3 py/csv_multiply.py icc defectless
#python3 py/test_solved.py defectless

python3 py/permute_vectors.py ratlsmooth
python3 py/csv_multiply.py icc ratlsmooth
python3 py/test_solved.py ratlsmooth

#python3 py/permute_vectors.py min
#python3 py/csv_multiply.py icc min
#python3 py/test_solved.py min

# extra

#python3 py/csv_permute.py exotic
#python3 py/csv_invert.py exotic

#python3 py/find_duplicates.py # only does mode 'all'

