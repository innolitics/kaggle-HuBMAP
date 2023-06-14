import logging
import os
import typing as t
from concurrent.futures import ThreadPoolExecutor, as_completed
from fastprogress import master_bar, progress_bar
from multiprocessing import cpu_count
from pathlib import Path

logger = logging.getLogger(__name__)


def get_paths(
    src_dir: os.PathLike,
    kwrd: str
    ) -> t.List[os.PathLike]:
    """
    Returns list of paths matching `kwrd` from `src_dir`.
    
    Args:
        src_dir: top level directory containing files of interest.
        kwrd: keyword to search for in paths from `src_dir`.
        
    Returns:
        List of paths in `src_dir` matching `kwrd`.
    """
    src_path = Path(src_dir)
    paths = sorted([str(p) for p in src_path.rglob(f'*{kwrd}')])
    logger.info(f'Found {len(paths)} paths in "{src_dir}" matching keyword "{kwrd}"')
    
    return paths

def make_concurrent(
    func: t.Callable,
    iterable: t.Iterable,
    progress: bool = False,
    max_workers: t.Optional[int] = None,
    *args,
    **kwargs
    ) -> t.List[t.Any]:
    """
    Makes a function run concurrently on the elements in `iterable`.

    Args:
        func: function to run concurrently
        iterable: items to apply function to
        progress: show progress bar
        max_workers: If `None`, all workers are used
        *args, **kwargs: for `func`
    """
    n = len(iterable)
    if max_workers is None:
        max_workers = min(len(iterable), cpu_count())
    result = []
    mb = master_bar(range(0, n, max_workers))

    for idx in mb if progress else range(0, n, max_workers):
        work_list = iterable[idx:idx+max_workers]
        with ThreadPoolExecutor(max_workers=len(work_list)) as executor:
            future = [executor.submit(func, i, *args, **kwargs) for i in work_list]
            if progress:
                for f in progress_bar(as_completed(future), total=len(work_list), parent=mb):
                    result.append(f.result())
            else:
                for f in as_completed(future):
                    result.append(f.result())

    return result