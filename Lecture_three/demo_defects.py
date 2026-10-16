"""Порівняти той самий набір тестів на правильній і дефектних версіях.

Кожен експеримент створює тимчасову копію файлів та окремий процес Python.
Оригінальні image_ops.py й тести залишаються незмінними.
Це навчальний експеримент з трьома конкретними дефектами, а не повний
інструмент мутаційного тестування.
"""

import argparse
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent
IMPLEMENTATIONS = {
    "correct": "return max(0, min(255, pixel + delta))",
    "no_lower_bound": "return min(255, pixel + delta)",
    "no_upper_bound": "return max(0, pixel + delta)",
    "wrong_sign": "return max(0, min(255, pixel - delta))",
}


def run_experiment(suite="all"):
    if importlib.util.find_spec("pytest") is None:
        raise SystemExit("Спочатку встановіть залежності: python -m pip install -r requirements.txt")
    if suite == "first":
        tests = [ROOT / "test_image_ops.py"]
    elif suite == "student":
        tests = [ROOT / "test_student.py"]
        if not tests[0].is_file():
            raise SystemExit("Спочатку створіть test_student.py зі своїми тестами.")
    else:
        tests = sorted(ROOT.glob("test_*.py"))

    results = {}
    for name, body in IMPLEMENTATIONS.items():
        with tempfile.TemporaryDirectory(prefix="unit_tests_") as directory:
            target = Path(directory)
            (target / "image_ops.py").write_text(
                "def brighten(pixel, delta):\n    " + body + "\n", encoding="utf-8"
            )
            for test in tests:
                shutil.copyfile(test, target / test.name)
            environment = os.environ.copy()
            # Зовнішні pytest-плагіни не потрібні цьому навчальному прикладу.
            environment["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
            environment.pop("PYTEST_ADDOPTS", None)
            completed = subprocess.run(
                [sys.executable, "-m", "pytest", "-q", "--tb=short", "--color=no",
                 *[test.name for test in tests]],
                cwd=target, text=True, capture_output=True, env=environment,
            )
            print(f"\n=== {name} ===", flush=True)
            print(completed.stdout, end="", flush=True)
            if completed.stderr:
                print(completed.stderr, end="", flush=True)
            if completed.returncode not in (0, 1):
                raise SystemExit(
                    f"Код завершення {completed.returncode}: перевірте запуск "
                    "або збирання тестів; це не результат виявлення дефекту."
                )
            results[name] = completed.returncode
            if name == "correct" and completed.returncode != 0:
                raise SystemExit(
                    "Правильна версія не проходить набір: перевірте запуск і власні "
                    "очікування перед експериментами з дефектами."
                )

    print("\nПідсумок експерименту:")
    for name, status in results.items():
        if name == "correct":
            label = "правильна версія проходить" if status == 0 else "перевірте власні очікування"
        else:
            label = "дефект виявлено" if status == 1 else "дефект НЕ виявлено"
        print(f"{name}: {label}")

    if results["correct"] != 0:
        raise SystemExit("Правильна версія має проходити тести перед оцінкою дефектів.")
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", choices=["all", "first", "student"], default="all")
    run_experiment(parser.parse_args().suite)
