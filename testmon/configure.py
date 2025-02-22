import sys
import re

try:
    from coverage.tracer import CTracer as Tracer
except ImportError:
    from coverage.pytracer import PyTracer as Tracer


def _is_dogfooding(coverage_stack):
    return coverage_stack


def _is_debugger():
    return sys.gettrace() and not isinstance(sys.gettrace(), Tracer)


def _is_coverage():
    return False


def _deactivate_on_xdist(options):
    return False
    return (
        options.get("numprocesses", False)
        or options.get("distload", False)
        or options.get("dist", "no") != "no"
    )


def _get_notestmon_reasons(options, xdist):
    if options["no-testmon"]:
        return "deactivated through --no-testmon"

    if options["testmon_noselect"] and options["testmon_nocollect"]:
        return "deactivated, both noselect and nocollect options used"

    if not any(
        options[t]
        for t in [
            "testmon",
            "testmon_noselect",
            "testmon_nocollect",
            "testmon_forceselect",
        ]
    ):
        return "not mentioned"

    if xdist:
        return "deactivated, execution with xdist is not supported"

    return None


def _get_nocollect_reasons(
    options,
    debugger=False,
    coverage=False,
    dogfooding=False,
    cov_plugin=False,
):
    if options["testmon_nocollect"]:
        return [None]

    if cov_plugin:
        return []

    if coverage and not dogfooding:
        return ["coverage.py was detected and simultaneous collection is not supported"]

    if debugger and not dogfooding:
        return ["it's not compatible with debugger"]

    return []


def _get_noselect_reasons(options):
    if options["testmon_forceselect"]:
        return []

    if options["testmon_noselect"]:
        return [None]

    if options["keyword"]:
        return ["-k was used"]

    if options["markexpr"]:
        return ["-m was used"]

    if options["lf"]:
        return ["--lf was used"]

    if any(re.match(r"(.*)\.py::(.*)", opt) for opt in options["file_or_dir"] or []):
        return ["you selected tests manually"]

    return []


def _formulate_deactivation(what, reasons):
    if reasons:
        return [
            f"{what} automatically deactivated because {reasons[0]}, "
            if reasons[0]
            else what + " deactivated, "
        ]
    return []


def _header_collect_select(
    options,
    debugger=False,
    coverage=False,
    dogfooding=False,
    xdist=False,
    cov_plugin=False,
):
    notestmon_reasons = _get_notestmon_reasons(options, xdist=xdist)

    if notestmon_reasons == "not mentioned":
        return None, False, False
    if notestmon_reasons:
        return "testmon: " + notestmon_reasons, False, False

    nocollect_reasons = _get_nocollect_reasons(
        options,
        debugger=debugger,
        coverage=coverage,
        dogfooding=dogfooding,
        cov_plugin=cov_plugin,
    )

    noselect_reasons = _get_noselect_reasons(options)

    if nocollect_reasons or noselect_reasons:
        message = "".join(
            _formulate_deactivation("collection", nocollect_reasons)
            + _formulate_deactivation("selection", noselect_reasons)
        )
    else:
        message = ""

    return (
        f"testmon: {message}",
        not bool(nocollect_reasons),
        not bool(noselect_reasons),
    )


def header_collect_select(config, coverage_stack, cov_plugin=None):
    options = vars(config.option)
    return _header_collect_select(
        options,
        debugger=_is_debugger(),
        coverage=_is_coverage(),
        dogfooding=_is_dogfooding(coverage_stack),
        xdist=_deactivate_on_xdist(options),
        cov_plugin=cov_plugin,
    )
