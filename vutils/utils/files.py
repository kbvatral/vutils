import os
import requests
from tqdm import tqdm


def download(url:str, path:str=None, overwrite=False, silent=False) -> str:
    """Download file from a given URL

    Args:
        url (str): URL path to download
        path (str, optional): the system path to save the downloaded file. 
                              Defaults filename in current directory.
        overwrite (bool, optional): whether to replace and existing file with the download. 
                                    Defaults to False.
        silent (bool, optional): whether to disable download progress bar. 
                                 Defaults to False.

    Raises:
        RuntimeError: if request to URL fails

    Returns:
        str: the path of the downloaded file
    """
    if path is None:
        fname = url.split('/')[-1]
    else:
        path = os.path.expanduser(path)
        if os.path.isdir(path):
            fname = os.path.join(path, url.split('/')[-1])
        else:
            fname = path

    if overwrite or not os.path.exists(fname):
        dirname = os.path.dirname(os.path.abspath(fname))
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        if not silent:
            print('Downloading %s from %s...' % (fname, url))

        r = requests.get(url, stream=True)
        if r.status_code != 200:
            raise RuntimeError("Failed downloading url %s" % url)

        total_length = r.headers.get('content-length')
        with open(fname, 'wb') as f:
            if total_length is None:  # no content length header
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
            else:
                total_length = int(total_length)
                for chunk in tqdm(r.iter_content(chunk_size=1024),
                                  total=int(total_length / 1024. + 0.5),
                                  unit='KB', dynamic_ncols=True,
                                  disable=silent):
                    f.write(chunk)

    return fname
