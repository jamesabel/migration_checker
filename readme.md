
# Migration Checker #

Checks that a disk migration was successful.

(Can be used for backups if this is run at the time the backup is done.)

it consists of 2 applications: `save.py` and `check.py`.

## Targeted Use ##

The targeted uses are:

- Migration of from one machine to another
- Migration from one disk to another
- Restoring from backups



## save.py ##

Traverses a file system and saves off the path, size and (optionally)
attributes for all files.  This file will later be used by check.py
on the restored system.

## check.py ##

Checks that the current system has the same files that the original
system did.
