from src.run_benchmark import run_benchmark, test_connection
from parameters import TEST

if __name__ == '__main__':
    if TEST:
        test_connection()
    else:
        run_benchmark()

        print('\n +----------------------------------------------------------------------------+'
              '\n | Hurray! The benchmark run is finished!                                     |'
              '\n | Go back to MANUAL.md to read instructions on how to interpret the results. |'
              '\n +----------------------------------------------------------------------------+')
