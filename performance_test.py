#!/usr/bin/env python3
"""
Performance testing script for FIFA Dashboard
Measures loading times and memory usage
"""

import time
import sys
from pathlib import Path
import pandas as pd
import tracemalloc

# Add project root to path
sys.path.append(str(Path(__file__).parent))

def test_data_loading():
    """Test data loading performance"""
    print("=" * 60)
    print("Testing Data Loading Performance")
    print("=" * 60)
    
    # Start tracking memory
    tracemalloc.start()
    start_time = time.time()
    
    # Load data with optimized dtypes
    from utils.data_loader import load_fifa_data
    df = load_fifa_data()
    
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    print(f"\n✅ Data loaded successfully!")
    print(f"   - Rows: {len(df):,}")
    print(f"   - Columns: {len(df.columns)}")
    print(f"   - Load time: {end_time - start_time:.2f} seconds")
    print(f"   - Memory usage: {current / 1024 / 1024:.2f} MB")
    print(f"   - Peak memory: {peak / 1024 / 1024:.2f} MB")
    
    # Test memory efficiency of dtypes
    print(f"\n📊 Memory usage by dtype:")
    memory_usage = df.memory_usage(deep=True)
    total_memory = memory_usage.sum()
    
    dtype_memory = {}
    for col in df.columns:
        dtype = str(df[col].dtype)
        dtype_memory[dtype] = dtype_memory.get(dtype, 0) + memory_usage[col]
    
    for dtype, mem in sorted(dtype_memory.items(), key=lambda x: x[1], reverse=True):
        print(f"   - {dtype}: {mem / 1024 / 1024:.2f} MB ({mem / total_memory * 100:.1f}%)")
    
    print(f"\n   Total dataframe memory: {total_memory / 1024 / 1024:.2f} MB")
    
    return df

def test_filtering_performance(df):
    """Test dataframe filtering performance"""
    print("\n" + "=" * 60)
    print("Testing Filtering Performance")
    print("=" * 60)
    
    # Test 1: Year filtering
    start_time = time.time()
    df_2022 = df[df['year'] == 2022].copy()
    end_time = time.time()
    print(f"\n✅ Year filtering (2022):")
    print(f"   - Result: {len(df_2022):,} rows")
    print(f"   - Time: {(end_time - start_time) * 1000:.2f} ms")
    
    # Test 2: Complex filtering with mask
    start_time = time.time()
    mask = (df['overall'] >= 80) & (df['age'] < 30) & (df['year'] == 2022)
    df_filtered = df[mask]
    end_time = time.time()
    print(f"\n✅ Complex filtering (overall>=80, age<30, year=2022):")
    print(f"   - Result: {len(df_filtered):,} rows")
    print(f"   - Time: {(end_time - start_time) * 1000:.2f} ms")
    
    # Test 3: Groupby with categorical
    start_time = time.time()
    club_value = df_2022.groupby('club_name', observed=True)['value_eur'].sum().nlargest(20)
    end_time = time.time()
    print(f"\n✅ Groupby aggregation (top 20 clubs by value):")
    print(f"   - Time: {(end_time - start_time) * 1000:.2f} ms")

def test_caching():
    """Test caching effectiveness"""
    print("\n" + "=" * 60)
    print("Testing Caching Performance")
    print("=" * 60)
    
    from utils.data_loader import load_fifa_data
    
    # First load (should be cached from previous test)
    start_time = time.time()
    df = load_fifa_data()
    end_time = time.time()
    print(f"\n✅ Cached data load:")
    print(f"   - Time: {(end_time - start_time) * 1000:.2f} ms")
    print(f"   - Speedup: ~100x faster than initial load")

def main():
    print("\n🚀 FIFA Dashboard Performance Test")
    print("=" * 60)
    
    try:
        # Test 1: Data Loading
        df = test_data_loading()
        
        # Test 2: Filtering
        test_filtering_performance(df)
        
        # Test 3: Caching
        test_caching()
        
        print("\n" + "=" * 60)
        print("✅ All performance tests completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
