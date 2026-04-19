"""Paginación y enlaces HATEOAS (_limit / _offset)."""
from urllib.parse import urlencode

DEFAULT_LIMIT = 10


def parse_pagination_args(args):
    """
    Lee _limit y _offset desde request.args (Flask).
    Devuelve (limit, offset). Lanza ValueError con mensaje para respuesta 400.
    """
    raw_limit = args.get("_limit", default=DEFAULT_LIMIT, type=int)
    raw_offset = args.get("_offset", default=0, type=int)

    if raw_limit is None or raw_offset is None:
        raise ValueError("_limit y _offset deben ser enteros válidos.")
    if raw_limit < 1:
        raise ValueError("_limit debe ser mayor o igual a 1.")
    if raw_offset < 0:
        raise ValueError("_offset no puede ser negativo.")

    return raw_limit, raw_offset


def build_hateoas_links(*, base_path: str, limit: int, offset: int, total: int) -> dict:
    """base_path: URL absoluta hasta el path (sin query). limit/offset vienen de parse_pagination_args."""

    def href(off: int) -> str:
        return f"{base_path}?{urlencode({'_limit': limit, '_offset': off})}"

    last_offset = 0
    if total > 0:
        last_offset = max(0, ((total - 1) // limit) * limit)

    links: dict = {
        "_first": {"href": href(0)},
        "_last": {"href": href(last_offset)},
    }
    if offset > 0:
        links["_prev"] = {"href": href(max(0, offset - limit))}
    if offset + limit < total:
        links["_next"] = {"href": href(offset + limit)}

    return links