import pyx.rich
from examples.progress_bar import ProgressBar
from pyx import E


def Main():
    # Equivalent to `return (
    #   <>
    #     <ProgressBar interval={0.03} />
    #     <ProgressBar interval={0.04} />
    #     <ProgressBar interval={0.05} />
    #     <ProgressBar interval={0.06} />
    #   </>
    # )`
    return E()[
        E(ProgressBar, interval=0.03),
        E(ProgressBar, interval=0.04),
        E(ProgressBar, interval=0.05),
        E(ProgressBar, interval=0.06),
    ]


if __name__ == "__main__":
    # Equivalent to createRoot(<Main />)
    pyx.rich.run(E(Main))
