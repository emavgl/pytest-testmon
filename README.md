<img src=https://user-images.githubusercontent.com/135344/219700265-0a9b152f-7285-4607-bbce-0c9aeddd520b.svg width=300>

This is a pytest plug-in which automatically selects and re-executes
only tests affected by recent changes. How is this possible in dynamic
language like Python and how reliable is it? Read here: [Determining
affected tests](https://testmon.org/determining-affected-tests.html)

## Quickstart

    pip install pytest-testmon

    # build the dependency database and save it to .testmondata
    pytest --testmon

    # change some of your code (with test coverage)

    # only run tests affected by recent changes
    pytest --testmon

To learn more about different options you can use with testmon, please
head to [testmon.org](https://testmon.org)

All command line options

```
--testmon	(select and collect) select only tests affected by recent changes and update the testmon database. In some circumstances different options are also forced. See below.
--testmon-noselect	Don't deselect, execute all tests picked up by pytest and create/update respective records in .testmondata. Forced if you use --testmon with some test selector (-k, -m, --last-failed, test_file.py::test_x, etc.)
--testmon-nocollect	Don't track, just deselect based on existing database and changes. This is forced also when you use --testmon with debugger or Coverage.py.
--testmon-forceselect	Selects only tests which both reach changed code and satisfy pytest selectors.
--no-testmon	Turn off (even if activated from config by default).
--testmon-env=<STRING>	This allows you to have separate coverage data within one .testmondata file, e.g. when using the same source code serving different endpoints or django settings.
```