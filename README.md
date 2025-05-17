# Queueing Theory Calculator

A Python/Tkinter application for analyzing and visualizing M/M/1 and M/M/S queueing models. Enter arrival and service rates (or times), choose your model, and get key performance metrics instantly.

## Overview

This tool applies classic queueing theory formulas to help you:

- **Characterize** customer arrival and service processes.
- **Compute** utilization, average number in system/queue, and average times.
- **Compare** single-server (M/M/1) vs. multi-server (M/M/S) scenarios.
- **Optimize** number of servers to meet service-level targets.

## Features

- **Interactive GUI** – Easy form input and results display.  
- **M/M/1 & M/M/S Models** – Switch between one server or multiple servers.  
- **Pn Calculation** – Compute probability of exactly _n_ customers in system.  
- **Unit Converter** – Convert “clients per minute” ↔ “clients per hour.”  
- **Adaptive Layout** – Resizes gracefully on different screen sizes.  
- **Standalone Executable** – Bundle with PyInstaller for easy distribution.  

## Requirements

- Python 3.x  
- Tkinter (bundled with most Python installations)  

## Installation

1. **Clone the repo**  
   ```bash
   git clone https://github.com/yourusername/queueing-theory-calculator.git
   cd queueing-theory-calculator
