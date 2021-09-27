import magic
import mimetypes

__all__ = ['get_mime', 'get_ext']

M = magic.Magic(mime=True)

def get_mime(buffer: bytes) -> str:
    return M.from_buffer(buffer)

def get_ext(buffer: bytes) -> str:
    mime = get_mime(buffer)
    return mimetypes.guess_extension(mime)
