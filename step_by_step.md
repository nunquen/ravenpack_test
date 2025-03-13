# STEPS DONE
## ✅ Setup environment on Mac OS.
- ⚠️ Couldn't install python3.8 as it's deprecated so python 3.9 was installed instead.

## ✅ Have the project in github.

### Test and fix project output.
#### Improvements on ask_universe functions
    - Replaced list comprehension with as it's more efficient:
        - First validation: ascii evaluation.
            - Map consumes less memory as it'll not evaluate all items inmediately
                -> map will yield values one at a time instead of storing them.
        - Second validation: Random choices.
            - After reviewing all of the choices, it returns that all of them are False.
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



- Improve code and add exception handling.
- Refactor.
- Include precommit: black, lint and flake8.
- Create Docker images and run in docker as a rest api service.
