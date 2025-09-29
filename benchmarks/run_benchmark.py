"""Benchmark script for USB PD Parser performance."""

import cProfile
import pstats
import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.pipeline_orchestrator import PipelineOrchestrator


def benchmark_full_pipeline():
    """Benchmark the full pipeline."""
    start_time = time.time()

    orchestrator = PipelineOrchestrator("application.yml")
    results = orchestrator.run_full_pipeline(mode=3)  # 200 pages for benchmark

    end_time = time.time()
    duration = end_time - start_time

    print(f"Pipeline completed in {duration:.2f} seconds")
    print(f"TOC entries: {results['toc_entries']}")
    print(f"Content items: {results['content_items']}")
    print(f"Performance: {results['content_items']/duration:.1f} items/second")

    return duration


def profile_pipeline():
    """Profile the pipeline with cProfile."""
    profiler = cProfile.Profile()

    profiler.enable()
    benchmark_full_pipeline()
    profiler.disable()

    # Save profile stats
    stats_file = Path("benchmarks/profile_stats.prof")
    profiler.dump_stats(str(stats_file))

    # Print top functions
    stats = pstats.Stats(profiler)
    stats.sort_stats("cumulative")
    print("\nTop 10 functions by cumulative time:")
    stats.print_stats(10)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", action="store_true", help="Run with profiling")
    args = parser.parse_args()

    if args.profile:
        profile_pipeline()
    else:
        benchmark_full_pipeline()
