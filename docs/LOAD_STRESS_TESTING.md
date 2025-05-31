# Load and Stress Testing Guide

## Overview

The James Bland: ACME Edition load and stress testing suite provides comprehensive testing for:
- **Maximum Player Capacity**: Testing 6 concurrent players and rejection of excess players
- **Long-Duration Stability**: Extended gameplay sessions with memory monitoring
- **Network Interruption Recovery**: Disconnection and reconnection scenarios
- **Memory Leak Detection**: Monitoring for memory leaks over extended gameplay

## Quick Start

### Prerequisites

Install the required dependencies:
```bash
pip install -r requirements.txt
```

### Running Tests

#### Quick Test (5 minutes)
```bash
python scripts/run_stress_tests.py --quick
```

#### Standard Test (10 minutes)
```bash
python scripts/run_stress_tests.py
```

#### Custom Duration Test
```bash
python scripts/run_stress_tests.py --duration 30  # 30 minute test
```

#### Custom Report File
```bash
python scripts/run_stress_tests.py --report my_test_report.json
```

### Running Individual Test Suites

You can also run specific test categories:

```bash
# Maximum player capacity tests
python -m pytest tests/test_load_stress.py::TestMaximumPlayerCapacity -v

# Long duration stability tests
python -m pytest tests/test_load_stress.py::TestLongDurationStability -v

# Network interruption recovery tests
python -m pytest tests/test_load_stress.py::TestNetworkInterruptionRecovery -v

# Server resource monitoring tests
python -m pytest tests/test_load_stress.py::TestServerResourceMonitoring -v

# Utility function tests
python -m pytest tests/test_utils.py -v
```

## Test Categories

### 1. Maximum Player Capacity Tests

**Purpose**: Validate that the server properly handles the maximum number of concurrent players.

**Tests Include**:
- ✅ `test_maximum_6_players_connection`: Confirms 6 players can connect simultaneously
- ✅ `test_7th_player_rejection`: Verifies 7th player is properly rejected
- ✅ `test_concurrent_game_actions_6_players`: Tests simultaneous action submission

**Expected Results**:
- All 6 players connect successfully
- 7th player receives "lobby full" error
- No errors during concurrent action submission

### 2. Long-Duration Stability Tests

**Purpose**: Test server stability and memory usage over extended periods.

**Tests Include**:
- ✅ `test_5_minute_continuous_gameplay`: Configurable duration continuous gameplay
- ✅ `test_memory_leak_detection`: Detects memory leaks over multiple game cycles

**Key Metrics**:
- Memory growth should be < 50% over test period
- Error count should be < 5 for entire session
- Minimum rounds completed based on test duration

**Memory Monitoring**:
- Samples taken every 30 seconds
- Tracks RSS (Resident Set Size) and VMS (Virtual Memory Size)
- Flags concerning memory growth patterns

### 3. Network Interruption Recovery Tests

**Purpose**: Validate robust handling of network disconnections and reconnections.

**Tests Include**:
- ✅ `test_client_disconnection_during_game`: Mid-game player disconnection
- ✅ `test_host_disconnection_transfer`: Host disconnection and transfer
- ✅ `test_simultaneous_disconnections`: Multiple simultaneous disconnections

**Expected Behavior**:
- Remaining players continue unaffected
- Host transfer occurs smoothly
- Reconnecting players are handled gracefully
- Game state remains consistent

### 4. Server Resource Monitoring Tests

**Purpose**: Monitor CPU, memory, and network resource usage under load.

**Tests Include**:
- ✅ `test_cpu_usage_under_load`: CPU usage during connection stress
- ✅ `test_memory_usage_scaling`: Memory scaling with player count

**Performance Targets**:
- Average CPU usage < 80%
- Peak CPU usage < 95%
- Memory usage scaling should be linear
- Memory variance < 50% of average per player

### 5. Utility Function Tests

**Purpose**: Validate helper functions and core game logic utilities.

**Tests Include**:
- ✅ IP clamping functions (0-20 range)
- ✅ Random selection utilities
- ✅ Action validation logic
- ✅ Victory condition checking
- ✅ Player summary generation

## Test Reports

### Automated Report Generation

The stress testing script automatically generates detailed JSON reports with:

- **Test Results**: Pass/fail status for each test category
- **System Metrics**: CPU, memory, and network usage over time
- **Performance Analysis**: Averages, peaks, and trends
- **Recommendations**: Actionable suggestions based on results

### Sample Report Structure

```json
{
  "start_time": "2024-12-19T14:30:00",
  "duration_minutes": 10,
  "tests": {
    "maximum_player_capacity": {
      "status": "passed",
      "subtests": {
        "6_players": {"returncode": 0, "duration": 15.2},
        "7th_player_rejection": {"returncode": 0, "duration": 8.1},
        "concurrent_actions": {"returncode": 0, "duration": 22.3}
      }
    }
  },
  "system_metrics": {
    "cpu_usage": [{"timestamp": 0, "value": 25.3}, ...],
    "memory_usage": [{"timestamp": 0, "value": 45.1}, ...]
  },
  "summary": {
    "success_rate": 100.0,
    "system_performance": {
      "cpu_usage_avg": 28.5,
      "cpu_usage_max": 45.2,
      "memory_usage_avg": 52.1,
      "memory_usage_max": 58.7
    },
    "recommendations": [
      "GOOD: All stress tests passed with good performance metrics."
    ]
  }
}
```

## Interpreting Results

### Success Criteria

**✅ PASSING RESULTS**:
- All test categories return status "passed"
- CPU usage averages < 80%
- Memory growth < 50% over test duration
- Error count < 5 for long-duration tests
- All 6 players can connect and play simultaneously

**⚠️ WARNING SIGNS**:
- CPU usage consistently > 70%
- Memory usage > 80% of system capacity
- Memory growth > 30% during testing
- Occasional test failures (< 25% failure rate)

**❌ CRITICAL ISSUES**:
- Multiple test category failures
- CPU usage > 90% sustained
- Memory leaks detected (growth > 50%)
- Server crashes or unrecoverable errors

### Performance Recommendations

Based on test results, you may receive recommendations such as:

- **HIGH**: Average CPU usage exceeded 70% - Consider optimizing server performance
- **CRITICAL**: Peak CPU usage exceeded 90% - Server may struggle under load
- **HIGH**: Memory usage exceeded 80% - Monitor for memory leaks
- **MEDIUM**: Some tests failed - Review error logs for issues

## Troubleshooting

### Common Issues

**Issue**: Tests fail to start server
**Solution**: Ensure port 5000 is available and check firewall settings

**Issue**: Memory tests show false positives
**Solution**: Run tests on a clean system with minimal background processes

**Issue**: Network tests fail inconsistently
**Solution**: Check network stability and reduce concurrent network activity

**Issue**: Long duration tests timeout
**Solution**: Increase test duration limits or run shorter test cycles

### Debug Mode

For detailed debugging, run individual tests with verbose output:

```bash
python -m pytest tests/test_load_stress.py::TestMaximumPlayerCapacity -v -s --tb=long
```

### Log Analysis

Server logs are captured during testing. Check the test report JSON for:
- `stdout` and `stderr` fields in test results
- `errors` array for runtime issues
- System metrics for performance trends

## Performance Baselines

### Expected Performance (Development Machine)

**System Requirements**: 8GB RAM, 4-core CPU, solid-state storage

- **6 Players**: < 30% CPU, < 200MB additional RAM
- **Long Duration**: < 5% memory growth per hour
- **Network Recovery**: < 2 seconds for reconnection handling
- **Turn Processing**: < 500ms per turn with 6 players

### Scaling Considerations

- Memory usage scales approximately linearly with player count
- CPU usage may spike during turn resolution phases
- Network interruptions should not affect other players
- Long-duration sessions should maintain stable memory usage

## Continuous Integration

### Automated Testing

Include stress tests in your CI pipeline:

```yaml
# Example GitHub Actions snippet
- name: Run Load Tests
  run: |
    python scripts/run_stress_tests.py --quick
    # Upload test report as artifact
```

### Performance Regression Detection

Monitor test reports over time to detect:
- Increasing memory usage trends
- CPU performance degradation
- Network handling regressions
- Capacity limit changes

## Advanced Configuration

### Custom Test Parameters

Modify test behavior via environment variables:

```bash
export STRESS_TEST_DURATION=1800  # 30 minutes
export MAX_PLAYERS=6
export MEMORY_THRESHOLD=0.4  # 40% growth limit
```

### Test Data Collection

For research or optimization purposes, enable detailed profiling:

```bash
# Run with memory profiling
python -m memory_profiler scripts/run_stress_tests.py

# Run with CPU profiling
python -m cProfile -o stress_test.prof scripts/run_stress_tests.py
```

---

## Support

For issues with load testing:
1. Check the generated test report JSON for detailed error information
2. Review system resource availability (RAM, CPU, network)
3. Ensure all dependencies are properly installed
4. Verify no other services are using required ports (5000, 5001)

The load testing suite is designed to be robust and provide actionable feedback for maintaining game server performance under real-world conditions. 