import dmdownloader.functional.FLfunctions as fl

class filterBase:
    def __init__(self, name, func):
        self.name = name
        self.do = func
top_filter = filterBase("top_filter", lambda dmk: dmk["type"] == 1)
bottom_filter = filterBase("bottom_filter", lambda dmk: dmk["type"] == 2)
none_filter = filterBase("none_filter", lambda dmk: dmk["type"] == -1)
# TODO: more filter

def load_filter(global_config: dict) -> list:
    filters = [none_filter]
    if global_config["top_filter"]:
        filters.append(top_filter)
    if global_config["bottom_filter"]:
        filters.append(bottom_filter)
    return filters

def Reportdecorater(filter):
    report = 0
    def do(x):
        nonlocal report
        flg = filter.do(x)
        if flg: report += 1
        return flg
    def get_report():
        nonlocal report
        return (filter.name, report)
    
    return (do, get_report)

def filter_separator(pre, curr):
    pre[0].append(curr[0])
    pre[1].append(curr[1])
    return pre

# TODO 能跑，但逻辑有点乱
def do(global_config: dict, danmakus:list[dict]) -> tuple[list[dict], dict[str, int], int]:
    '''
        A filter, as it's name

        return:
            result, the filted danmakus list
            report detail, see `get_report_detail()`
    '''
    filters = load_filter(global_config)

    funcs = [fl.curried_map(lambda filter: Reportdecorater(filter)),
            lambda x: fl.reduce(fl.reduceAdaptor(filter_separator), x, [[],[]])]
    decorated_filter, get_reports = fl.pipe(funcs)(filters)

    filter_funcs = fl.curried_map(lambda filter: fl.curried_filter(filter))(decorated_filter)
    result = fl.pipe(filter_funcs)(danmakus)

    return (result, get_report_detail(danmakus, result, fl.map(lambda fun: fun(), get_reports)))

filter_report_template: str = "过滤 %(filted)d 条弹幕\n共 %(total)d 条，剩余 %(left)d 条\n详细: %(filter_detail)s"
def get_report_detail(dmks, result, filter_detail):
    report = {}
    report["total"] = len(dmks)
    report["filter_detail"] = filter_detail
    report["left"] = len(result)
    report["filted"] = fl.reduce(fl.reduceAdaptor(lambda pre, curr: pre + curr[1]), filter_detail, 0)
    return report