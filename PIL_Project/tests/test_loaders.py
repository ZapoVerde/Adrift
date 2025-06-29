from PIL.loaders import code_loader

def test_load_code_symbols_smoke():
    symbols = code_loader.load_code_symbols(project_root="tests/testdata")
    assert isinstance(symbols, list)