import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
import anndata as ad


# -------------------------------------------------------------------------------
# Some test data
# -------------------------------------------------------------------------------

X_list = [    # data matrix of shape n_obs x n_vars
    [1, 0], [3, 0], [5, 6]]

obs_dict = {  # annotation of observations / rows
    'row_names': ['name1', 'name2', 'name3'],  # row annotation
    'oanno1': ['cat1', 'cat2', 'cat2'],        # categorical annotation
    'oanno2': ['o1', 'o2', 'o3'],              # string annotation
    'oanno3': [2.1, 2.2, 2.3]}                 # float annotation

var_dict = {  # annotation of variables / columns
    'vanno1': [3.1, 3.2]}

uns_dict = {  # unstructured annotation
    'oanno1_colors': ['#000000', '#FFFFFF'],
    'uns2': ['some annotation']}


# -------------------------------------------------------------------------------
# The test functions
# -------------------------------------------------------------------------------


def test_readwrite_dynamic():
    for typ in [np.array, csr_matrix]:
        X = typ(X_list)
        adata = ad.AnnData(X, obs=obs_dict, var=var_dict, uns=uns_dict)
        adata.filename = './test.h5ad'
        adata.write()
        adata = ad.read('./test.h5ad')
        assert pd.api.types.is_categorical(adata.obs['oanno1'])
        assert pd.api.types.is_string_dtype(adata.obs['oanno2'])
        assert adata.obs.index.tolist() == ['name1', 'name2', 'name3']
        assert adata.obs['oanno1'].cat.categories.tolist() == ['cat1', 'cat2']


def test_readwrite_h5ad():
    for typ in [np.array, csr_matrix]:
        X = typ(X_list)
        adata = ad.AnnData(X, obs=obs_dict, var=var_dict, uns=uns_dict)
        assert pd.api.types.is_string_dtype(adata.obs['oanno1'])
        adata.write('./test.h5ad')
        adata = ad.read('./test.h5ad')
        assert pd.api.types.is_categorical(adata.obs['oanno1'])
        assert pd.api.types.is_string_dtype(adata.obs['oanno2'])
        assert adata.obs.index.tolist() == ['name1', 'name2', 'name3']
        assert adata.obs['oanno1'].cat.categories.tolist() == ['cat1', 'cat2']


def test_readwrite_loom():
    for typ in [np.array, csr_matrix]:
        X = typ(X_list)
        adata = ad.AnnData(X, obs=obs_dict, var=var_dict, uns=uns_dict)
        adata.write_loom('./test.loom')
        adata = ad.read_loom('./test.loom')
        if isinstance(X, np.ndarray):
            assert np.allclose(adata.X, X)
        else:
            # TODO: this should not be necessary
            assert np.allclose(adata.X, X.toarray())


def test_write_csv():
    for typ in [np.array, csr_matrix]:
        X = typ(X_list)
        adata = ad.AnnData(X, obs=obs_dict, var=var_dict, uns=uns_dict)
        adata.write_csvs('./test_csv_dir')
