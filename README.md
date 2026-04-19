# OS Lab Assignment-3
## Comprehensive Implementation of Page Replacement Algorithms

**Course:** Fundamentals of Operating System Lab (ENCA252)  
**Program:** BCA (AI & DS) (Research)  
**University:** K.R. Mangalam University, New Delhi  
**GitHub:** [rakesh4407](https://github.com/rakesh4407)

---

## 📌 Problem Statement

In modern operating systems, virtual memory allows efficient utilization of physical memory. When memory frames are full, page replacement algorithms are used to decide which page should be replaced.

This assignment implements and analyzes the following page replacement algorithms:
- **FIFO** — First In First Out
- **LRU** — Least Recently Used
- **Optimal** — Optimal Page Replacement
- **MRU** — Most Recently Used
- **Second Chance** — Clock Algorithm

---

## 📁 File Structure

```
OS-Lab-Assignment-3/
│
└── page_replacement.py      # Main Python file with all algorithms
```

---

## ⚙️ Tools & Technology Used

| Tool | Details |
|------|---------|
| Language | Python 3.x |
| Libraries | Built-in only (collections — deque, OrderedDict) |
| IDE | VS Code / PyCharm / IDLE |
| OS | Linux / Ubuntu / Windows |

---

## 🧠 Algorithms Implemented

### 1. FIFO — First In First Out
- Oldest page in memory is replaced first
- Uses a queue to track arrival order
- Simple but can suffer from **Belady's Anomaly**

### 2. LRU — Least Recently Used
- Replaces the page that was least recently accessed
- Exploits **temporal locality**
- Implemented using Python's `OrderedDict` for efficient tracking

### 3. Optimal Page Replacement
- Replaces the page that will not be used for the longest time in the future
- Gives **minimum possible page faults**
- Not implementable in practice — used only as a benchmark

### 4. MRU — Most Recently Used
- Replaces the most recently used page
- Useful in **cyclic access patterns**
- Generally performs worse than LRU for typical workloads

### 5. Second Chance (Clock Algorithm)
- Modified FIFO with a **reference bit** per page
- If reference bit = 1 → give second chance (reset to 0)
- If reference bit = 0 → evict the page
- Approximates LRU with low overhead — used in real OS kernels

---

## ▶️ How to Run

### On Linux / Ubuntu:
```bash
python3 page_replacement.py
```

### On Windows (PowerShell):
```powershell
python page_replacement.py
```

---

## 📥 Sample Input

```
Enter number of frames: 3
Enter page reference string: 7 0 1 2 0 3 0 4 2 3 0 3 2 1 2 0 1 7 0 1
```

---

## 📤 Sample Output

```
FIFO  (First-In First-Out)
  Total Page Faults: 15

LRU   (Least Recently Used)
  Total Page Faults: 12

Optimal Page Replacement
  Total Page Faults: 9

MRU   (Most Recently Used)
  Total Page Faults: 16

Second Chance (Clock Algorithm)
  Total Page Faults: 14
```

---

## 📊 Performance Comparison

| Algorithm | Page Faults | Rank |
|-----------|------------|------|
| Optimal       | 9  | #1 ✔️ |
| LRU           | 12 | #2 |
| Second Chance | 14 | #3 |
| FIFO          | 15 | #4 |
| MRU           | 16 | #5 ✘ |

---

## 📝 Conclusion

- **Optimal** gives minimum faults but requires future knowledge — not practical
- **LRU** is the best practical algorithm — exploits temporal locality
- **Second Chance** is a good low-overhead alternative to LRU
- **FIFO** is simple but can suffer from Belady's Anomaly
- **MRU** performs poorly for general workloads

---

## 🔗 Related Assignments

- [OS-Lab-Assignment-2](https://github.com/rakesh4407/OS-Lab-Assignment-2)
- [OS-Lab-Assignment-3](https://github.com/rakesh4407/OS-Lab-Assignment-3)
- [OS-Lab-Assignment-4](https://github.com/rakesh4407/OS-Lab-Assignment-4)
