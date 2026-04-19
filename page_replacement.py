"""
=============================================================
Lab Assignment-3: Page Replacement Algorithms
Course: Fundamentals of Operating System Lab (ENCA252)
Program: BCA (AI & DS) - K.R. Mangalam University
=============================================================
Algorithms Implemented:
  1. FIFO          - First In First Out
  2. LRU           - Least Recently Used
  3. Optimal       - Optimal Page Replacement
  4. MRU           - Most Recently Used
  5. Second Chance - Clock Algorithm
=============================================================
"""

from collections import deque, OrderedDict


# ─────────────────────────────────────────────
# TASK 1 – Input Handling
# ─────────────────────────────────────────────
def get_input():
    """Read number of frames and page reference string from the user."""
    print("\n" + "=" * 60)
    print("      PAGE REPLACEMENT ALGORITHM SIMULATOR")
    print("=" * 60)

    frames = int(input("\nEnter number of frames: "))
    raw = input("Enter page reference string (space-separated): ")
    pages = list(map(int, raw.split()))

    print(f"\nFrames        : {frames}")
    print(f"Reference Str : {pages}")
    print(f"Total Pages   : {len(pages)}")
    return frames, pages


# ─────────────────────────────────────────────
# TASK 2 – FIFO (First In First Out)
# ─────────────────────────────────────────────
def fifo(pages, num_frames):
    """
    Oldest page is replaced first.
    Uses a queue: front = oldest page.
    """
    frames = []       # pages currently in memory
    queue  = deque()  # tracks arrival order
    faults = 0
    log    = []

    for page in pages:
        hit = page in frames
        if not hit:
            faults += 1
            if len(frames) < num_frames:
                frames.append(page)
                queue.append(page)
            else:
                evict = queue.popleft()          # remove oldest
                frames[frames.index(evict)] = page
                queue.append(page)
        log.append((page, list(frames), "HIT" if hit else "FAULT"))

    return faults, log


# ─────────────────────────────────────────────
# TASK 3 – LRU (Least Recently Used)
# ─────────────────────────────────────────────
def lru(pages, num_frames):
    """
    Least recently used page is replaced.
    OrderedDict keeps usage order; move_to_end() = mark as recent.
    """
    cache  = OrderedDict()
    faults = 0
    log    = []

    for page in pages:
        hit = page in cache
        if not hit:
            faults += 1
            if len(cache) >= num_frames:
                cache.popitem(last=False)   # evict LRU (first item)
            cache[page] = None
        else:
            cache.move_to_end(page)         # mark as most recently used
        log.append((page, list(cache.keys()), "HIT" if hit else "FAULT"))

    return faults, log


# ─────────────────────────────────────────────
# TASK 4 – Optimal Page Replacement
# ─────────────────────────────────────────────
def optimal(pages, num_frames):
    """
    Replace the page not used for the longest time in future.
    Minimum page faults — used as benchmark only (needs future knowledge).
    """
    frames = []
    faults = 0
    log    = []

    for i, page in enumerate(pages):
        hit = page in frames
        if not hit:
            faults += 1
            if len(frames) < num_frames:
                frames.append(page)
            else:
                # Find future use index for each frame
                future = {}
                for f in frames:
                    try:
                        future[f] = pages[i + 1:].index(f)
                    except ValueError:
                        future[f] = float('inf')  # never used again
                evict = max(future, key=future.get)
                frames[frames.index(evict)] = page
        log.append((page, list(frames), "HIT" if hit else "FAULT"))

    return faults, log


# ─────────────────────────────────────────────
# TASK 5 – MRU (Most Recently Used)
# ─────────────────────────────────────────────
def mru(pages, num_frames):
    """
    Most recently used page is replaced.
    Useful for cyclic access patterns.
    """
    frames     = []
    recent_use = []   # last element = most recently used
    faults     = 0
    log        = []

    for page in pages:
        hit = page in frames
        if not hit:
            faults += 1
            if len(frames) < num_frames:
                frames.append(page)
            else:
                evict = recent_use[-1]               # evict most recent
                frames[frames.index(evict)] = page
                recent_use.remove(evict)
        else:
            recent_use.remove(page)

        recent_use.append(page)
        log.append((page, list(frames), "HIT" if hit else "FAULT"))

    return faults, log


# ─────────────────────────────────────────────
# TASK 5b – Second Chance (Clock Algorithm)
# ─────────────────────────────────────────────
def second_chance(pages, num_frames):
    """
    Modified FIFO with a reference bit per frame.
    ref=1 → give second chance (reset to 0, skip).
    ref=0 → evict.
    Clock hand sweeps through frames.
    """
    frames  = []     # list of (page, reference_bit)
    faults  = 0
    log     = []
    pointer = 0      # clock hand position

    for page in pages:
        page_list = [f[0] for f in frames]
        hit = page in page_list

        if not hit:
            faults += 1
            if len(frames) < num_frames:
                frames.append((page, 1))
            else:
                # Sweep clock hand until ref=0 found
                while True:
                    p, ref = frames[pointer % num_frames]
                    if ref == 0:
                        frames[pointer % num_frames] = (page, 1)
                        pointer = (pointer + 1) % num_frames
                        break
                    else:
                        frames[pointer % num_frames] = (p, 0)  # second chance
                        pointer = (pointer + 1) % num_frames
        else:
            # Set reference bit to 1 on hit
            idx = page_list.index(page)
            frames[idx] = (page, 1)

        snap = [f[0] for f in frames]
        log.append((page, list(snap), "HIT" if hit else "FAULT"))

    return faults, log


# ─────────────────────────────────────────────
# Helper – Print Step-by-Step Table
# ─────────────────────────────────────────────
def print_table(algo_name, log, faults, num_frames):
    """Display execution trace in a clean table."""
    print(f"\n{'─' * 60}")
    print(f"  {algo_name}")
    print(f"{'─' * 60}")
    col_w = num_frames * 5
    print(f"{'Page':>6} | {'Frames':<{col_w}} | Status")
    print("─" * (14 + col_w))
    for page, frames, status in log:
        frame_str = "  ".join(f"{f:>3}" for f in frames)
        print(f"{page:>6} | {frame_str:<{col_w}} | {status}")
    print(f"\n  ➤ Total Page Faults: {faults}")


# ─────────────────────────────────────────────
# TASK 6 – Performance Comparison
# ─────────────────────────────────────────────
def compare_algorithms(results):
    """Print ranked comparison of all algorithms."""
    print("\n" + "=" * 60)
    print("         PERFORMANCE COMPARISON")
    print("=" * 60)
    print(f"{'Algorithm':<25} | {'Page Faults':>12} | Rank")
    print("─" * 50)

    sorted_r = sorted(results.items(), key=lambda x: x[1])
    for rank, (algo, faults) in enumerate(sorted_r, 1):
        print(f"{algo:<25} | {faults:>12} | #{rank}")

    print(f"\n  ✔ Best  : {sorted_r[0][0]}  ({sorted_r[0][1]} faults)")
    print(f"  ✘ Worst : {sorted_r[-1][0]} ({sorted_r[-1][1]} faults)")


# ─────────────────────────────────────────────
# TASK 7 – Result Analysis
# ─────────────────────────────────────────────
def analyze_results(results):
    """Print pros/cons and conclusion for each algorithm."""
    print("\n" + "=" * 60)
    print("         RESULT ANALYSIS & CONCLUSION")
    print("=" * 60)

    analysis = {
        "FIFO": (
            "Simple queue-based replacement. Easy to implement.\n"
            "    Con: Can suffer Belady's Anomaly. Ignores usage frequency."
        ),
        "LRU": (
            "Exploits temporal locality. Good real-world performance.\n"
            "    Con: Requires usage tracking overhead."
        ),
        "Optimal": (
            "Theoretically minimum faults. Perfect benchmark.\n"
            "    Con: Requires future knowledge — NOT usable in practice."
        ),
        "MRU": (
            "Good for cyclic/sequential scan workloads.\n"
            "    Con: Poor for general workloads. Often worst performer."
        ),
        "Second Chance": (
            "Practical FIFO improvement using reference bits.\n"
            "    Pro: Approximates LRU with low overhead. Used in Linux kernel."
        ),
    }

    for algo, comment in analysis.items():
        faults = results.get(algo, "N/A")
        print(f"\n  [{algo}]  —  {faults} page faults")
        print(f"    {comment}")

    sorted_r = sorted(results.items(), key=lambda x: x[1])
    print("\n  CONCLUSION:")
    print(f"  • Optimal gives minimum faults ({sorted_r[0][1]}) but is impractical.")
    print(f"  • LRU ({results['LRU']} faults) is the best practical algorithm.")
    print(f"  • Second Chance ({results['Second Chance']} faults) is a good low-overhead alternative.")
    print(f"  • MRU and FIFO generally perform worse for typical reference strings.")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    # Task 1 – Input
    num_frames, pages = get_input()

    # Task 2-5 – Run all algorithms
    fifo_faults, fifo_log = fifo(pages, num_frames)
    lru_faults,  lru_log  = lru(pages, num_frames)
    opt_faults,  opt_log  = optimal(pages, num_frames)
    mru_faults,  mru_log  = mru(pages, num_frames)
    sc_faults,   sc_log   = second_chance(pages, num_frames)

    # Print step-by-step tables
    print_table("FIFO  (First-In First-Out)",       fifo_log, fifo_faults, num_frames)
    print_table("LRU   (Least Recently Used)",       lru_log,  lru_faults,  num_frames)
    print_table("Optimal Page Replacement",          opt_log,  opt_faults,  num_frames)
    print_table("MRU   (Most Recently Used)",        mru_log,  mru_faults,  num_frames)
    print_table("Second Chance (Clock Algorithm)",   sc_log,   sc_faults,   num_frames)

    # Task 6 – Comparison
    results = {
        "FIFO":          fifo_faults,
        "LRU":           lru_faults,
        "Optimal":       opt_faults,
        "MRU":           mru_faults,
        "Second Chance": sc_faults,
    }
    compare_algorithms(results)

    # Task 7 – Analysis
    analyze_results(results)

    print("\n" + "=" * 60)
    print("  Simulation Complete!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()