from debug_menu import DebugMenu

def main():
    import multiprocessing
    multiprocessing.freeze_support() # Allow multiprocessing to be ran on Windows
    """Runs the debugging operation."""
    DebugMenu.options()

if __name__ == '__main__':
    main()
