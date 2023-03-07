# Main class for FNSynoptics backend structure.
from TraceMap import TraceMap


def main():
    path = r"C:\Users\thech\Desktop\MIEI\Dissertation\Fiber Networks Synoptics\doc\dxf\exemplo VODAFONE\01 - Traçado de Rede Secundária\01 - Traçado de Rede Secundária_PEN15.dxf"
    trace_map = TraceMap(path)
    trace_map.parser()
    # trace_map.parse_to_list()
    # trace_map.print_maps()
    # trace_map.print_lists()
    return


main()
