# Main class for FNSynoptics backend structure.
from TraceMap import TraceMap
import AttributeProcessing as ap


def main():
    path = r"C:\Users\thech\Desktop\MIEI\Dissertation\Fiber Networks Synoptics\doc\dxf\exemplo VODAFONE\01 - Traçado de Rede Secundária\01 - Traçado de Rede Secundária_PEN15.dxf"
    # trace_map = TraceMap(path)
    # trace_map.parser()
    # trace_map.print_maps()
    # trace_map.print_lists()
    cable = "12FO - 175m"
    houses = "7HPs"
    jso = "JSO216"
    print(ap.get_fibers(cable))
    print(ap.get_length(cable))
    print(ap.get_houses(houses))
    print(ap.get_jso_from_pdo(jso))


main()
