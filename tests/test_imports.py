import importlib


def test_imports_smoke() -> None:
    modules = [
        "stress_prediction.utils.clean",
        "stress_prediction.utils.config",
        "stress_prediction.utils.download",
        "stress_prediction.utils.features",
        "stress_prediction.utils.metrics",
        "stress_prediction.utils.model",
        "stress_prediction.utils.plots",
        "stress_prediction.utils.split",
        "stress_prediction.utils.threshold",
        "stress_prediction.utils.utils",
    ]

    for module in modules:
        assert importlib.import_module(module) is not None
