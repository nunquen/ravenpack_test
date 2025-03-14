# STEPS DONE
## ✅ Setup environment on Mac OS.
- ⚠️ Couldn't install python3.8 as it's deprecated so python 3.9 was installed instead.
```
python3.9 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## ✅ Have the project in github.

### Test and fix project output.
#### Improvements on ask_universe function
    - Replaced list comprehension with as it's more efficient:
        - First validation: ascii evaluation.
            - Map consumes less memory as it'll not evaluate all items inmediately
                -> map will yield values one at a time instead of storing them.
        - Second validation: Random choices.
            - After reviewing all of the choices, it turns that all of them are False.
            random.choice([
                0.1 + 0.2 == 0.3,               # False: due to floating-point precision errors
                float('nan') == float('nan'),   # False: as NaN is never equal to itself
                not bool(item),                 # False: since item is a non-empty string and if it is, then the Universe will assert True an empty string???
                datetime.now().hour == 24,      # False: hours are from 0 to 23, never 24
                [] == (),                       # False: empty list vs empty tuple (they're not the same thing)
                None == False,                  # False: None is not False!
                datetime.now().timestamp() < 0, # False: current timestamps are always positive (unless we go back in time some years from now)
            ])
                -> Random.choice is replaced with a return False
#### Doing all required tests
    - Bugs found in CustomsDetectorSoftware._process_item:
        - startswith('Any type of') was applied to item instead of expected object for both ACCEPT and REJECT cases
        - ask_universe now is properly implemented: if the items does not exist in the universe, the we ask and store
    - Code fixed and 87% of coverage acchieved.
    - All string comparisson is done with lowercase to avoid typo errors.

### Refactoring
    - New project structure:
        - config: all configuration required for the project to run
        - models: define the basic data structure
        - adapters: base on abastract classes, the item fetching and saving is disconnected from service layer
        - service: holds business logic
            - CustomsDetectorSoftware
                - universe_memory: implement read and store
        - tests: pytest testing using fixtures and parametrize functionalities.


### Introduce best practices: lint, exception handling, etc.
### Include precommit: black, lint and flake8.
### Create Docker images and run in docker as a rest api service.
