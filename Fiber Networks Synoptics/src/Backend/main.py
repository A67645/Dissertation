# Main class for FNSynoptics backend structure.
from TraceMap import TraceMap


def main():
    trace_map = TraceMap("CO-PEN", "144-FO")
    trace_map.draw()
    return


main()
