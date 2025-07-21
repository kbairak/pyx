import argparse
import io

import pyx.rich
from examples.progress_bar import ProgressBar
from pyx import E


def Main():
    show_msg, set_show_msg = pyx.use_state(False)

    def _on_complete():
        set_show_msg(True)

    # Equivalent to `return (
    #   <>
    #     <ProgressBar onComplete={onComplete} />
    #     {showMsg && <div>Hello world</div>}
    #   </>
    # )`
    return E()[
        E(ProgressBar, on_complete=_on_complete),
        E("div")["Done"] if show_msg else None,
    ]


parser = argparse.ArgumentParser(description="Progress bars example")
parser.add_argument("-s", action="store_true", help="Suppress output to enable debugging")

if __name__ == "__main__":
    args = parser.parse_args()
    pyx.rich.run(E(Main), file=io.StringIO() if args.s else None)
