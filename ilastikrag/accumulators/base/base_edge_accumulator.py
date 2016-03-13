class BaseEdgeAccumulator(object):
    """
    Base class for all edge accumulators,
    i.e. accumulators that compute features from the edge values
    between superpixels (not superpixel contents).
    """

    #: Accumulator type
    ACCUMULATOR_TYPE = 'edge'

    #: An id string for this accumulator.
    #: Must not contain an underscore (``_``).
    #: Must not conflict with any other accumulators of the same type ('edge').
    #: All feature names supported by this accumulator must begin with the prefix ``<id>_edge_``
    ACCUMULATOR_ID = ''

    def __init__(self, rag, feature_names):
        """
        Parameters
        ----------
        rag:
            The rag.
        
        feature_names
            A list of feature names to compute with this accumulator.
        """
        pass
    
    def cleanup(self):
        """
        Called by the Rag to indicate that processing has completed, and
        the accumulator should discard all cached data and intermediate results.
        Subclasses must reimplement this function.
        """
        raise NotImplementedError

    @classmethod
    def supported_features(cls, rag):
        """
        Returns the list of feature names that can be computed for the given Rag.
        """
        raise NotImplementedError

    def ingest_edges_for_block(self, dense_edge_tables, block_start, block_stop):
        """
        Ingests the edge data from a particular block of labels in the Rag.

        Parameters
        ----------
        dense_edge_tables
            *list* of *pandas.DataFrame* objects, one per image axis.          |br|
            Contains only the edges contained within block_start, block_stop.  |br|
            Each DataFrame has the same columns as ``Rag.dense_edge_tables``,     |br|
            plus an extra column for ``edge_value``                            |br|
        
        block_start
            The location of the block within the Rag's full label volume.
        
        block_stop
            The end of the block within the Rag's full label volume.
        """
        raise NotImplementedError
    
    def append_merged_edge_features_to_df(self, edge_df):
        """
        Called by the Rag after all blocks have been ingested.

        Merges the features of all ingested blocks into a final set of edge
        feature columns, and appends those columns to the given
        ``pandas.DataFrame`` object.
        """        
        raise NotImplementedError
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.cleanup()
