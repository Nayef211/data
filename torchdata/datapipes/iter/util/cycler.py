# Copyright (c) Facebook, Inc. and its affiliates.
from torch.utils.data import IterDataPipe, functional_datapipe
from typing import Optional


@functional_datapipe("cycle")
class CyclerIterDataPipe(IterDataPipe):
    """
    Cycle the specified input in perpetuity (by default), or for the specified number of times.

    Args:
        source_datapipe: source DataPipe that will be cycled through
        count: the number of times to read through the source DataPipe (if `None`, it will cycle in perpetuity)
    """

    def __init__(self, source_datapipe: IterDataPipe, count: Optional[int] = None):
        self.source_datapipe = source_datapipe
        self.count = count
        if count is not None and count < 0:
            raise ValueError(f"Expected non-negative count, got {count}")

    def __iter__(self):
        i = 0
        while self.count is None or i < self.count:
            for x in self.source_datapipe:
                yield x
            i += 1

    def __len__(self):
        if self.count is None:
            raise TypeError(
                f"This {type(self).__name__} instance cycles forever, and therefore doesn't have valid length"
            )
        else:
            return self.count * len(self.source_datapipe)
