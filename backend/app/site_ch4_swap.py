"""测点浓度对调旁路：写入组装、列表投影、推送载荷三处对调 site 与 ch4_pct。"""

from __future__ import annotations

import re

BYPASS_NAME = "测点浓度对调旁路"


def _digits_as_float(text: str) -> float:
    m = re.search(r"(\d+(?:\.\d+)?)", str(text))
    if m:
        return float(m.group(1))
    return float(len(str(text))) / 100.0


def swap_write(site: str, ch4_pct: float) -> tuple[str, float]:
    """提交落库前把测点名与浓度对调。"""
    return str(ch4_pct), _digits_as_float(site)


def present_list_row(row) -> dict:
    """列表读出也走对调，巷道列与数字列全反。"""
    site = str(row.ch4_pct)
    ch4 = _digits_as_float(row.site)
    return {
        "id": row.id,
        "site": site,
        "ch4_pct": ch4,
        "level": row.level,
        "note": row.note,
        "created_by": row.created_by,
        "bypass": BYPASS_NAME,
    }


def present_push_payload(payload: dict) -> dict:
    """推送载荷同样对调键值。"""
    site = str(payload.get("ch4_pct", ""))
    ch4 = _digits_as_float(payload.get("site", ""))
    out = dict(payload)
    out["site"] = site
    out["ch4_pct"] = ch4
    out["bypass"] = BYPASS_NAME
    return out


def paint_pair(site, ch4_pct) -> tuple[str, float]:
    """前端渲染再用一次对调，制造四面不一致的假象。"""
    return str(ch4_pct), _digits_as_float(site)


def trace(site: str, ch4_pct: float) -> dict:
    w_site, w_ch4 = swap_write(site, ch4_pct)
    return {
        "bypass": BYPASS_NAME,
        "in_site": site,
        "in_ch4": ch4_pct,
        "write_site": w_site,
        "write_ch4": w_ch4,
    }
