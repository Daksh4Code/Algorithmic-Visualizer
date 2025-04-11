# ALGOVISUALIZER: Instruction & Explanation Documentation (See PresentationDocument for PDF)

## Instructions

### First, run the 'AlgorithmicVisualizer.py file' A grid like screen should be displayed, along with an (optional) music file in the background. Then, follow the instructions below. 

1. **To set the starting point:**  
   Click once anywhere on the grid where you want it to be located.

2. **To set the endpoint:**  
   Click once anywhere on the grid where you want it to be located after placing the start point.

3. **To add walls:**  
   Click anywhere on the grid to place them in your desired location.  
   You can add multiple walls as needed.

4. **Choose an algorithm** and click the corresponding button to visualize the pathfinding process.

5. **To start over:**  
   Simply click the reset button.

---

## The Different Algorithms

### 1. Breadth First Search (BFS)
- Visits all nodes at the current depth level before moving to the next.
- Guarantees the shortest path from the starting node to the ending node.
- **Time Complexity:** O(V + E)  
- **Space Complexity:** O(V)

### 2. Depth First Search (DFS)
- Visits nodes as far as possible along each branch before backtracking.
- Does **not** always guarantee the shortest path.
- **Time Complexity:** O(V + E)  
- **Space Complexity:** O(V)

### 3. Dijkstra's Algorithm
- Similar to BFS but works with weighted graphs using a priority queue.
- Guarantees the shortest path.
- **Time Complexity:** O(V²)  
- **Space Complexity:** O(V)

### 4. A* Search
- Informed search using cost so far + heuristic estimate.
- Guarantees the shortest path if heuristic is admissible.
- **Time and Space Complexity:** Depends on the heuristic and implementation.

### 5. Greedy Best First Search
- Informed search using heuristic only.
- Does **not** guarantee the shortest path.
- **Time and Space Complexity:** Depends on the heuristic and implementation.
