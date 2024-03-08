import base64

from cache.files import add_cached_file

def save_uploaded_file(name: str, content: str) -> int:
    """
    Decode and store a file uploaded with Plotly Dash. The file will be saved in the cache folder.

    The file name is automatically generated, the information is saved in `file_handling.cached_files`
    
    The cache folder is defined in `file_handling.CACHE_DIR`.

    Parameters
    ----------
    name : string
        The name of the new file
    content: string
        base64-encoded content as received from Dash upload function
    automatic_name: bool
        if True, the file name will be generated automatically (this is done to prevent filename collisions)

    Returns
    -------
    Returns cached file ID
    """

    id, path = add_cached_file(name)
    
    # remove the header added by Dash
    data = content.encode("utf8").split(b";base64,")[1]
    
    # decode and save the content
    with open(path, "wb") as fp:
        fp.write(base64.decodebytes(data))

    return id