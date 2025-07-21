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


if __name__ == "__main__":
    pyx.rich.run(E(Main))
